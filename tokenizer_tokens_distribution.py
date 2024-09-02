import regex as re
from collections import defaultdict


class TokenizerTokensDistribution:

    def __init__(self, vocab, threshold=6):
        self.vocab = vocab
        self.threshold = threshold

    def is_space_start_capital(self, token):
        return re.match(r'^([\s\u0120\u2581])([A-Z])', token) is not None

    def is_space_start_lowercase(self, token):
        return re.match(r'^([\s\u0120\u2581])([^A-Z])', token) is not None

    def is_space_start(self, token):
        return re.match(r'^([\s\u0120\u2581])', token) is not None

    def has_replacement_bytes(self, token):
        return '�' in token

    def is_code_related(self, token):
        code_pattern = re.compile(r'''
            [\{\}\[\]()<>]          # Brackets and parentheses
            | [!<>=]=?              # Comparison operators
            | [-+*/%]=?             # Arithmetic operators
            | &&|\|\||!             # Logical operators
            | \+\+|--               # Increment/decrement
            | ::|\->|\.\.\.         # Scope resolution, arrow, ellipsis
            | [&|^~]                # Bitwise operators
            | \\[nrt]               # Common escape sequences
            | ={2,}                 # Two or more equal signs (common in markup)
            | :\\                   # Backslash after colon (often in file paths)
            | [\\\/]                # Single backslash or forward slash
            | \w+://                # Protocol prefix http://
            | [\?\"\'\.]            # Question mark, double quote, single quote, period
        ''', re.VERBOSE)
        return code_pattern.search(token) is not None

    def is_midword_short_token(self, token):
        return not re.match(r'^([\s\u0120\u2581])', token) and len(token) < self.threshold

    def is_single_char(self, token):
        return len(token) == 1

    def is_non_latin_char(self, token):
        return len(token) == 1 and ord(token) > 127

    def is_control_word(self, token):
        control_words = ['<s>', '</s>', '<pad>', '<unk>', '<mask>', '<eos>', '<bos>']
        result = ((token in control_words) or
                  (token.startswith('control_')) or
                  (token.startswith('[') and token.endswith(']')))

        return result

    def is_pure_unicode_byte(self, token):
        # Check if the token is a hexadecimal representation of a byte
        return bool(re.match(r'^<0x[0-9A-F]{2}>$', token))

    def classify_tokens(self):
        filters = [
            ('control_words', self.is_control_word),
            ('replacement_bytes', self.has_replacement_bytes),
            ('pure_unicode_byte', self.is_pure_unicode_byte),
            ('non_latin_char', self.is_non_latin_char),
            ('single_char', self.is_single_char),
            ('code_related', self.is_code_related),
            # ('space_start_capital', is_space_start_capital),
            # ('space_start_lowercase', is_space_start_lowercase),
            ('space_start', self.is_space_start),
            ('mid_word', self.is_midword_short_token),
        ]

        stats = defaultdict(int)
        classified_tokens = defaultdict(set)

        for token in self.vocab:
            classified = False
            for group, filter_func in filters:
                if filter_func(token):
                    stats[group] += 1
                    classified_tokens[group].add(token)
                    classified = True
                    break

            if not classified:
                stats['other'] += 1
                classified_tokens['other'].add(token)

        return stats, classified_tokens
