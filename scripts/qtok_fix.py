from transformers import PreTrainedTokenizerFast
import json
import argparse

def main(input_file, output_file):
    '''
    Fix broken encoding in tokenizer
    '''
    tokenizer = PreTrainedTokenizerFast.from_pretrained(input_file, use_fast=False)
    id2token = {}
    token2id = {}
    for rid in range(tokenizer.vocab_size):
        token = tokenizer.decode(rid).replace(" ", "Ġ")
        id2token[rid] = token
        token2id[token] = rid

    with open(input_file, "r") as fr:
        data = json.load(fr)

    fixed_vocab = {}
    raw_token2id = {}
    for raw_token, value in data["model"]["vocab"].items():
        fixed_vocab[id2token[value]] = value
        raw_token2id[raw_token] = value
    data["model"]["vocab"] = fixed_vocab
    for i, value in enumerate(data["model"]["merges"]):
        a, b = value.split(" ")
        a_token, b_token = id2token[raw_token2id[a]], id2token[raw_token2id[b]]
        data["model"]["merges"][i] = f"{a_token} {b_token}"

    with open(output_file, "w", encoding="utf-8") as fw:
        json.dump(data, fw, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Fix broken encoding in tokenizer")
    parser.add_argument("-i", "--input_file", type=str, required=True, help="Path to the tokenizer json input file")
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the output file")
    args = parser.parse_args()
    input_file = args.input_file
    outout_file = args.output_file
    if input_file == outout_file:
        print("Input and output file are the same")
        exit(1)
    main(input_file, outout_file)