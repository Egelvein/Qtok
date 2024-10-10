# Qtok/src/qtok/qtoklib/tables.py

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

    # Process Qtok
    tokenizers_to_meta["Qtok"] = defaultdict(int)
    for token in token2hits_tok:
        meta = token2meta[token]
        if meta[0] in headers:
            tokenizers_to_meta["Qtok"][meta[0]] += 1
        else:
            print(f"Unexpected meta: {meta}")

    # Process other tokenizers
    for model, tokens in model2vocab_tok.items():
        tokenizers_to_meta[model] = defaultdict(int)
        for token in tokens:
            meta = token2meta[token]
            if meta[0] in headers:
                tokenizers_to_meta[model][meta[0]] += 1
            else:
                print(f"Unexpected meta for {model}: {meta}")

    # Create tables
    table = [["Tokenizer"] + headers]
    table_p = [["Tokenizer"] + headers]

    for model in ["Qtok"] + list(model2vocab_tok.keys()):
        row = [model] + [tokenizers_to_meta[model][header] for header in headers]
        table.append(row)

        total = sum(tokenizers_to_meta[model].values())
        row_p = [model] + [round(100 * tokenizers_to_meta[model][header] / total, 2) for header in headers]
        table_p.append(row_p)

    return table, table_p

def get_unicode_tables(model2vocab_tok, token2hits_tok, token2meta):
    tokenizers_to_meta = defaultdict(lambda: defaultdict(int))
    model2size = defaultdict(int)

    # Process Qtok
    for token in token2hits_tok:
        meta = token2meta[token]
        if "alpha" in meta[0]:
            tokenizers_to_meta["Qtok"][meta] += 1
            model2size["Qtok"] += 1

    # Process other tokenizers
    for model, tokens in model2vocab_tok.items():
        for token in tokens:
            meta = token2meta[token]
            if "alpha" in meta[0]:
                tokenizers_to_meta[model][meta] += 1
                model2size[model] += 1

    headers = list(tokenizers_to_meta["Qtok"].keys())
    table = [["Tokenizer"] + headers]

    for model in ["Qtok"] + list(model2vocab_tok.keys()):
        row = [model] + [round(100 * tokenizers_to_meta[model][header] / model2size[model], 2) for header in headers]
        table.append(row)

    # Transpose and format table
    transposed_table = list(zip(*table))
    formatted_table = [[format_header(row[0])] + list(row[1:]) if isinstance(row[0], tuple) else list(row) for row in transposed_table]

    # Process 'Other' row
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

    return list(zip(*final_table))

def get_language_table(model2vocab_tok, token2hits_tok, token2meta, lang_data):
    tokenizers_to_meta = defaultdict(lambda: defaultdict(float))
    model2size = defaultdict(int)
    unseen_tokens = set()

    # Process Qtok
    for token in token2hits_tok:
        meta = token2meta[token]
        if "alpha" in meta[0] and len(token) > 1:
            if token in lang_data:
                for lang in lang_data[token]:
                    tokenizers_to_meta["Qtok"][lang] += 1 / len(lang_data[token])
                    model2size["Qtok"] += 1
            else:
                unseen_tokens.add(token)

    # Process other tokenizers
    for model, tokens in model2vocab_tok.items():
        for token in tokens:
            meta = token2meta[token]
            if "alpha" in meta[0] and len(token) > 1:
                if token in lang_data:
                    for lang in lang_data[token]:
                        tokenizers_to_meta[model][lang] += 1 / len(lang_data[token])
                        model2size[model] += 1

    headers = list(tokenizers_to_meta["Qtok"].keys())
    table = [["Tokenizer"] + headers]

    for model in ["Qtok"] + list(model2vocab_tok.keys()):
        row = [model] + [round(100 * tokenizers_to_meta[model][header] / model2size[model], 2) for header in headers]
        table.append(row)

    # Transpose and format table
    transposed_table = list(zip(*table))
    formatted_table = [[format_header(row[0])] + list(row[1:]) if isinstance(row[0], tuple) else list(row) for row in transposed_table]

    # Process 'Other' row
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

    return list(zip(*final_table)), unseen_tokens

def format_header(header):
    if isinstance(header, tuple):
        return f"{header[1]} ({header[0].replace('_alpha', '')})"
    return header
