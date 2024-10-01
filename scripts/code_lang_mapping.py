import json
# def tokens_mapping():
#     language_countries_mapping = {
#         # "ar": ["Saudi Arabia", "Iraq", "Egypt", "Syria", "Yemen", "Sudan", "Tunisia", "Jordan", "United Arab Emirates", "Lebanon", "Libya", "Palestine", "Oman", "Kuwait", "Qatar", "Bahrain", "Algeria", "Morocco"],
#         "az": ["Azerbaijan"],
#         "be": ["Belarus"],
#         "bg": ["Bulgaria"],
#         "bs": ["Bosnia and Herzegovina"],
#         "ca": ["Spain"],
#         "cs": ["Czech Republic"],
#         "cy": ["United Kingdom (Wales)"],
#         "da": ["Denmark"],
#         # "de": ["Germany", "Austria", "Switzerland", "Belgium", "Luxembourg", "Liechtenstein"],
#         "de": ["Germany"],
#         # "el": ["Greece", "Cyprus"],
#         "el": ["Greece"],
#         # "en": ["United Kingdom", "Ireland"],
#         "en": ["United Kingdom"],
#         "es": ["Spain"],
#         "et": ["Estonia"],
#         "eu": ["Spain"],
#         # "fa": ["Iran", "Afghanistan", "Tajikistan"],
#         "fi": ["Finland"],
#         # "fr": ["France", "Belgium", "Switzerland", "Luxembourg", "Monaco"],
#         "fr": ["France"],
#         "ga": ["Ireland"],
#         "gl": ["Spain"],
#         "he": ["Israel"],
#         "hr": ["Croatia"],
#         "hu": ["Hungary"],
#         "hy": ["Armenia"],
#         "is": ["Iceland"],
#         # "it": ["Italy", "Switzerland", "San Marino", "Vatican City"],
#         "it": ["Italy"],
#         "ka": ["Georgia"],
#         "kk": ["Kazakhstan"],
#         # "ku": ["Turkey", "Iran", "Iraq", "Syria"],
#         "ku": ["Turkey"],
#         "lt": ["Lithuania"],
#         "lv": ["Latvia"],
#         "mk": ["North Macedonia"],
#         # "nl": ["Netherlands", "Belgium"],
#         "nl": ["Netherlands"],
#         "no": ["Norway"],
#         "pl": ["Poland"],
#         "pt": ["Portugal"],
#         # "ro": ["Romania", "Moldova"],
#         "ro": ["Romania"],
#         # "ru": ["Russia", "Belarus", "Kazakhstan", "Kyrgyzstan"],
#         "sk": ["Slovakia"],
#         "sl": ["Slovenia"],
#         "sq": ["Albania", "Kosovo"],
#         # "sr": ["Serbia", "Montenegro", "Bosnia and Herzegovina", "Kosovo"],
#         "sr": ["Serbia"],
#         "sv": ["Sweden"],
#         "tr": ["Turkey"],
#         "uk": ["Ukraine"],
#         "ur": ["Pakistan"]
#     }
#     with open("languages_countries_mapping_single.json", "w") as f:
#         json.dump(language_countries_mapping, f)
#     return
#
#
# tokens_mapping()

