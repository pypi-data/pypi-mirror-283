import multiprocessing as mp
from typing import List
import json


class Multiproc():
    def __init__(self, base_class) -> None:
        self.base_class = base_class


    def call_process_dict_item(self, module, item, *args):
        return module.process_dict_item(item, *args)


    def process_validators_mp(self, proc_cnt, data:List[dict], validators:List[object]):
        with mp.Pool(processes=proc_cnt) as pool:
            for item in data:
                validators_data = pool.starmap(self.call_process_dict_item, [(validator, item) for validator in validators])
                merged_valid_data = self.base_class.merge_validators_data(validators_data)
                yield merged_valid_data

    def process_item_validators_mp(self, proc_cnt, item:dict, validators:List[object]):
        with mp.Pool(processes=proc_cnt) as pool:
            validators_data = pool.starmap(self.call_process_dict_item, [(validator, item) for validator in validators])
            merged_valid_data = self.base_class.merge_validators_data(validators_data)
            return merged_valid_data
        


    def process_parsers_mp(self, proc_cnt, data:List[dict], parsers:List[object], validators_dict:dict, style_to_validator:dict):
        with mp.Pool(processes=proc_cnt) as pool:
            for item in data:
                parsers_data = pool.starmap(self.call_process_dict_item, [(parser, item) for parser in parsers])
                merged_parsed_data = self.base_class.merge_parsers_data(parsers_data, validators_dict, style_to_validator)
                yield merged_parsed_data


    def process_bibformate_mp(self, proc_cnt, data:List[dict], bibformatter:object):
        with mp.Pool(processes=proc_cnt) as pool:
            bibformatter_data = pool.starmap(self.call_process_dict_item, [(bibformatter, item) for item in data])
            return bibformatter_data
