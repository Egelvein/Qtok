#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 20.09.2024
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

import argparse
import requests
import os
from .qtoklib.tokenizer import load_vocab
import json
from .qtoklib.classification import get_classification
from .qtoklib.tables import get_stats_table
from .qtoklib.tables import get_unicode_tables
from .qtoklib.figures import plot_with_distinct_markers_and_colors
from collections import defaultdict
from .qtoklib.tables import get_language_table
from .qtoklib.report_generator import generate_html_report, generate_latex_report

def save_tsv_file(file_path, data):
    with open(file_path, "w", encoding="utf-8") as fw:
        for line in data:
            # print("\t".join(map(str, line)))
            d = "\t".join(map(str, line))
            fw.write(f"{d}\n")

def download_or_use_local(file_or_url, output_folder, label):
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

def run_it():
    parser = argparse.ArgumentParser(description='Qtop: quality control tool for tokenizers')
    parser.add_argument('-i', help='Tokenizer json files or URLs', required=True, nargs='+')
    parser.add_argument('-l', help='Tokenizer labels', required=True, nargs='+')
    parser.add_argument('-o', help='Output folder', required=True)
    args = parser.parse_args()

    tokenizer_files_or_urls = args.i
    labels = args.l
    output_folder = args.o

    if len(tokenizer_files_or_urls) != len(labels):
        raise ValueError("Number of tokenizer files/URLs must match number of labels")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    model2vocab_tok = {}
    for file_or_url, label in zip(tokenizer_files_or_urls, labels):
        local_file = download_or_use_local(file_or_url, output_folder, label)
        if local_file:
            model2vocab_tok[label] = load_vocab(local_file)
        else:
            print(f"Skipping tokenizer for label {label} due to file/download issues")

    if not model2vocab_tok:
        print("No valid tokenizer files found. Exiting.")
        return

    model2vocab_json_file = os.path.join(os.path.dirname(__file__), "data/model2vocab_tok.json")
    token2his_json_file = os.path.join(os.path.dirname(__file__), "data/token2hits_tok.json")

    with open(model2vocab_json_file) as fh:
        model2vocab = json.load(fh)

    with open(token2his_json_file) as fh:
        token2hits = json.load(fh)

    # Update model2vocab and token2hits with new tokenizers
    for label, vocab in model2vocab_tok.items():
        model2vocab[label] = vocab
        for token, rank in vocab.items():
            if token not in token2hits:
                token2hits[token] = [0] * len(model2vocab) + [rank]
            else:
                token2hits[token].extend([0] * (len(model2vocab) - len(token2hits[token])) + [rank])

    token2meta, category2tokens = get_classification(token2hits)

    stats_table, stats_table_p = get_stats_table(model2vocab, token2hits, token2meta)
    unicode_table_p = get_unicode_tables(model2vocab, token2hits, token2meta)

    file_path0 = os.path.join(output_folder, "basic_stats_abs.tsv")
    file_path1 = os.path.join(output_folder, "basic_stats.tsv")
    output_image_file1 = os.path.join(output_folder, "basic_stats.png")

    file_path2 = os.path.join(output_folder, "unicode_stats.tsv")
    output_image_file2 = os.path.join(output_folder, "unicode_stats.png")

    file_path_lang_lat = os.path.join(output_folder, "latin_stats.tsv")
    output_image_file_lat = os.path.join(output_folder, "latin_stats.png")
    file_path_lang_cyr = os.path.join(output_folder, "cyrillic_stats.tsv")
    output_image_file_cyr = os.path.join(output_folder, "cyrillic_stats.png")

    save_tsv_file(file_path0, stats_table)
    save_tsv_file(file_path1, stats_table_p)
    save_tsv_file(file_path2, unicode_table_p)

    plot_with_distinct_markers_and_colors(labels, file_path1, output_image_file1)
    plot_with_distinct_markers_and_colors(labels, file_path2, output_image_file2)

    tokens2natural_lat_file = os.path.join(os.path.dirname(__file__), "data/tokens2natural_lat.json")
    tokens2natural_cyr_file = os.path.join(os.path.dirname(__file__), "data/tokens2natural_cyr.json")

    with open(tokens2natural_lat_file) as fh:
        lat_data = json.load(fh)
    with open(tokens2natural_cyr_file) as fh:
        cyr_data = json.load(fh)

    final_table_lat, unseen_tokens_lat = get_language_table(model2vocab, token2hits, token2meta, lat_data)
    final_table_cyr, unseen_tokens_cyr = get_language_table(model2vocab, token2hits, token2meta, cyr_data)

    save_tsv_file(file_path_lang_lat, final_table_lat)
    save_tsv_file(file_path_lang_cyr, final_table_cyr)

    plot_with_distinct_markers_and_colors(labels, file_path_lang_lat, output_image_file_lat)
    plot_with_distinct_markers_and_colors(labels, file_path_lang_cyr, output_image_file_cyr)

    generate_html_report(
        output_folder,
        labels,
        stats_table,
        stats_table_p,
        unicode_table_p,
        final_table_lat,
        final_table_cyr,
        unseen_tokens_lat,
        unseen_tokens_cyr
    )

    generate_latex_report(
        output_folder,
        labels,
        stats_table,
        stats_table_p,
        unicode_table_p,
        final_table_lat,
        final_table_cyr,
        unseen_tokens_lat,
        unseen_tokens_cyr
    )

    print(f"HTML report generated: {os.path.join(output_folder, 'report.html')}")
    print(f"LaTeX report generated: {os.path.join(output_folder, 'report.tex')}")
    print(f"PDF report generated: {os.path.join(output_folder, 'report.pdf')}")

if __name__ == "__main__":
    run_it()
