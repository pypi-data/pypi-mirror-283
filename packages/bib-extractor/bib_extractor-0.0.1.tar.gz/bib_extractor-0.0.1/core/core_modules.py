from abc import ABC, abstractmethod
import logging
import json
import os
from typing import Generator
from typing import List, Union
from collections import OrderedDict
import shutil
import random

from merge_parsers import ParsersMerger
from multiprocess import Multiproc

# class MyException(Exception):
#     pass



class BaseABC(ABC):
    def __init__(self, opts):
        super().__init__()
        self.opts = opts
        # logger = logging.getLogger(__name__)
        # self.logger = logging.LoggerAdapter(logger, {'classname': self.__class__.__name__})
        self.logger = self.setup_logger(self.__class__.__name__)
        
    
    def setup_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        if not logger.handlers:
            formatter = logging.Formatter('%(asctime)s %(levelname)s [%(process)s]: %(name)s: %(classname)s: %(message)s')
            handler = logging.FileHandler(f"logs/{logger_name}.log", mode='w')
            handler.setFormatter(formatter)

            logger.addHandler(handler)
            print(f"setup logger for: {logger_name}")

        return logging.LoggerAdapter(logger, {'classname': logger_name})

    def test(self):
        return (f"It is {self.__class__.__name__}")
    
    def read_file_list(self, texts_list_path):
        """
        Читает файл со списком путей к файлам и возвращает список путей.
        
        :param texts_list_path: Путь к файлу со списком путей.
        :return: Список путей к файлам.
        """
        try:
            with open(texts_list_path, 'r') as file_list:
                return [line.strip() for line in file_list if line.strip()]
        except FileNotFoundError as e:
            self.logger.error(f"File '{texts_list_path}' not found: {e}")
            raise FileNotFoundError(e)
        except Exception as e:
            self.logger.error(f"Unexpected error while loading file with texts path: {e}")
            raise Exception(e)

    def get_text_content_from_file(self, file_path):
        """
        Открывает и выводит содержимое текстового файла на экран.
        
        :param file_path: Путь к текстовому файлу.
        """
        try:
            with open(file_path, 'r') as file:
                self.logger.debug(f"Text of file '{file_path}':")
                self.logger.debug(file.read())
                return file.read()
        except FileNotFoundError as e:
            self.logger.error(f"File '{file_path}' not found: {e}. Skip file")
        except Exception as e:
            self.logger.error(f"Unexpected error while loading text from file '{file_path}': {e}")
    
    def load_json_from_file(self, file_path):
        """
        Загружает JSON документ из файла и возвращает его содержимое.

        :param file_path: Путь к файлу .json
        :return: Содержимое JSON документа (словарь, список и т.д.)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.logger.info(f"Loaded JSON file '{file_path}'")
            return data
        except FileNotFoundError as e:
            self.logger.error(f"File '{file_path}' not found: {e}")
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to decode JSON from file '{file_path}': {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error while loading JSON file '{file_path}': {e}")
        return None
    
    def rewrite_json(self, file_path):
        """
        Пересоздает JSON файл.
        
        :param file_path: Путь к JSON файлу.
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            self.logger.info(f"Rewrited file '{file_path}'")
            pass
    
    def append_to_json(self, file_path, data):
        """
        Дозаписывает данные в JSON файл.
        
        :param file_path: Путь к JSON файлу.
        :param data: Данные для записи, должны быть в формате словаря с ключами 'file' и 'refs'.
        """
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []
        existing_data.append(data)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)
            self.logger.info(f"Added data in file '{file_path}'")
    
    def write_to_json(self, file_path, data):
        """
        Записывает данные в JSON файл.
        
        :param file_path: Путь к JSON файлу.
        :param data: Данные для записи
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            self.logger.info(f"Writed data in file '{file_path}'")
    
    
    def merge_validators_data(self, validators_data: List[dict]) -> dict:
        """
        На вход список из данных по одному документу (с одними и теми же ссылками) для каждого валидатора

        На выход - один словарь данных по документу с объединенными данными по валидности
        """

        if len(validators_data) == 0:
            self.logger.warning("Merge validators data have empty input data. return empty dict")
            return {}

        merged_data = validators_data[0].copy()
        merged_data['refs'] = []

        # Создаем словарь для быстрого доступа к ссылкам из первого валидатора
        ref_dicts = [{ref['ref']: ref for ref in validator['refs']} for validator in validators_data]

        # Собираем все уникальные ссылки из всех валидаторов, сохраняя порядок
        all_refs = OrderedDict()
        for ref_dict in ref_dicts:
            for ref in ref_dict.keys():
                all_refs[ref] = True

        for ref in all_refs.keys():
            merged_ref = {'ref': ref, 'valid': {}}
            for ref_dict in ref_dicts:
                if ref in ref_dict:
                    # Объединяем данные по валидности
                    merged_ref['valid'].update(ref_dict[ref]['valid'])
                    # Копируем все остальные поля, если они еще не добавлены
                    for key, value in ref_dict[ref].items():
                        if key not in merged_ref:
                            merged_ref[key] = value

            merged_data['refs'].append(merged_ref)

        return merged_data
    
    def merge_parsers_data(self, parsers_data: List[dict], validators_dict: dict, style_to_validator: dict) -> dict:
        """
        На вход список из данных по одному документу (с одними и теми же ссылками) для каждого парсера

        Согласование данных TODO: реализовать

        На выход - один словарь данных по документу с объединенными данными по валидности
        """
        PM = ParsersMerger()
        selected_style_to_parser = PM.merge_parsers_data(parsers_data)
        if len(selected_style_to_parser) == 1: # если стиль один - возвращаем результат
            selected_style = list(selected_style_to_parser.keys())[0]
            selected_parser = selected_style_to_parser[selected_style]
            merged_data = parsers_data[selected_parser]
            merged_data['style'] = selected_style
            self.logger.debug(f"After Merging parsers data Selected style: '{selected_style}'. Selected parser num '{selected_parser}'.")
            return merged_data
        # если стилей больше 1, то
        # 1 вариант - выбрать рандомно 
        # 2 вариант - отправить в валидаторы и оценить результаты по валидности ссылок

        # 1 вариант
        # selected_styles = list(selected_style_to_parser.keys())
        # selected_style = random.choice(selected_styles)
        # selected_parser = selected_style_to_parser[selected_style]
        # merged_data = parsers_data[selected_parser]
        # merged_data['style'] = selected_style
        # self.logger.debug(f"After Merging parsers data between {selected_styles} Randomly Selected style: '{selected_style}'. Selected parser num '{selected_parser}'.")
        # return merged_data
    
        # 2 вариант
        selected_styles = list(selected_style_to_parser.keys())
        selected_validators = [ validators_dict[style_to_validator[style]] for style in selected_styles ] 
        MP = Multiproc(self)
        merged_valid_data = MP.process_item_validators_mp(self.opts.proc_cnt, parsers_data[0], selected_validators)
        count_valid = {} # считаем статистику по валидности по стилям
        for ref_dict in merged_valid_data['refs']:
            valid = ref_dict['valid']
            for validator_name, val in valid.items():
                if val is True:
                    if validator_name in count_valid:
                        count_valid[validator_name] += 1
                    else:
                        count_valid[validator_name] = 1
        self.logger.debug(f"valid count values by style: {count_valid}")
        max_valid_count = max(count_valid.values())
        validator_to_style = {v: k for k, v in style_to_validator.items()}
        top_styles = [ validator_to_style[validator_name] for validator_name, votes in count_valid.items() if votes == max_valid_count ]
        if len(top_styles) == 1:
            selected_style = top_styles[0]
            selected_parser = selected_style_to_parser[selected_style]
            merged_data = parsers_data[selected_parser]
            merged_data['style'] = selected_style
            self.logger.debug(f"After Merging parsers data using Validators Selected style: '{selected_style}'. Selected parser num '{selected_parser}'.")
            return merged_data
        else:
            selected_styles = list(selected_style_to_parser.keys())
            selected_style = selected_styles[0] # в базовом случае возвращаем просто первый стиль
            selected_parser = selected_style_to_parser[selected_style]
            merged_data = parsers_data[selected_parser]
            merged_data['style'] = False  # "Not define"
            self.logger.debug(f"After Merging parsers The style is not define")
            return merged_data

        # ВРЕМЕННО пока берем просто первый парсер
        # merged_data = parsers_data[0] 

        # return merged_data

    def prepare_data(self, refs_data:List) -> List[dict]:
        """
        Возврат данных в формате
        
        [ 
            {
                'file': <name_file1>, 
                'refs': [ {'ref': ref1}, {'ref': ref2}, {'ref': ref3}, ... ]
            },
            {
                'file': <name_file2>, 
                'refs': [ {'ref': ref4}, {'ref': ref5}, {'ref': ref6}, ... ]
            }, 
            ...
        ]

        """
        self.logger.info(f"Preparing input data")
        prepared_refs_data = self._check_input_data_type(refs_data)
        return prepared_refs_data

    def _check_input_data_type(self, refs_data):
        first_item = refs_data[0]
        # определяем тип входного формата по первому элементу списка
        if isinstance(first_item, str):
            # 1 тип. Обработка биб.ссылки
            # конвертируем к типу 2 и обрабатываем как тип 2 (т.е. преобразовываем к типу 3)
            """
            [ 
                ref1, ref2, ref3, ... 
            ]
            """
            self.logger.info(f"Input refs file has type 1 - List of references - List[str]. Converting to type 4")
            refs_data = self._convert_to_type_2(refs_data)
            refs_data = self._convert_to_type_3(refs_data)
            refs_data = self._convert_to_type_4(refs_data)
        elif isinstance(first_item, list):
            # 2 тип. Обработка списка ( в нем каждый элемент списка это список из биб.ссылок)
            # то есть каждый док - это один список  из биб. ссылок
            # преобразовываем к типу 3
            """
            [ 
                [ ref1, ref2, ref3, ... ], 
                [ ref4, ref5, ref6, ... ], 
                ... 
            ]
            """
            self.logger.info(f"Input refs file has type 2 - List of List references - List[List[str]]. Converting to type 4")
            refs_data = self._convert_to_type_3(refs_data)
            refs_data = self._convert_to_type_4(refs_data)
        elif isinstance(first_item, dict):
            # 3 и 4 тип. Обработка словаря ( в нем в поле 'refs' список из биб.ссылок или список из словарей по одной биб.ссылке)
            
            if isinstance(first_item['refs'], list) and isinstance(first_item['refs'][0], str):
                # 3 тип. Обработка словаря ( в нем в поле 'refs' список из строковых биб.ссылок)
                """
                [ 
                    {'file': <name_file1>, 'refs': [ ref1, ref2, ref3, ... ] },
                    {'file': <name_file2>, 'refs': [ ref4, ref5, ref6, ... ] }, 
                    ...
                ]
                """
                self.logger.info(f"Input refs file has type 3 - List of Dict with references info - List[Dict[<'refs' is List[str]>]]. Converting to type 4")
                refs_data = self._convert_to_type_4(refs_data)
            elif isinstance(first_item['refs'], list) and isinstance(first_item['refs'][0], dict):
                # 4 тип. Обработка словаря ( в нем в поле 'refs' список из словарей по одной биб.ссылке)
                # также в этом словаре {'ref': ref2} может быть и информация с метаданными и т.д. Например: {'ref': ref2, 'meta': {...}, ...}
                """
                [ 
                    {'file': <name_file1>, 'refs': [ {'ref': ref1}, {'ref': ref2}, {'ref': ref3}, ... ] },
                    {'file': <name_file2>, 'refs': [ {'ref': ref4}, {'ref': ref5}, {'ref': ref6}, ... ] }, 
                    ...
                ]
                """
                self.logger.info(f"Input refs file has type 4 - List of Dict with references info - List[Dict[<'refs' is List[dict]>]]")
            else:
                raise ValueError("Unsupported item type")
        else:
            raise ValueError("Unsupported item type")
        self.logger.info(f"Refs file has type 4 - List of Dict with references info - List[Dict[<'refs' is List[dict]>]]")
        return refs_data
    
    def _convert_to_type_2(self, refs_data):
        self.logger.info(f"Func convert to type 2")
        return [refs_data]
    
    def _convert_to_type_3(self, refs_data):
        self.logger.info(f"Func convert to type 3")
        new_refs_data = []
        for num, refs in enumerate(refs_data, start=1):
            new_refs_data.append(
                {
                    'file': str(num),
                    'refs': refs
                }
            )
        return new_refs_data

    def _convert_to_type_4(self, refs_data):
        self.logger.info(f"Func convert to type 4")
        for data_item in refs_data:
            new_refs_item = []
            for ref in data_item['refs']:
                new_refs_item.append(
                    {
                        'ref': ref
                    }
                )
            data_item['refs'] = new_refs_item
        return refs_data
    


    
    def write_bib_file(self, filepath:str, bib_string):
        with open(filepath, 'w') as bibfile:
            bibfile.write(bib_string)


    def create_directory_for_bib_files(self, file_path, out_dir, recreate_dir):
        # Заменяем все символы '/' на '_' и убираем первый символ '_', если он есть
        new_directory_name = file_path.replace('/', '_').lstrip('_')
        new_directory_path = os.path.join(out_dir, new_directory_name)
        if not os.path.exists(new_directory_path):
            os.makedirs(new_directory_path)
            self.logger.info(f"Directory '{new_directory_path}' created.")
        elif recreate_dir:
            shutil.rmtree(new_directory_path)
            os.makedirs(new_directory_path)
            self.logger.info(f"Directory '{new_directory_path}' deleted and created again.")
        else:
            self.logger.info(f"Directory '{new_directory_path}' already exist.")
        return new_directory_path



class Extractor(BaseABC):
    @abstractmethod
    def extract(self, text:str):
        pass

    # def extract_list_old(self, texts_path:str) -> Generator[dict, None, None]:
    #     for text_path in self.read_file_list(texts_path):
    #         text = self.get_text_content_from_file(text_path)
    #         refs_lst = self.extract(text)
    #         yield {'file': text_path, 'refs': refs_lst}
    
    def extract_list(self, texts_in_string:list[str]) -> Generator[list, None, None]:
        for text in texts_in_string:
            refs_lst = self.extract(text)
            yield refs_lst


class Parser(BaseABC):
    def __init__(self, opts, confidence):
        super().__init__(opts)
        self.confidence = confidence

    @abstractmethod
    def parse(self, bib_ref:str) -> dict:
        # return {'metadata': {<parsed meta>}, "style_info": { <name of style>: <confidence from 0 to 100>, <name of style>: <confidence from 0 to 100>, ... } }
        pass
    def process_list(self, refs_data:List[dict]) -> Generator[dict, None, None]:
        """
        Если необходимо одним парсером обрабатывать данные
        Возврат данных в формате
        [
            {
                'file': <name_file1>, 
                'refs': [ 
                    { 'ref': ref1, 'meta': {'year': '2012', ...}, 'style': 'gost', 'confidence': 57 },
                    { 'ref': ref2, 'meta': {'year': '2011', ...}, 'style': 'gost', 'confidence': 89 }
                    { 'ref': ref3, 'meta': {'year': '2010', ...}, 'style': 'gost', 'confidence': 45 }
                    ... 
                ] 
            },
            {
                'file': <name_file2>, 
                'refs': [ 
                    { 'ref': ref4, 'meta': {'year': '2009', ...}, 'style': 'gost', 'confidence': 57 },
                    { 'ref': ref5, 'meta': {'year': '2008', ...}, 'style': 'mla', 'confidence': 89 }
                    { 'ref': ref6, 'meta': {'year': '2007', ...}, 'style': 'gost', 'confidence': 45 }
                    ... 
                ] 
            }
        ]
        """
        for rd in refs_data:
            yield self.process_dict_item(rd)
    
    def process_dict_item(self, refs_data_item:dict) -> dict:
        """
        Возврат данных в формате
        {
            'file': <name_file1>, 
            'refs': [ 
                { 'ref': ref1, 'meta': {'year': '2012', ...}, 'style': 'gost', 'confidence': 57 },
                { 'ref': ref2, 'meta': {'year': '2011', ...}, 'style': 'gost', 'confidence': 89 }
                { 'ref': ref3, 'meta': {'year': '2010', ...}, 'style': 'gost', 'confidence': 45 }
                ... 
            ] 
        }
        """
        new_refs = []
        for bib_ref in refs_data_item['refs']:
            new_ref = bib_ref
            parser_result = self.parse(bib_ref['ref'])
            for key, val in parser_result.items():
                new_ref[key] = val
            new_refs.append(new_ref)
        refs_data_item['refs'] = new_refs
        refs_data_item['_confidence'] = self.confidence
        return refs_data_item

    # TODO: добавить интерфейсы

class Validator(BaseABC):
    @abstractmethod
    def validate(self, bib_ref:str) -> dict:
        # {'<class validator name>': <True/False>}
        pass
    
    def process_list(self, refs_data:List[dict]) -> Generator[dict, None, None]:
        """
        Возврат данных в формате/ Для каждой ссылки будет валидность T/F по определенному стилю
        
        [ 
            {
                'file': <name_file1>, 
                'refs': [ 
                    { 'ref': ref1, 'valid': {'gost': True} },
                    { 'ref': ref2, 'valid': {'gost': False} },
                    { 'ref': ref3, 'valid': {'gost': False} },
                    ... 
                ] 
            },
            {
                'file': <name_file2>, 
                'refs': [ 
                    { 'ref': ref4, 'valid': {'gost': True} },
                    { 'ref': ref5, 'valid': {'gost': False} },
                    { 'ref': ref6, 'valid': {'gost': True} },
                    ... 
                ] 
            }, 
            ...
        ]

        если <name_file1> отсутсвтует, то пишем просто номер в списке

        """
        for rd in refs_data:
            yield self.process_dict_item(rd)
    
    def process_dict_item(self, refs_data_item:dict) -> dict:
        """
        Возврат данных в формате/ Для каждой ссылки будет валидность T/F по определенному стилю
        {
            'file': <name_file1>, 
            'refs': [ 
                { 'ref': ref1, 'valid': {'gost': True} },
                { 'ref': ref2, 'valid': {'gost': False} },
                { 'ref': ref3, 'valid': {'gost': False} },
                ... 
            ] 
        }
        """
        new_refs = []
        for bib_ref in refs_data_item['refs']:
            new_ref = bib_ref
            valid = self.validate(bib_ref['ref'])
            new_ref['valid'] = valid
            new_refs.append(new_ref)
        refs_data_item['refs'] = new_refs
        return refs_data_item

    

class BibFormatter(BaseABC):
    @abstractmethod
    def formate(self, meta:dict):
        pass
    def process_list(self, meta_path:str) -> Generator[str, None, None]:
        data = self.load_json_from_file(meta_path)
        for rd in data:
            yield self.process_dict_item(rd)

    # def extract_list(self, texts_path:str) -> Generator[dict, None, None]:
    #     for text_path in self.read_file_list(texts_path):
    #         text = self.get_text_content_from_file(text_path)
    #         refs_lst = self.extract(text)
    #         yield {'file': text_path, 'refs': refs_lst}
    # # TODO: добавить интерфейсы

    def process_dict_item(self, refs_data_item:dict) -> dict:
        """
        создаем директорию под файл
        формируем bib по мете
        записываем файл в директорию
        """
        new_refs = []
        for bib_ref in refs_data_item['refs']:
            new_ref = bib_ref
            bibtex_id, bibtex_string = self.formate(bib_ref['metadata'])
            bibtex = { 'bibtex_id': bibtex_id, 'bibtex_string': bibtex_string }
            new_ref['bibtex'] = bibtex
            new_refs.append(new_ref)
        refs_data_item['refs'] = new_refs
        return refs_data_item
    
        