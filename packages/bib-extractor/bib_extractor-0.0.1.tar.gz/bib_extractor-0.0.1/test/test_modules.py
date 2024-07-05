import random
from core.core_modules import Extractor, Validator, Parser, BibFormatter

class TestExtractor(Extractor):
    def __init__(self, opts):
        super().__init__(opts)
        # загружаем 2 тысячи готовых биб ссылок и выдаем рандомные (от 4 до 15) при вызове функции
        self.test_bib_refs = self.load_json_from_file('./test/test_list_bib_refs.json')

    def extract(self, text=''):
        
        # print(f"len test bib refs {len(test_bib_refs)}")
        num_links = random.randint(4, 15)
        random_links = random.sample(self.test_bib_refs, num_links)

        bib_refs = random_links
        # возвращаем список из биб ссылок
        return bib_refs


class TestParser1(Parser):
    def __init__(self, opts, confidence):
        super().__init__(opts, confidence)
        # загружаем словарь метаданных для каждой из тестовых ссылок
        self.test_bibref2meta = self.load_json_from_file('./test/test_parser_bibref2meta.json')
        self.list_of_styles = ['style1', 'style2', 'style3']
        self.probabilities_of_styles = [0.3, 0.5, 0.2]


    def parse(self, bib_ref):
        # на вход одна биб ссылка в виде текста

        # парсинг
        metadata = {}

        metadata = self.test_bibref2meta[bib_ref]

        # выбираем количество стилей от 1 до 2
        num_styles = random.randint(1, 2)

        # рандомно выбираем стиль, но есть вероятности выбора
        selected_style = random.choices(self.list_of_styles, weights=self.probabilities_of_styles, k=num_styles)

        style_info = {
            style: random.randint(60, 100) for style in selected_style
        }

        # на выход словарь {стиль, уверенность, мета}
        result = {
            "style_info": style_info,
            "metadata": metadata
        }
        self.logger.info(f"Parsed bib ref: {result}.")

        return result

class TestParser2(TestParser1):
    def __init__(self, opts, confidence):
        super().__init__(opts, confidence)
        self.list_of_styles = ['style4', 'style5']
        self.probabilities_of_styles = [0.3, 0.7]
        



class TestValidator1(Validator):
    def validate(self, bib_ref):        
        valid = random.choice([True, False]) # True / False
        self.logger.info(f"Valid: '{valid}'. Validate the bib ref: '{bib_ref}'")
        # return {'ref': bib_ref, 'style': self.__class__.__name__, 'valid': valid}
        return {self.__class__.__name__: valid}

class TestValidator2(TestValidator1):
    def __init__(self, opts):
        super().__init__(opts)

class TestValidator3(TestValidator1):
    def __init__(self, opts):
        super().__init__(opts)

class TestValidator4(TestValidator1):
    def __init__(self, opts):
        super().__init__(opts)

class TestValidator5(TestValidator1):
    def __init__(self, opts):
        super().__init__(opts)


class TestFormatter(BibFormatter):
    def formate(self, meta):
        return self.create_bib_entry(meta)
        
    def create_bib_entry(self,metadata):
        bib_entry = f"@{metadata['ENTRYTYPE']}{{{metadata['ID']},\n"
        for key, value in metadata.items():
            if key not in ['ENTRYTYPE', 'ID']:
                bib_entry += f"    {key}={{{value}}},\n"
        bib_entry = bib_entry.rstrip(',\n') + "\n}"
        return metadata['ID'], bib_entry


if __name__ == "__main__":

    extractor = TestExtractor()
    print(extractor.extract())