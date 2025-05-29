# Qtok/src/qtok/qtoklib/choose_tokenizers.py
# -*- coding: utf-8 -*-
#
# @created: 29.05.2025
# @updated: 29.05.2024 (added support of different operating modes + fixed pdflatex error handling)
# @author: Viacheslav Siniaev
# @contact: sisla00@protonmail.com

import os
import copy
import json
from tqdm import tqdm
from .tokenizer import load_vocab

model2vocab_json_file = os.path.join(os.path.dirname(__file__), "../data/model2vocab_tok.json")
token2his_json_file = os.path.join(os.path.dirname(__file__), "../data/token2hits_tok.json")

basic_paths = (model2vocab_json_file, token2his_json_file)
with open(basic_paths[1]) as fh:
    token2hits = json.load(fh)


def download_or_use_local(file_or_url: str, output_folder: str, label: str):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    local_file = os.path.join(output_folder, f"tokenizer_{label}.json")

    if file_or_url.startswith(('http://', 'https://')):

        if "huggingface.co" in file_or_url and "blob/main" in file_or_url:
            file_or_url = file_or_url.replace("blob/main", "raw/main")

        try:
            response = requests.get(file_or_url)
            if response.status_code == 200:
                with open(local_file, 'wb') as f:
                    f.write(response.content)
                print(f"File downloaded successfully and saved to {local_file}")
                return local_file
            else:
                print(f"Failed to download file. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred while downloading: {e}")
            return None
    else:
        if os.path.exists(file_or_url):
            return file_or_url
        else:
            print(f"Local file not found: {file_or_url}")
            return None


def prepare_tokens(tokenizer_vocab: dict,
                   token2hits_vocab: dict,
                   model2vocab_all: dict = None) -> tuple:

    for label, vocab in tqdm(tokenizer_vocab.items(), desc="Updating vocabularies"):
        if model2vocab_all is not None:
            if label == "Qtok":
                model2vocab_all = {"Qtok": token2hits, **model2vocab_all}
            else:
                model2vocab_all[label] = vocab
            tokenizer_vocab = copy.deepcopy(model2vocab_all)

        for token, rank in vocab.items():
            if token not in token2hits_vocab:
                token2hits_vocab[token] = [0] * len(tokenizer_vocab) + [rank]
            else:
                token2hits_vocab[token].extend([0] * (len(tokenizer_vocab) - len(token2hits_vocab[token])) + [rank])

    return tokenizer_vocab, token2hits_vocab

def choose_tokenizers(tokenizer_files_or_urls: dict,
                      labels: list,
                      output_folder: str,
                      basic_paths: tuple = basic_paths,
                      token2hits: dict = token2hits,
                      needed_tokenizers: str = "AT") -> tuple:
    """
    Choose only needed tokenizers to count statistics.
    Result depends on argument '--needed-tokenizer'.
    Can work in 3 modes:
        - 'AT' - All Tokenizers which were given in terminal + basic tokenizers. Default setting.
        - 'OGT' - Only Given Tokenizers. Will process only tokenizers, which were given in terminal.
        - 'OGTQ' - Only Given Tokenizers + Qtok unified tokenizer.

    Returns a dictionary with chosen tokenizers.
    """

    model2vocab_tok = {}
    for file_or_url, label in tqdm(zip(tokenizer_files_or_urls, labels), desc="Downloading tokenizers", total=len(labels)):
        local_file = download_or_use_local(file_or_url, output_folder, label)
        if local_file:
            model2vocab_tok[label] = load_vocab(local_file)
        else:
            print(f"Skipping tokenizer for label {label} due to file/download issues")

    if not model2vocab_tok:
        print("No valid tokenizer files found. Exiting.")
        return


    # Choose tokenizers to return
    if needed_tokenizers == "OGT":
        model2vocab = copy.deepcopy(model2vocab_tok)
        _, token2hits = prepare_tokens(model2vocab, token2hits)

    elif needed_tokenizers == "OGTQ":
        model2vocab_tok = {"Qtok": token2hits, **model2vocab_tok}
        model2vocab = copy.deepcopy(model2vocab_tok)
        _, token2hits = prepare_tokens(model2vocab, token2hits)

    elif needed_tokenizers == "AT":
        model2vocab_tok = {"Qtok": token2hits, **model2vocab_tok}
        with open(basic_paths[0]) as fh:
            model2vocab_all = json.load(fh)

        model2vocab, token2hits = prepare_tokens(model2vocab_tok, token2hits, model2vocab_all)

    else:
        print(f"""
              Error Invalid Key: {needeed_tokenizers}
              Please, choose one of the following options for --needeed-tokenizers parameter:
                  - "AT" for All Tokenizers
                  - "OGT" for Only Given Tokenizers
                  - "OGTQ" for Only Given Tokenizers + Qtok
              """)

    return model2vocab, token2hits
