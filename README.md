# Qtok: Quality Control Tool for Tokenizers

Qtok is a Python-based tool designed for quality control and analysis of tokenizers used in natural language processing (NLP) tasks.

## Features

- Analyze multiple tokenizer vocabularies simultaneously
- Generate statistics on token distribution
- Produce visualizations of token characteristics
- Compare multiple tokenizers
- Analyze Unicode coverage
- Assess language-specific token distributions (Latin and Cyrillic scripts)

![Qtok Pipeline](https://raw.githubusercontent.com/nup-csai/Qtok/main/images/pipeline.svg)

## Installation

You can install Qtok using pip:

```bash
pip install qtok
```

Or clone the repository and install:

```bash
git clone https://github.com/nup-csai/Qtok.git
cd Qtok
pip install .
```

## Usage

Qtok can be used as a command-line tool:

```bash
qtok -i /path/to/tokenizer1.json /path/to/tokenizer2.json ... -l label1 label2 ... -o /path/to/output/folder [--latex]
```

Arguments:
- `-i`: Paths to the tokenizer JSON files or URLs (required, multiple inputs accepted)
- `-l`: Labels for the tokenizers (required, must match the number of input files)
- `-o`: Output folder for results (required)
- `--latex`: Optional flag to generate LaTeX and PDF reports (default: False)

Example:
```bash
qtok -i /path/to/tokenizer1.json /path/to/tokenizer2.json -l label1 label2 -o /path/to/output/folder --latex
```

- Arguments:
  - `-i`: Paths to the tokenizer JSON files or URLs (required, multiple inputs accepted)
  - `-l`: Labels for the tokenizers (required, must match the number of input files)
  - `-o`: Output folder for results (required)
  
Example if you want to work only with specific tokenizers:
```bash
qtok -i /path/to/tokenizer1.json /path/to/tokenizer2.json -l label1 label2 -o /path/to/output/folder -nt OGT --latex
```

- Arguments:
  - `-i`: Paths to the tokenizer JSON files or URLs (required, multiple inputs accepted)
  - `-l`: Labels for the tokenizers (required, must match the number of input files)
  - `-o`: Output folder for results (required)
  - `-nt`: Work only with given tokenizers or with all basic tokenizers. By default "AT" (All Tokenizers), more supported options "OGT" (Only Given Tokenizers) and "OGTQ" (Only Given Tokenizers + Qtok unified tokenizer)
## Output

Qtok generates several output files:

1. `basic_stats.tsv` and `basic_stats.png`: Basic statistics of the tokenizers
2. `unicode_stats.tsv` and `unicode_stats.png`: Unicode coverage statistics
3. `latin_stats.tsv` and `latin_stats.png`: Statistics for Latin script tokens
4. `cyrillic_stats.tsv` and `cyrillic_stats.png`: Statistics for Cyrillic script tokens
5. `report.html`: An HTML report summarizing all analyses
6. `report.tex` and `report.pdf`: LaTeX and PDF versions of the report (if `--latex` flag is used and pdflatex is installed)

## Requirements

- Python 3.6+
- matplotlib
- numpy
- pandas
- requests
- tqdm

## Reproducibility

For full tables and data, please refer to the Jupyter notebook available at:

[Qtok/paper/Qtok_v3.ipynb](https://github.com/nup-csai/Qtok/blob/main/paper/Qtok_v3.ipynb)

## Contributing

Contributions to Qtok are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Aleksey Komissarov
- Iaroslav Chelombitko
- Egor Safronov

## Contact

For any queries, please contact ad3002@gmail.com.

## Acknowledgments

- Thanks to all contributors and users of Qtok
- Special thanks to the NLP community for inspiration and support
