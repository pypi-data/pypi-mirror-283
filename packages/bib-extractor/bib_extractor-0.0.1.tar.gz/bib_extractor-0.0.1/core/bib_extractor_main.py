import argparse
import logging
from system_loader import SystemLoader, SystemNotLoadException
from core_modules import BaseABC
import time 
import copy
import json
from multiprocess import Multiproc


class BibExtractor():
    def __init__(self, opts:dict=None):
        self._set_opts(opts)

        self.system_loader = SystemLoader(self.opts)
        self.base_class = BaseABC(self.opts)
        self.MP = Multiproc(self.base_class)

    def _set_opts(self, opts):
        if isinstance(opts, argparse.Namespace):
            self._set_opts_from_cli(opts)
        elif isinstance(opts, dict):
            self._set_opts_from_dict(opts)

    def _set_opts_from_dict(self, new_opts):
        # при вызове функций как интерфейс (обычный словарь)
        default_opts = {
            'config': './config.json',
            'verbose': 'False',
            'proc_cnt': 2,
            'log': 'common_log.log'
        }
        opts = argparse.Namespace(**default_opts)
        for key, value in new_opts.items():
            setattr(opts, key, value)
        self.opts = opts
    
    def _set_opts_from_cli(self, new_opts):
        # при вызове функций из CLI (уже объект <class 'argparse.Namespace'>)
        self.opts = new_opts

    def pipeline(self, texts_in_string, texts_filenames = False):
        self.base_class.logger.info(f"Pipeline mode")

        # извлекаем биб.ссылки
        bibrefs_lists_gen = self.extract(texts_in_string)
        for index, refs_lst in enumerate(bibrefs_lists_gen):
            # получаем ссылки по одному тексту
            # если переданы названия текстов, то присваиваем их
            refs_res = [ {'file': texts_filenames[index], 'refs': refs_lst} ] if texts_filenames else refs_lst

            # парсим данные в одном или нескольких парсерах + согласование
            merged_parsed_data_gen = self.parse(refs_res)
            merged_parsed_data =  next(merged_parsed_data_gen) # т.к. в генераторе будет только один элемент, т.к. обрабатываем по одному
            style_of_text = merged_parsed_data['style']
            if style_of_text is False:
                # парсер не определил стиль - возвращаем эти данные распарсенные пользователю
                self.base_class.logger.info(f"Doc has not style - return only parsed data without style")
                yield merged_parsed_data
            # стиль определен - отправляем в валидатор
            selected_validator = self.system_loader.validators[self.system_loader.style_to_validator[style_of_text]]
            valid_data = self.MP.process_item_validators_mp(self.opts.proc_cnt, merged_parsed_data, [selected_validator] )
            # в словаре по документу есть стиль и валидность t/f
            yield valid_data
        
    
    def extract(self, texts_in_string):
        """
        на вход список из текстов (уже преобразованных в обычную строку)
        """
        self.base_class.logger.info(f"Extractor mode")
        extractor = self.system_loader.get_extractor()
        bibrefs_lists_gen = extractor.extract_list(texts_in_string)
        return bibrefs_lists_gen


    def parse(self, refs_data):
        """
        на вход json список из биб реф (Пример - input_test{1,2,3,4}.json)
        """
        self.base_class.logger.info(f"Parser mode")
        parsers = self.system_loader.get_parsers()
        validators_dict = self.system_loader.validators
        self.base_class.logger.info(f"Len parsers = {len(parsers)}")
        prepared_data = self.base_class.prepare_data(refs_data)
        merged_parsed_data_gen = self.MP.process_parsers_mp(self.opts.proc_cnt, prepared_data, parsers, validators_dict, self.system_loader.style_to_validator)
        return merged_parsed_data_gen

    def validate(self, refs_data):
        """
        на вход json список из биб реф (Пример - input_test{1,2,3,4}.json)
        """
        self.base_class.logger.info(f"Validator mode")
        validators = self.system_loader.get_validators()
        prepared_data = self.base_class.prepare_data(refs_data)
        merged_valid_data_gen = self.MP.process_validators_mp(self.opts.proc_cnt, prepared_data, validators)
        return merged_valid_data_gen
    
    def bibformate(self, meta_data):
        self.base_class.logger.info(f"BibFormatter mode")
        bibformatter = self.system_loader.get_bibformatter()
        # load_data = base_class.load_json_from_file(opts.meta_file)
        prepared_data = self.base_class.prepare_data(meta_data)
        bibformatter_data = self.MP.process_bibformate_mp(self.opts.proc_cnt, prepared_data, bibformatter)
        return bibformatter_data
    