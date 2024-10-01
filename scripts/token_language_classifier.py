import langid
from code_lang_mapping import language_alphabets


class TokenLanguageClassifier:
    # languages: list = list()
    language_codes: list = ["bs", "hr", "mk", "sr", "en", "de", "sv", "da", "no", "nl", "is", "pl", "uk", "cs", "be",
                            "sk", "sl", "bg", "mk", "fr", "it", "es", "pt", "ro", "hu", "fi", "et", "cy", "ga", "tr",
                            "lt", "lv", "sq", "el", "ka"]

    def __init__(self, token):
        self.token = token
        self.__token_length = len(token)
        self.__languages = list()
        self.__number_of_top_languages = 0
        self.result_languages: list = list()

    def display_token_length(self):
        return self.__token_length

    def display_languages(self):
        return self.__languages

    def __token_classification(self):
        ranked: list = langid.rank(self.token)
        ranked_cleared: list = list()
        for item in ranked:
            if item[0] in self.language_codes:
                ranked_cleared.append(item)
        ranked_cleared = ranked_cleared[:self.number_of_top_languages]
        language_code_token: set = set()
        for item in ranked_cleared:
            code = item[0]
            language_code_token.add(code)
        self.__languages = list(language_code_token)

    def __clear_languages(self):
        cleared_detected_langs: set = set()
        for detected_lang in self.__languages:
            correct_chars = 0
            incorrect_chars = 0
            for char in self.token:
                if detected_lang not in language_alphabets:
                    continue
                if char in language_alphabets[detected_lang] or char in language_alphabets[detected_lang].upper():
                    correct_chars += 1
                else:
                    incorrect_chars += 1
            if correct_chars >= incorrect_chars:
                cleared_detected_langs.add(detected_lang)
        self.result_languages = list(cleared_detected_langs)

    def __number_of_top_languages_update(self):
        if self.__token_length == 2:
            self.number_of_top_languages = 4
        elif 3 <= self.__token_length <= 4:
            self.number_of_top_languages = 3
        elif 4 < self.__token_length < 6:
            self.number_of_top_languages = 2
        elif self.__token_length >= 6:
            self.number_of_top_languages = 1

    def classify(self):
        self.__number_of_top_languages_update()
        self.__token_classification()
        self.__clear_languages()
        return self.result_languages
