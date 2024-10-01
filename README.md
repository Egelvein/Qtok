# Qtok: Quality Control Tool for Tokenizers

Qtok is a Python-based tool designed for quality control and analysis of tokenizers used in natural language processing (NLP) tasks.

## Features

- Analyze tokenizer vocabularies
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
qtok -i /path/to/tokenizer.json -l tokenizer_label -o /path/to/output/folder
```

Arguments:
- `-i`: Path to the tokenizer JSON file (required)
- `-l`: Label for the tokenizer (optional, default is "default")
- `-o`: Output folder for results (required)

## Output

Qtok generates several output files:

1. `basic_stats.tsv` and `basic_stats.png`: Basic statistics of the tokenizer
2. `unicode_stats.tsv` and `unicode_stats.png`: Unicode coverage statistics
3. `latin_stats.tsv` and `latin_stats.png`: Statistics for Latin script tokens
4. `cyrillic_stats.tsv` and `cyrillic_stats.png`: Statistics for Cyrillic script tokens

## Requirements

- Python 3.6+
- matplotlib
- numpy
- pandas

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
