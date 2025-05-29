#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 20.09.2024
# @updated: 29.05.2024 (added support of different operating modes + fixed pdflatex error handling) by Viacheslav
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com


import os
import json
import argparse
import requests
from tqdm import tqdm
from collections import defaultdict
from .qtoklib.classification import get_classification
from .qtoklib.choose_tokenizers import choose_tokenizers
from .qtoklib.figures import plot_with_distinct_markers_and_colors
from .qtoklib.report_generator import (
    generate_html_report,
    generate_latex_report,
    )
from .qtoklib.tables import (
    get_stats_table,
    get_unicode_tables,
    get_language_table,
    )


def save_tsv_file(file_path, data):
    with open(file_path, "w", encoding="utf-8") as fw:
        for line in data:
            d = "\t".join(map(str, line))
            fw.write(f"{d}\n")

def run_it():
    parser = argparse.ArgumentParser(description='Qtop: quality control tool for tokenizers')
    parser.add_argument('-i', '--input', help='Tokenizer json files or URLs', required=True, nargs='+')
    parser.add_argument('-l', '--labels', help='Tokenizer labels', required=True, nargs='+')
    parser.add_argument('-o', '--output', help='Output folder', required=True)
    parser.add_argument('-nt', '--needed-tokenizers', help='Work only with given tokenizers or with all basic tokenizers',
                        default="AT", type=str, choices=["AT", "OGT", "OGTQ"])
    parser.add_argument('--latex', action='store_true', help='Generate LaTeX and PDF reports')
    args = parser.parse_args()

    tokenizer_files_or_urls = args.input
    labels = args.labels
    output_folder = args.output
    generate_latex = args.latex
    needed_tokenizers = args.needed_tokenizers

    # if len(tokenizer_files_or_urls) != len(labels):
    #     raise ValueError("Number of tokenizer files/URLs must match number of labels")
    # Maybe change to this row? -O is rare case
    assert len(tokenizer_files_or_urls) == len(labels), "Number of tokenizer files/URLs must match number of labels"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get model2vocab and token2hits with chosen tokenizers
    model2vocab, token2hits = choose_tokenizers(
        tokenizer_files_or_urls=tokenizer_files_or_urls,
        labels=labels,
        output_folder=output_folder,
        needed_tokenizers=needed_tokenizers
        )

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

    print(f"HTML report generated: {os.path.join(output_folder, 'report.html')}")

    if generate_latex:
        pdflatex_success = generate_latex_report(
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

        print(f"LaTeX report generated: {os.path.join(output_folder, 'report.tex')}")
        if pdflatex_success:
            print(f"PDF report generated: {os.path.join(output_folder, 'report.pdf')}")

if __name__ == "__main__":
    run_it()