language_alphabets = {
    "en": "abcdefghijklmnopqrstuvwxyz",
    "de": "abcdefghijklmnopqrstuvwxyzäöüß",
    "sv": "abcdefghijklmnopqrstuvwxyzåäö",
    "da": "abcdefghijklmnopqrstuvwxyzæøå",
    "no": "abcdefghijklmnopqrstuvwxyzæøå",
    "nl": "abcdefghijklmnopqrstuvwxyz",
    "is": "aábdðeéfghiíjklmnoóprstuúvxyýþæö",
    "pl": "aąbcćdeęfghijklłmnńoóprsśtuwyzźż",
    "uk": "абвгґдежзийіїклмнопрстуфхцчшщьюяє",
    "cs": "aábcčdďeéěfghiíjklmnňoópqrřsštťuúůvyýzž",
    "be": "абвгдежзийклмнопрстуўфхцчшыьэюя",
    "sk": "aáäbcčdďeéfghiíjklĺľmnňoóôprsštťuúvwxyýzž",
    "sl": "abcčdefghijklmnoprsštuvzž",
    "bg": "абвгдежзийклмнопрстуфхцчшщъьюя",
    "mk": "абвгдѓежзийклмнопрстуфхцчшщјљњќџ",
    "fr": "abcdefghijklmnopqrstuvwxyzàâæçéèêëîïôœùûüÿ",
    "it": "abcdefghijklmnopqrstuvwxyz",
    "es": "abcdefghijklmnopqrstuvwxyzáéíñóúü",
    "pt": "abcdefghijklmnopqrstuvwxyzáâãàçéêíóôõú",
    "ro": "abcdefghijklmnopqrstuvwxyzăâîșț",
    "hu": "aábcdeéfghiíjklmnoóöőpqrstuúüűvwxyz",
    "fi": "abcdefghijklmnopqrstuvwxyzåäö",
    "et": "abcdefghijklmnopqrstuvwxyzäöõüšž",
    "cy": "abcdefghijklmnopqrstuvwxyz",
    "ga": "abcdefghijklmnopqrstuvwxyz",
    "tr": "abcçdefgğhıijklmnoöprsştuüvyz",
    "lt": "aąbcčdeęėfghiįyjklmnoprsštuųūvzž",
    "lv": "aābcčdeēfgģhiījkķlļmnņoprsštuūvzž",
    "sq": "abcdefghijklmnopqrstuvwxyz",
    "el": "αβγδεζηθικλμνξοπρστυφχψω",
    "ka": "აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ",
    # "Armenian": "աբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքևօֆ"
}
#
# language_alphabet_in_tokenizer = {
#     "en": [0, len(language_alphabets["en"])],
#     "de": [0, len(language_alphabets["de"])],
#     "sv": [0, len(language_alphabets["sv"])],
#     "da": [0, len(language_alphabets["da"])],
#     "no": [0, len(language_alphabets["no"])],
#     "nl": [0, len(language_alphabets["nl"])],
#     "is": [0, len(language_alphabets["is"])],
#     "pl": [0, len(language_alphabets["pl"])],
#     "uk": [0, len(language_alphabets["uk"])],
#     "cs": [0, len(language_alphabets["cs"])],
#     "be": [0, len(language_alphabets["be"])],
#     "sk": [0, len(language_alphabets["sk"])],
#     "sl": [0, len(language_alphabets["sl"])],
#     "bg": [0, len(language_alphabets["bg"])],
#     "mk": [0, len(language_alphabets["mk"])],
#     "fr": [0, len(language_alphabets["fr"])],
#     "it": [0, len(language_alphabets["it"])],
#     "es": [0, len(language_alphabets["es"])],
#     "pt": [0, len(language_alphabets["pt"])],
#     "ro": [0, len(language_alphabets["ro"])],
#     "hu": [0, len(language_alphabets["hu"])],
#     "fi": [0, len(language_alphabets["fi"])],
#     "et": [0, len(language_alphabets["et"])],
#     "cy": [0, len(language_alphabets["cy"])],
#     "ga": [0, len(language_alphabets["ga"])],
#     "tr": [0, len(language_alphabets["tr"])],
#     "lt": [0, len(language_alphabets["lt"])],
#     "lv": [0, len(language_alphabets["lv"])],
#     "sq": [0, len(language_alphabets["sq"])],
#     "el": [0, len(language_alphabets["el"])],
#     "ka": [0, len(language_alphabets["ka"])],
# }


def load_jsons():
    with open("languages_countries_mapping.json") as lang_cont:
        lang_cont_mapp = json.load(lang_cont)

    with open("tokens_countrycode_mapping.json") as tok_cont:
        tok_cont_mapp = json.load(tok_cont)

    with open("lang_code_to_alphabet_second_metric.json") as alphabets:
        alphabets_mapp = json.load(alphabets)

    with open("countrycode_to_countries_second_metric.json") as count_to_count:
        count_to_count_mapp = json.load(count_to_count)

    with open("core_tokens.json") as core_tokens:
        core_toks = json.load(core_tokens)

    if lang_cont_mapp:
        print("lang_cont_mapp_OK!")
    if tok_cont_mapp:
        print("tok_cont_mapp_OK!")

    return lang_cont_mapp, tok_cont_mapp, alphabets_mapp, count_to_count_mapp, core_toks
