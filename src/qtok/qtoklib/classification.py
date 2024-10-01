import unicodedata
from collections import defaultdict
from .tokenizer import char_to_byte

LANGUAGES = ['ADLAM', 'CHAKMA', 'OL', 'BAMUM', 'OGHAM', 'BOPOMOFO', 'COPTIC', 'RUNIC', 'HALFWIDTH',
                    'MODI', 'KAITHI', 'LEPCHA', 'SHAVIAN', 'LIMBU', 'BATAK', 'PHOENICIAN', 'GLAGOLITIC', 'MANDAIC', 'BALINESE', 'SAMARITAN', 'PHAGS-PA', 'OLD', 'BLACK-LETTER', 'SUNDANESE', 'INSCRIPTIONAL', 'LISU', 'CHAM', 'TAGALOG', 'DESERET', 'TAGBANWA',
                    'BUGINESE', 'THAANA', 'MONGOLIAN', 'DINGBAT', 'JAVANESE', 'EGYPTIAN', 'GEORGIAN', "NKO", 'TIFINAGH', "GURMUKHI", "BENGALI", "SINHALA", "ORIYA", "TAI", "KANGXI", 'CANADIAN', "CHEROKEE", "LAO", 'TELUGU', 'SYRIAC', "TAMIL", "BRAILLE", "ETHIOPIC", "MYANMAR", "HEBREW", "ARABIC", "TIBETAN", "HIRAGANA", "CYRILLIC", "GREEK", "CJK", "LATIN", "KATAKANA", "KHMER", 'THAI', 'ARMENIAN',
                    'YI', 'HANGUL', 'GOTHIC', 'MALAYALAM', 'DEVANAGARI', "GUJARATI", 'KANNADA', 'MEETEI', 'ARABIC-INDIC']


def get_classification(token2hits_tok):

    token2meta = {}
    category2tokens = {
        "char": defaultdict(list),
        "spaced": defaultdict(list),
        "inner": defaultdict(list),
        "control_words": defaultdict(list),
        "pure_unicode": defaultdict(list),
        "unicode_flanks": defaultdict(list),
        "code": defaultdict(list),
        "control_token": defaultdict(list),
        "unicode_flanks": defaultdict(list),
    }

    for token in token2hits_tok:
        if len(token) == 1:
            if token in char_to_byte:
                token2meta[token] = ("pure_unicode", "pure_unicode")
                category2tokens["pure_unicode"]["pure_unicode"].append(token)
                continue
            try:
                ut = [unicodedata.name(x).split() for x in token]
            except:
                token2meta[token] = ("char_errors",  "char_errors")
                category2tokens["char"]["errors"].append(token)
                continue
            if ut[0][0] in LANGUAGES:
                token2meta[token] = ("char_alpha",  ut[0][0])
                category2tokens["char"][("char_alpha",  ut[0][0])].append(token)
                continue
            else:
                token2meta[token] = ("char_other",  "char_other")
                category2tokens["char"]["other"].append(token)
                continue
        else:
            if token[0] == " ":
                try:
                    ut = [unicodedata.name(x).split() for x in token]
                except:
                    token2meta[token] = ("spaced_errors", "spaced_errors")
                    category2tokens["spaced"]["errors"].append(token)
                    continue
                hits = list(set([unicodedata.name(x).split()[0] for x in token[1:]]))
                if len(hits) == 1 and hits[0] in LANGUAGES:
                    token2meta[token] = ("spaced_alpha", hits[0])
                    category2tokens["spaced"][hits[0]].append(token)
                else:
                    token2meta[token] = ("spaced_other","other")
                category2tokens["spaced"]["other"].append(token)
            else:
                if (token.startswith("<") and token.endswith(">") and not "<0y" in token) or ((token.startswith("[") and token.endswith("]"))):
                    if not token[1:-1].lower().replace("/", "") in ["br", "h1", "h2", "h3", "h4", "h5", "h6", "b", "img", "li", "tr", "td", "p", "th", "u", "em"]:
                        token2meta[token] = ("control_tokens","control_token")
                        category2tokens["control_token"]["control_token"].append(token)
                        continue
                if token.startswith("<0y"):
                    token2meta[token] = ("unicode_flanks","unicode_flanks")
                    category2tokens["unicode_flanks"]["unicode_flanks"].append(token)
                    continue

                try:
                    ut = [unicodedata.name(x).split() for x in token]
                except:
                    token2meta[token] = ("inner_errors", "errors")
                    category2tokens["inner"]["errors"].append(token)
                    continue
                hits = list(set([unicodedata.name(x).split()[0] for x in token]))
                if len(hits) == 1 and hits[0] in LANGUAGES:
                    token2meta[token] = ("inner_alpha", hits[0])
                    category2tokens["inner"][hits[0]].append(token)
                else:
                    token2meta[token] = ("inner_other", "other")
                    category2tokens["inner"]["other"].append(token)

    return token2meta, category2tokens
