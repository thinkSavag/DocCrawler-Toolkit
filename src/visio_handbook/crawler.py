# scripts/crawl.py
import argparse
import json
import os
import time
from collections import deque

import requests
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches

from visio_handbook.utils import setup_logging, save_raw, save_processed, load_config
from visio_handbook.parser import parse_html

logger = setup_logging()

def fetch_page(url, delay):
    """Download a single page and return its HTML."""
    logger.info(f"Fetching {url!r}")
    resp = requests.get(url)
    time.sleep(delay)
    return resp.text

def crawl(start_urls, delay):
    """Fetch start URLs and follow TOC links breadth-first."""
    raw_dir = "data/raw"
    proc_dir = "data/processed"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(proc_dir, exist_ok=True)

    queue = deque(start_urls)
    seen = set(start_urls)

    while queue:
        url = queue.popleft()
        html = fetch_page(url, delay)
        name = url.rstrip("/").split("/")[-1] + ".html"
        save_raw(raw_dir, name, html)

        page_data = parse_mod.parse_html(html)
        json_name = name.replace(".html", ".json")
        save_processed(proc_dir, json_name, page_data)

        for link in page_data.get("toc_links", []):
            if link.startswith("https://support.microsoft.com") and link not in seen:
                seen.add(link)
                queue.append(link)

    logger.info("Crawl complete")

def render_md(data_files, template_path, output_path):
    # … your existing render_md code …
    pass

def render_docx(data_files, template_path, output_path):
    # … your existing render_docx code …
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--format', choices=['md', 'docx'], default='md')
    args = parser.parse_args()

    cfg = load_config()  # loads configs/crawler.yaml
    start_urls = cfg.get("start_urls", [])
    delay = cfg.get("delay_seconds", 1.0)

    # 1) Crawl + BFS TOC links
    crawl(start_urls, delay)

    # 2) Render pages
    proc = "data/processed"
    data_files = [
        os.path.join(proc, f)
        for f in os.listdir(proc) if f.endswith('.json')
    ]

    if args.format == 'md':
        render_md(data_files, 'handbook_template.md', 'output/handbook.md')
    else:
        render_docx(data_files, 'handbook_template.docx', 'output/handbook.docx')

if __name__ == "__main__":
    main()