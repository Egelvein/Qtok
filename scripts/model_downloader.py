import requests
import os
import logging
from enum import IntEnum, auto
from transformers import AutoTokenizer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("model_downloader")
sess = requests.Session()


class TOKENIZER_TYPE(IntEnum):
    SPM = auto()
    BPE = auto()
    WPM = auto()


def download_file_with_auth(url, token, save_path):
    headers = {"Authorization": f"Bearer {token}"}
    response = sess.get(url, headers=headers)
    response.raise_for_status()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    logger.info(f"File {save_path} downloaded successfully")


def download_model(model, auth_token):
    name = model["name"]
    repo = model["repo"]
    tokt = model["tokt"]

    os.makedirs(f"models/tokenizers/{name}", exist_ok=True)

    files = ["config.json", "tokenizer.json", "tokenizer_config.json"]
    if tokt == TOKENIZER_TYPE.SPM:
        files.append("tokenizer.model")

    for file in files:
        save_path = f"models/tokenizers/{name}/{file}"
        if os.path.isfile(save_path):
            logger.info(f"{name}: File {save_path} already exists - skipping")
            continue
        download_file_with_auth(f"{repo}/resolve/main/{file}", auth_token, save_path)


def load_tokenizer(name):
    return AutoTokenizer.from_pretrained(f"models/tokenizers/{name}")
