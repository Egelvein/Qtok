from collections import defaultdict


def get_stats_table(model2vocab_tok, token2hits_tok, token2meta):

    headers = [
        "control_tokens",
        "pure_unicode",
        "char_alpha",
        "spaced_alpha",
        "inner_alpha",

        "char_other",
        "spaced_other",
        "inner_other",

        "unicode_flanks",

        "char_errors",
        "spaced_errors",



        "inner_errors",
    ]
    tokenizers_to_meta = {}


    model = "Qtok"
    tokenizers_to_meta[model] = defaultdict(int)
    for token in token2hits_tok:
        meta = token2meta[token]
        if meta[0] in headers:
            tokenizers_to_meta[model][meta[0]] += 1
        else:
            print(meta)
            break

    for model, tokens in model2vocab_tok.items():

        tokenizers_to_meta[model] = defaultdict(int)
        for token in tokens:
            meta = token2meta[token]
            if meta[0] in headers:
                tokenizers_to_meta[model][meta[0]] += 1
            else:
                print(meta)
                break

    table = [
        ["Tokenizer"] + headers[::]
    ]
    model = "Qtok"
    table.append([model] + [0] * len(headers))
    for i, header in enumerate(headers, start=1):
        table[-1][i] = tokenizers_to_meta[model][header]

    for model in model2vocab_tok:
        table.append([model] + [0] * len(headers))
        for i, header in enumerate(headers, start=1):
            table[-1][i] = tokenizers_to_meta[model][header]

    table_p = [
    ["Tokenizer"] + headers[::]
    ]
    model = "Qtok"
    table_p.append([model] + [0] * len(headers))
    for i, header in enumerate(headers, start=1):
        table_p[-1][i] = round(100.*tokenizers_to_meta[model][header]/len(token2meta), 2)

    for model in model2vocab_tok:
        table_p.append([model] + [0] * len(headers))
        for i, header in enumerate(headers, start=1):
            table_p[-1][i] = round(100.*tokenizers_to_meta[model][header]/len(model2vocab_tok[model]), 2)



    return table, table_p


def get_unicode_tables(model2vocab_tok, token2hits_tok, token2meta):
    headers = []
    tokenizers_to_meta = {}

    model = "Qtok"
    tokenizers_to_meta[model] = defaultdict(int)

    for token in token2hits_tok:
        meta = token2meta[token]
        if not "alpha" in meta[0]:
            continue
        lang = meta[1]
        tokenizers_to_meta[model][meta] += 1

    headers = list(tokenizers_to_meta[model].keys())

    for model, tokens in model2vocab_tok.items():
        tokenizers_to_meta[model] = defaultdict(int)
        for token in tokens:
            meta = token2meta[token]
            if not "alpha" in meta[0]:
                continue
            lang = meta[1]
            tokenizers_to_meta[model][meta] += 1

    table = [
        ["Tokenizer"] + headers[::]
    ]

    model = "Qtok"
    table.append([model] + [0] * len(headers))
    for i, header in enumerate(headers, start=1):
        table[-1][i] = round(100.*tokenizers_to_meta[model][header]/len(token2meta), 2)

    for model in model2vocab_tok:
        table.append([model] + [0] * len(headers))
        for i, header in enumerate(headers, start=1):
            table[-1][i] = round(100.*tokenizers_to_meta[model][header]/len(model2vocab_tok[model]), 2)

    transposed_table = list(zip(*table))

    def format_header(header_tuple):
        return f"{header_tuple[1]} ({header_tuple[0].replace('_alpha', '')})"

    formatted_table = [[format_header(row[0])] + list(row[1:]) if isinstance(row[0], tuple) else list(row) for row in transposed_table]

    other_row = ['Other'] + [0] * (len(formatted_table[0]) - 1)
    final_table = [formatted_table[0]]

    for row in formatted_table[1:]:
        if all(float(cell) <= 1 for cell in row[1:]):
            for i in range(1, len(row)):
                other_row[i] += float(row[i])
        else:
            final_table.append(row)

    other_row = [other_row[0]] + [round(val, 2) for val in other_row[1:]]

    if any(other_row[1:]):
        final_table.append(other_row)

    final_table = list(zip(*final_table))

    with open("table2.tsv", "w") as fw:
        for line in final_table:
            print("\t".join(map(str, line)))
            d = "\t".join(map(str, line))
            fw.write(f"{d}\n")

    return final_table


def get_language_table(model2vocab_tok, token2hits_tok, token2meta, lang_data):

    headers = []
    tokenizers_to_meta = {}

    model = "Qtok"
    tokenizers_to_meta[model] = defaultdict(int)
    model2size = defaultdict(int)

    unseen_tokens = set()

    for token in token2hits_tok:
        meta = token2meta[token]
        if not "alpha" in meta[0]:
            continue
        if len(token) == 1:
            continue
        if not token in lang_data:
            unseen_tokens.add(token)
            continue
        for lang in lang_data[token]:
            tokenizers_to_meta[model][lang] += 1/len(lang_data[token])
            model2size[model] += 1

    headers = list(tokenizers_to_meta[model].keys())

    for model, tokens in model2vocab_tok.items():
        tokenizers_to_meta[model] = defaultdict(int)
        for token in tokens:
            meta = token2meta[token]
            if not "alpha" in meta[0]:
                continue
            if not token in lang_data:
                continue
            for lang in lang_data[token]:
                tokenizers_to_meta[model][lang] += 1/len(lang_data[token])
                model2size[model] += 1

    table = [
        ["Tokenizer"] + headers[::]
    ]

    model = "Qtok"
    table.append([model] + [0] * len(headers))
    for i, header in enumerate(headers, start=1):
        table[-1][i] = round(100.*tokenizers_to_meta[model][header]/model2size[model], 2)

    for model in model2vocab_tok:
        table.append([model] + [0] * len(headers))
        for i, header in enumerate(headers, start=1):
            table[-1][i] = round(100.*tokenizers_to_meta[model][header]/model2size[model], 2)

    transposed_table = list(zip(*table))

    def format_header(header_tuple):
        return f"{header_tuple[1]} ({header_tuple[0].replace('_alpha', '')})"

    formatted_table = [[format_header(row[0])] + list(row[1:]) if isinstance(row[0], tuple) else list(row) for row in transposed_table]

    other_row = ['Other'] + [0] * (len(formatted_table[0]) - 1)
    final_table = [formatted_table[0]]

    for row in formatted_table[1:]:
        if all(float(cell) <= 0.5 for cell in row[1:]):
            for i in range(1, len(row)):
                other_row[i] += float(row[i])
        else:
            final_table.append(row)

    other_row = [other_row[0]] + [round(val, 2) for val in other_row[1:]]

    if any(other_row[1:]):
        final_table.append(other_row)

    final_table = list(zip(*final_table))

    return final_table, unseen_tokens