import langid
import requests
import unicodedata
import pandas as pd
import logging
import regex as re
import sentencepiece
import os
import json
import copy
from collections import defaultdict
import streamlit as st
import matplotlib.pyplot as plt
from transformers import AutoTokenizer
from code_lang_mapping import load_jsons
from token_language_classifier import TokenLanguageClassifier
from tokenizer_tokens_distribution import TokenizerTokensDistribution
from tokenizer_alphabet_viewer import TokenizerAlphabetViewer
from tokenizer_metrics_calculation import TokenizerMetricsCalculation

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("token_analysis")

language_code_country_mapping, token_code_country_mapping, alphabets_mapping_2, language_code_country_mapping_2, core_tokens = load_jsons()


def get_model_language_tokens(vocab, language_code):
    tokens = [token for token in vocab.keys() if langid.classify(token)[0] == language_code]
    return tokens


def tokens_analyzer(model_url_link, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(model_url_link, headers=headers)
    response.raise_for_status()
    tokenizer_data = response.json()

    # vocab = tokenizer_data.get('model', {}).get('vocab', {})
    vocab = tokenizer_data.get('model', {}).get('vocab', {})
    length_one_distribution = TokenizerAlphabetViewer(vocab).get_alphabet_view()
    distributing_tokens = TokenizerTokensDistribution(vocab)
    vocab_stats, classified_tokens = distributing_tokens.classify_tokens()
    new_vocab = classified_tokens["space_start"]
    all_tokens, singletons = get_model_language_tokens_gguf(new_vocab)

    metrics_calculator: TokenizerMetricsCalculation = TokenizerMetricsCalculation(vocab.keys(), classified_tokens, core_tokens, singletons)
    tokenizer_metrics = metrics_calculator.get_metrics()


    result_1 = {
        "Country": list(all_tokens.keys()),
        "Number of tokens": list(all_tokens.values())
    }
    tokenizer_metrics_dict = {
        "№ tokens": tokenizer_metrics[0],
        "№ space start tokens": tokenizer_metrics[1],
        "% space start tokens": tokenizer_metrics[2],
        "№ сore tokens": tokenizer_metrics[3],
        "% core tokens": tokenizer_metrics[4],
        "№ singleton tokens": tokenizer_metrics[5],
        "% singleton tokens": tokenizer_metrics[6],
    }
    return result_1, length_one_distribution, vocab_stats, tokenizer_metrics_dict


codings = ["LATIN", "CYRILLIC", "GREEK", "GEORGIAN"]


def get_script(char):
    try:
        script = unicodedata.name(char).split()[0]
        return script
    except ValueError:
        return "UNKNOWN"


def classify_by_script(text):
    scripts = {get_script(char) for char in text}
    return scripts


def token_unicode_coding(token):
    all_codings = classify_by_script(token)
    # if "CYRILLIC" in all_codings:
    #     print(token)
    for coding in all_codings:
        if coding in codings:
            return True
    return False


def fixing_encoding(tokenizer):
    tokens = {}
    for rid in range(tokenizer.vocab_size):
      tokens[tokenizer.decode(rid)] = rid
    return tokens


def tokens_analyzer_gguf(tokenizer):
    fixed_vocab = fixing_encoding(tokenizer)
    fixed_vocab_copy = copy.deepcopy(fixed_vocab)
    length_one_distribution = TokenizerAlphabetViewer(fixed_vocab_copy).get_alphabet_view()

    distributing_tokens = TokenizerTokensDistribution(fixed_vocab)
    vocab_stats, classified_tokens = distributing_tokens.classify_tokens()

    new_vocab = classified_tokens["space_start"]
    all_tokens, singletons = get_model_language_tokens_gguf(new_vocab)

    metrics_calculator: TokenizerMetricsCalculation = TokenizerMetricsCalculation(fixed_vocab.keys(), classified_tokens, core_tokens, singletons)
    tokenizer_metrics = metrics_calculator.get_metrics()

    # vocab = tokenizer.get_vocab()
    # length_one_distribution = TokenizerAlphabetViewer(vocab).get_alphabet_view()
    # vocab_stats, space_vocab = TokenizerTokensDistribution(vocab).classify_tokens()
    # all_tokens = get_model_language_tokens_gguf(space_vocab["space_start"])
    result_1 = {
        "Country": list(all_tokens.keys()),
        "Number of tokens": list(all_tokens.values())
    }
    tokenizer_metrics_dict = {
        "№ tokens": tokenizer_metrics[0],
        "№ space start tokens": tokenizer_metrics[1],
        "% space start tokens": tokenizer_metrics[2],
        "№ сore tokens": tokenizer_metrics[3],
        "% core tokens": tokenizer_metrics[4],
        "№ singleton tokens": tokenizer_metrics[5],
        "% singleton tokens": tokenizer_metrics[6],
    }
    return result_1, length_one_distribution, vocab_stats, tokenizer_metrics_dict


def get_model_language_tokens_gguf(vocab):
    result: dict = dict()
    counter = 0
    singletons = 0
    for token in vocab:
    # for token in vocab.keys():
        if not token_unicode_coding(token):
            continue
        if token in token_code_country_mapping.keys():
            countrycodes = token_code_country_mapping[token]
            counter += 1
        else:
            token_classifier: TokenLanguageClassifier = TokenLanguageClassifier(token)
            countrycodes = token_classifier.classify()
        for country_code in countrycodes:
            if country_code in language_code_country_mapping.keys():
                country_names = language_code_country_mapping[country_code]
                for country_name in country_names:
                    if country_name not in result.keys():
                        result.update({country_name: 1})
                    else:
                        result[country_name] += 1
            else:
                continue

        if len(countrycodes) == 1:
            singletons += 1
    # print(counter)
    return result, singletons


def plot_stats(stats):
    groups = list(stats.keys())
    values = list(stats.values())

    plt.figure(figsize=(12, 6))
    bars = plt.bar(groups, values)
    plt.title('Token Classification Distribution')
    plt.xlabel('Groups')
    plt.ylabel('Number of Tokens')
    plt.xticks(rotation=45, ha='right')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:,}',
                 ha='center', va='bottom')
    plt.tight_layout()
    st.pyplot(plt)
    # plt.show()
