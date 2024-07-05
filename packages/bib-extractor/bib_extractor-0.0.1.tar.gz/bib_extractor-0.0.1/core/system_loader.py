import logging 
import importlib
import json
from core_modules import BaseABC


class SystemNotLoadException(Exception):
    pass

class SystemLoader(BaseABC):
    def __init__(self, opts):
        super().__init__(opts)
        self.config_path = self.opts.config
        self.config = self._load_config()
        self._load_style_to_validator()
        self.logger.debug(f"{self.style_to_validator}")
        self.extractor, self.parsers, self.validators, self.bibformatter = {}, {}, {}, {}
        self._load_modules()
        self._test_modules()
        

    def _load_config(self):
        try:
            with open(self.config_path, 'r') as file:
                config = json.load(file)
                self.logger.info(f"Config file loaded successfully!")
                return config
        except FileNotFoundError as e:
            self.logger.error(f"File with config not found: {e}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON from config file: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error while loading config: {e}")
        # если конфиг не загрузился
        raise SystemNotLoadException("Config not loaded properly")
    
    def _load_style_to_validator(self, mess=None):
        try:
            self.style_to_validator = self.config['style_to_validator']
            self.logger.info(f"style_to_validator loaded successfully!")
        except KeyError as e:
            mess = f"KeyError in config. Check the correctness of config file: {e}"
        except Exception as e:
            mess = f"Check the correctness of config file: {e}"
        if mess:
            self.logger.error(mess)
            raise SystemNotLoadException(mess)

    def _import_module(self, module_path, *args):
        try:
            module_name, class_name = module_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            module_attr = getattr(module, class_name)(self.opts, *args)
            self.logger.info(f"Module '{class_name}' from '{module_name}' loaded successfully!")
            return module_attr
        except ImportError as e:
            self.logger.error(f"Failed to import module '{module_path}': {e}")
        except AttributeError as e:
            self.logger.error(f"Module '{module_path}' does not have attribute '{class_name}': {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error while loading module '{module_path}': {e}")
        # если модуль не загрузился
        raise SystemNotLoadException("Modules not loaded properly")
    
    def _load_module(self, module_path, *args):
        mess=None
        try:
            module = self._import_module(module_path, *args)
            return module
        except KeyError as e:
            mess = f"KeyError in config. Check the correctness of config file: {e}"
        except Exception as e:
            mess = f"Check the correctness of config file: {e}"
        if mess:
            self.logger.error(mess)
            raise SystemNotLoadException(mess)
    
    def _load_all_modules(self):
        mess=None
        try:
            self.extractor = self._load_module_by_name('extractor')
            self.parsers = self._load_module_by_name('parsers') # all parsers
            self.validators = self._load_module_by_name('validators') # all validators
            self.bibformatter = self._load_module_by_name('bibformatter')

            self._check_extractor()
            self._check_bibformatter()
        except KeyError as e:
            mess = f"KeyError in config. Check the correctness of config file: {e}"
        except Exception as e:
            mess = f"Check the correctness of config file: {e}"
        if mess:
            self.logger.error(mess)
            raise SystemNotLoadException(mess)
    
    
    def _load_module_by_name(self, module_type, module_name=None):
        if module_name:
            # если модуль указан явно - используем его
            if module_type == 'parsers':
                module = { module_name: self._load_module(
                    self.config['modules'][module_type][module_name]['path'], 
                    self.config['modules'][module_type][module_name]['confidence']
                    ) }
            else:
                module = { module_name: self._load_module(self.config['modules'][module_type][module_name]) }
        else:
            # по дефолту используем все модули
            self.logger.info(f"Use all modules of {module_type} by default")
            if module_type == 'parsers':
                module = { 
                    name: self._load_module(self.config['modules']['parsers'][name]['path'], self.config['modules']['parsers'][name]['confidence']) 
                    for name in self.config['modules']['parsers'].keys() 
                    }
            else:
                module = { 
                    name: self._load_module(self.config['modules'][module_type][name]) 
                    for name in self.config['modules'][module_type].keys() 
                    }
        return module


    def _check_extractor(self):
        if len(self.extractor) > 1 or len(self.extractor) == 0:
            self.logger.error(f"In System must be one (1) extractor, but in config {len(self.extractor)}.")
            raise SystemNotLoadException("Check amount extractors")


    def _check_bibformatter(self):
        if len(self.bibformatter) > 1 or len(self.bibformatter) == 0:
            self.logger.error(f"In System must be one (1) bibformatter, but in config {len(self.bibformatter)}.")
            raise SystemNotLoadException("Check amount bibformatters")


    
    def get_module_by_name(self, module_name, text_mode):
        """
        module_name - название ключа модуля из конфига
        text_mode - Validator or Parser - текстовое указание тип модуля, который загружаем
        """
        try:    
            module_list = self.mode_to_module_list[text_mode]
        except Exception as e:
            mess = f"Text mode incorrect. {e}"
            self.logger.error(mess)
            raise Exception(mess)
        if module_name:
            # если модуль указан явно - используем его
            try:
                modules = [ module_list[module_name] ] 
            except KeyError as e:
                self.logger.error(f"Failed to get {text_mode} by key '{module_name}' from system. Check the correctness of name: {e}")
                raise SystemNotLoadException(e)
            except Exception as e:
                self.logger.error(f"Unexpected error while get {text_mode} : {e}")
                raise SystemNotLoadException(e)
            self.logger.info(f"Use {text_mode} '{module_name}'")
        else:
            # по дефолту используем все модули
            modules = [module for _,module in module_list.items()]
            self.logger.info(f"Use all {text_mode}s by default")
        return modules
    
    def _load_modules(self):
        if self.opts.command == 'pipeline':
            self._load_all_modules()
        elif self.opts.command == 'extract':
            self.extractor = self._load_module_by_name('extractor')
            self._check_extractor()
        elif self.opts.command == 'parse':
            self.parsers = self._load_module_by_name('parsers', self.opts.parser)
            self.validators = self._load_module_by_name('validators', module_name=None) # all validators
        elif self.opts.command == 'validate':
            self.validators = self._load_module_by_name('validators', self.opts.validator)
        elif self.opts.command == 'bibformate':
            self.bibformatter = self._load_module_by_name('bibformatter')
            self._check_bibformatter()


    def _test_modules(self):
        try:
            self.logger.debug(f"Test extractor: {[extractor.test() for _,extractor in self.extractor.items()]}") if self.extractor else ''
            self.logger.debug(f"Test parsers: {[parser.test() for _,parser in self.parsers.items()]}") if self.parsers else ''
            self.logger.debug(f"Test validator: {[validator.test() for _,validator in self.validators.items()]}") if self.validators else ''
            self.logger.debug(f"Test bibformatter: '{[bibformatter.test() for _,bibformatter in self.bibformatter.items()]}'") if self.bibformatter else ''
        except Exception as e:
            self.logger.error(f"Failed test modules: {e}")

    def get_extractor(self):
        return list(self.extractor.values())[0]
    def get_parsers(self):
        return list(self.parsers.values())
    def get_validators(self):
        return list(self.validators.values())
    def get_bibformatter(self):
        return list(self.bibformatter.values())[0]
