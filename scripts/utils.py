import logging
import os
import json
import requests
from datetime import datetime

def setup_logging(log_dir="data/logs"):
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{datetime.now():%Y%m%d_%H%M%S}.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger()

def save_raw(folder, name, text):
    with open(os.path.join(folder, name), 'w', encoding='utf-8') as f:
        f.write(text)


def load_raw(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def save_processed(folder, name, data):
    with open(os.path.join(folder, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def download_image(url, folder):
    os.makedirs(folder, exist_ok=True)
    fname = url.split('/')[-1]
    path = os.path.join(folder, fname)
    r = requests.get(url)
    if r.ok:
        with open(path, 'wb') as f:
            f.write(r.content)
        return path
    return ''

# utils.py  (add this at the bottom)

import yaml

def load_config(path="configs/crawler.yaml"):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
