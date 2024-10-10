# Qtok: Quality Control Tool for Tokenizers

Qtok is a Python-based tool designed for quality control and analysis of tokenizers used in natural language processing (NLP) tasks.

## Features

- Analyze multiple tokenizer vocabularies simultaneously
- Generate statistics on token distribution
- Produce visualizations of token characteristics
- Compare multiple tokenizers
- Analyze Unicode coverage
- Assess language-specific token distributions (Latin and Cyrillic scripts)

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
qtok -i /path/to/tokenizer1.json /path/to/tokenizer2.json ... -l label1 label2 ... -o /path/to/output/folder
```

Arguments:
- `-i`: Paths to the tokenizer JSON files or URLs (required, multiple inputs accepted)
- `-l`: Labels for the tokenizers (required, must match the number of input files)
- `-o`: Output folder for results (required)

Example:
```bash
qtok -i tokenizer1.json https://example.com/tokenizer2.json tokenizer3.json -l label1 label2 label3 -o output_folder
```

## Output

Qtok generates several output files:

1. `basic_stats.tsv` and `basic_stats.png`: Basic statistics of the tokenizers
2. `unicode_stats.tsv` and `unicode_stats.png`: Unicode coverage statistics
3. `latin_stats.tsv` and `latin_stats.png`: Statistics for Latin script tokens
4. `cyrillic_stats.tsv` and `cyrillic_stats.png`: Statistics for Cyrillic script tokens
5. `report.html`: An HTML report summarizing all analyses
6. `report.tex` and `report.pdf`: LaTeX and PDF versions of the report (if pdflatex is installed)

## Requirements

- Python 3.6+
- matplotlib
- numpy
- pandas
- requests

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
