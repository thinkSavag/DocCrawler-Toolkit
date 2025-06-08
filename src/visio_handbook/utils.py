import json
import logging
import os
from datetime import datetime

import requests
import yaml


def setup_logging(log_dir="data/logs"):
    """Configure console and file logging."""
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
    return logging.getLogger(__name__)


def save_raw(folder, name, text):
    """Write raw HTML ``text`` to ``folder/name``."""
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, name), 'w', encoding='utf-8') as f:
        f.write(text)


def load_raw(path):
    """Read text from ``path``."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def save_processed(folder, name, data):
    """Serialize ``data`` as JSON to ``folder/name``."""
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def download_image(url, folder):
    """Download an image to ``folder`` and return its local path."""
    os.makedirs(folder, exist_ok=True)
    fname = url.split('/')[-1]
    path = os.path.join(folder, fname)
    r = requests.get(url)
    if r.ok:
        with open(path, 'wb') as f:
            f.write(r.content)
        return path
    return ''


def load_config(path="configs/crawler.yaml"):
    """Load crawler configuration from ``path``."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_processed_files(proc_dir="data/processed"):
    """Return a list of JSON files under ``proc_dir``."""
    os.makedirs(proc_dir, exist_ok=True)
    return [
        os.path.join(proc_dir, f)
        for f in os.listdir(proc_dir)
        if f.endswith(".json")
    ]


def build_context(files):
    """Load pages from ``files`` and return a render context."""
    pages = []
    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            pages.append(json.load(f))
    return {"pages": pages}
