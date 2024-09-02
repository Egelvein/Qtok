from code_lang_mapping import load_jsons
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("token_analysis")

language_code_country_mapping, token_code_country_mapping, alphabets_mapping_2, language_code_country_mapping_2, core_tokens = load_jsons()

class TokenizerAlphabetViewer:
    def __init__(self, tokenizer_vocab):
        self.__tokens = [token for token in tokenizer_vocab if len(token) == 1]

    def get_tokens(self):
        return self.__tokens

    def get_alphabet_view(self):
        result = {
            "Country": list(),
            "Number of tokens": list()
        }

        for country_code, alphabet in alphabets_mapping_2.items():
            count = sum(1 for token in self.__tokens if token in alphabet)
            if count > 0:
                if country_code in language_code_country_mapping_2.keys():
                    countries = language_code_country_mapping_2[country_code]
                else:
                    continue
                for country in countries:
                    result["Country"].append(country)
                    result["Number of tokens"].append(count)
                # result["Country"].extend(language_code_country_mapping_2.get(country_code, []))
                # result["Number of tokens"].append(count)
        return result