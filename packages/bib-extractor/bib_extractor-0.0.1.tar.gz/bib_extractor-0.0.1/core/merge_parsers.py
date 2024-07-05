import json
from collections import defaultdict
import logging

class LangId:
    RU = 0
    EN = 1
    UNDEFINED = 15


def lang_of_letter(cp):
    if 0x400 <= cp <= 0x4FF:
        return LangId.RU
    if 0x41 <= cp <= 0x5A or 0x61 <= cp <= 0x7A:
        return LangId.EN
    return LangId.UNDEFINED


def lang_of_text(s):
    lang_count = defaultdict(int)
    for char in s:
        lang_count[lang_of_letter(ord(char))] += 1
    return max(lang_count, key=lang_count.get)


def get_lang_of_bibref(bibref):
    res = lang_of_text(bibref)
    if res != 0: # english
        return 'eng'
    else: # russian
        return 'rus'




class ParsersMerger():
    def __init__(self):
        self.approximately_russian_style = {'style5','style4'} # здесь должны быть названия ГОСТов
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
    
    def print_json(self, data):
        self.logger.debug(json.dumps(data, indent=4, ensure_ascii=False))


##################################################

    def count_votes(self, window_refs, confidence_by_parser):
        # 1. считаем голоса каждого стиля в рамках каждого парсера (где уверенность > 70)
        style_votes = []

        for index_of_parser, parser_refs in enumerate(window_refs):
            parser_votes = {}
            for ref in parser_refs:
                for style, confidence in ref.get("style_info", {}).items():
                    if confidence > confidence_by_parser[index_of_parser]:
                        if style not in parser_votes:
                            parser_votes[style] = 0
                        parser_votes[style] += 1
            style_votes.append(parser_votes)
        return style_votes

    def filter_votes(self, style_votes):
        """
        Filter styles to keep only those with the maximum number of votes.
        
        :param style_votes: Dictionary of styles with their corresponding votes.
        :return: Dictionary of styles with the maximum number of votes.
        """
        # 2. оставляем только максимальное количество голосов в каждом из парсеров
        style_votes_only_max = []
        for i, votes in enumerate(style_votes):
            if votes:
                max_vote = max(votes.values())
                max_votes = {style: votes_elem for style, votes_elem in votes.items() if votes_elem == max_vote}
                # print("max_votes")
                # print_json(max_votes)
                style_votes_only_max.append(max_votes)
        return style_votes_only_max

    def select_max_votes_styles(self, style_votes_only_max):
        """
        Select the styles with the maximum number of votes from a list of style votes dictionaries.
        
        :param style_votes_only_max: List of dictionaries with styles and their corresponding votes.
        :return: Dictionary with index as key and the corresponding max style votes dictionary as value.
        """
        # 3. сравниваем голоса между парсерами и выбираем стиль + записываем номер парсера
        if not style_votes_only_max:
            return {}

        max_votes = 0
        max_votes_styles = {}

        for index, style_votes in enumerate(style_votes_only_max, start=0):
            current_max_votes = max(style_votes.values())
            if current_max_votes > max_votes:
                max_votes = current_max_votes
                max_votes_styles = {style: index for style, votes in style_votes.items() if votes == max_votes}
            elif current_max_votes == max_votes:
                for style, votes in style_votes.items():
                    if votes == max_votes:
                        max_votes_styles[style] = index

        return max_votes_styles

    def update_aggregated_results(self, style_to_parser, votes_by_style, result):
        """
        Update aggregated results with a new result from select_max_votes_styles.
        
        :param style_to_parser: Dictionary with current mapping of styles to parser indices.
        :param votes_by_style: Dictionary with current counts of votes by style.
        :param result: New result from select_max_votes_styles to be aggregated.
        """
        for style, parser_index in result.items():
            style_to_parser[style] = parser_index
            if style in votes_by_style:
                votes_by_style[style] += 1
            else:
                votes_by_style[style] = 1

    def select_top_styles(self, votes_by_style, style_to_parser):
        """
        Select the styles with the maximum number of votes.

        :param votes_by_style: Dictionary with counts of votes by style.
        :param style_to_parser: Dictionary with current mapping of styles to parser indices.
        :return: Dictionary with the style(s) having the maximum votes and their corresponding parser indices.
        """
        if not votes_by_style:
            return {}

        max_votes = max(votes_by_style.values())
        top_styles = {style: style_to_parser[style] for style, votes in votes_by_style.items() if votes == max_votes}

        return top_styles


    def select_style_by_lang(self, parsers_data, top_styles_to_parser):
        """
        1. проверка на стили, среди которых выбираем.
        - если все в списке approximately_russian_style, то возвращаем "не определено"
        - если всех нет в списке approximately_russian_style, то тоже возвращаем "не определено"
        - если среди стилей один встречается русский, а остальные другого формата - работаем с данными
        2. определяем язык каждой ссылки (достаточно взять ссылки из первого парсера)
        3. считаем количество вхождений rus и eng. 
        4. 
        - если в п.1 был один русский и количество rus > eng, то результат - "определен русский стиль и возвращаем его"

        """
        #  1. проверка на стили, среди которых выбираем
        top_styles = set(top_styles_to_parser.keys())
        top_styles_rus = top_styles.intersection(self.approximately_russian_style)
        top_styles_rus = list(top_styles_rus)

        SEARCH_RUS = True if len(top_styles_rus) == 1 else False
        SEARCH_RUS_STYLE = top_styles_rus[0] if SEARCH_RUS else False # запоминаем название стиля, если оно одно

        if SEARCH_RUS is False:
            # Стиль этим методом определить невозможно
            return False

        # 2. определяем язык каждой ссылки (достаточно взять ссылки из первого парсера)
        refs_dict = parsers_data[0]['refs']
        refs_str = [ref_dict['ref'] for ref_dict in refs_dict]
        langs = [get_lang_of_bibref(ref) for ref in refs_str]
        rus_count = langs.count('rus')
        eng_count = langs.count('eng')
        if rus_count > eng_count and SEARCH_RUS:
            # русских больше и искали русский - возвращаем парсер соответствующий этому русскому стилю
            self.logger.debug(f'RUS more than ENG. Select {SEARCH_RUS_STYLE}')
            return { SEARCH_RUS_STYLE: top_styles_to_parser[SEARCH_RUS_STYLE]}
        else:
            self.logger.debug ('RUS no more than ENG. Style is not selected')
            # Стиль этим методом определить невозможно
            return False




    def process_window(self, window_refs, confidence_by_parser):
        """
        Process a window of bibliographic references.
        
        :param window_refs: List of references within the current window from each parser.
        :param confidence_by_parser: The confidence threshold for each parsers in window_refs.
        :return: The selected parser index based on the maximum votes.
        """
        # 1. считаем голоса каждого стиля в рамках каждого парсера (где уверенность > 70)
        style_votes = self.count_votes(window_refs, confidence_by_parser)
        # print(f"all votes")
        # print_json(style_votes)

        # 2. оставляем только максимальное количество голосов в каждом из парсеров
        style_votes_only_max = self.filter_votes(style_votes)
        # print(f"only max")
        # print_json(style_votes_only_max)

        # 3. сравниваем голоса между парсерами и выбираем наибольший + записываем номер парсера
        parser_with_max_style = self.select_max_votes_styles(style_votes_only_max)
        self.logger.debug(f"num parser and max style")
        self.print_json(parser_with_max_style)

        return parser_with_max_style


    def merge_parsers_data(self, parsers_data, window_size=5, step_size=1, retry_mode=False):
        """
        Merge bibliographic references parsed by multiple parsers.

        :param parsers_data: List of dictionaries containing parsed data from each parser.
        :param window_size: The size of the sliding window to process references.
        :param step_size: The step size for the sliding window.
        :param retry_mode: флаг для определения - повторно вызывается функция (т.е. рекурсивно) или нет
        :return: Merged bibliographic references (placeholder for now).
        """
        
        self.logger.debug(f"#########################################")
        if retry_mode:
            self.logger.debug(f"Start merge parsers again by all bib refs")
        else:
            self.logger.debug(f"Start merge parsers first time with sliding window")
        self.logger.debug(f"#########################################")

        refs_by_parser = []
        confidence_by_parser = []
        
        assert isinstance(parsers_data, list), "data by parsers for merging must be list"
        # Extract all references from each parser's data
        for parser_data in parsers_data:
            refs_by_parser.append(parser_data["refs"])
            confidence_by_parser.append(parser_data["_confidence"])

                
        assert all(len(refs) == len(refs_by_parser[0]) for refs in refs_by_parser), "All parsers must have the same number of references."    
        
        num_refs = len(refs_by_parser[0])
        if window_size > num_refs:
            window_size = num_refs

        style_to_parser = {}
        votes_by_style = {}

        # Process the references using a sliding window approach
        for i in range(0, num_refs - window_size + 1, step_size):
            # Create a window of references for each parser
            window_refs = [refs[i:i + window_size] for refs in refs_by_parser]
            parser_with_max_style = self.process_window(window_refs, confidence_by_parser)
            # обновляем словари: 1 - статистика для соответствия стиля и парсера, 2 - голоса за каждый стиль
            self.update_aggregated_results(style_to_parser, votes_by_style, parser_with_max_style)

        self.logger.debug("votes_by_style")
        self.print_json(votes_by_style)

        top_styles_to_parser = self.select_top_styles(votes_by_style, style_to_parser)
        self.logger.debug("top_styles_to_parser")
        self.print_json(top_styles_to_parser)
        
        merged_data = {}

        if len(top_styles_to_parser) == 1:
            # значит один стиль опредилили - возвращаем данные по нужному номеру парсера
            return top_styles_to_parser
        elif len(top_styles_to_parser) > 1:
            # Если стилей с одинаковыми голосами несколько
            if retry_mode:
                return False
            # 1. пересчет по всему документа (без окна)
            selected_style_to_parser_by_retry_mode = self.merge_parsers_data(parsers_data, window_size=num_refs, retry_mode=True)
            if selected_style_to_parser_by_retry_mode is not False:
                # пересчет по полному документу успешен - вернулись данные по стилю
                self.logger.debug(f"retry mode return successfully data")
                return selected_style_to_parser_by_retry_mode
            # значит рекурсивный вызов с пересчетом по полному документу не увенчался успехом, продолжаем поиск
            self.logger.debug(f"retry mode return not success. continue search by lang")

            # 2. по кирилице - гост или не гост. Надо для этого задать параметр для названий стилей, которые соответствуют ГОСТу
            selected_style_to_parser_by_lang = self.select_style_by_lang(parsers_data, top_styles_to_parser)
            if selected_style_to_parser_by_lang:
                # вернули результат по парсеру
                self.logger.debug(f"select style by lang return successfully data")
                return selected_style_to_parser_by_lang
            # Не вернулась дата -> п.3
            self.logger.debug(f"select style by lang mode return not success. continue search after validate")
            
            # 3. в валидаторы отправляем и считаем где больше TRUE  - тот стиль и выбираем
            # то есть оставляем в merged_data  несколько результатов парсеров и метку в какие валидаторы отправлять 
            # а уже потом в валидаторе добавить логику проверки
            return top_styles_to_parser # возвращаем просто стили с максимальными голосами
        else:
            self.logger.debug(f"Стиль цитирования неизвестен - len(top_styles_to_parser) < 1")
            pass #error
        
        
        return ''






###################################################

# with open("./merge_parsers/parsers_data.json", "r") as f:
#     parsers_data = json.load(f)
#     print(f"loaded file with results of {len(parsers_data)} parsers")

# PM = ParsersMerger()
# result = PM.merge_parsers_data(parsers_data, window_size=10, step_size=1)
# # print(json.dumps(result, indent=4, ensure_ascii=False))
# with open("./merge_parsers/result_data.json", "w") as f:
#     json.dump(result, f, indent=4, ensure_ascii=False)