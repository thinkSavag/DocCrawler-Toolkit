import time

import os
import json

from utils import setup_logging, save_raw, load_config
import requests, time, os
from jinja2 import Environment, FileSystemLoader
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import argparse

logger = setup_logging()

def crawl():
        """
    1) Load configuration from configs/crawler.yaml
    2) For each URL: download HTML, save to data/raw/
    3) Parse with parse_html(), save JSON to data/processed/
    4) After all pages, render templates
    """
        
    logger.info("1) Loading crawler config")
    cfg = load_config("configs/crawler.yaml")
    start_urls = cfg.get("start_urls", [])
    delay      = cfg.get("delay_seconds", 1.0)
    out_dir    = cfg.get("output_folder", "data/raw")
    os.makedirs(out_dir, exist_ok=True)

    logger.info(f"2) Beginning fetch loop (delay {delay!s}s)")
    for url in start_urls:
        logger.info(f"   → Fetching {url}")
        resp = requests.get(url)
        filename = url.rstrip("/").split("/")[-1] + ".html"
        path     = os.path.join(out_dir, filename)
        save_raw(path, resp.text)
        logger.info(f"   ✔ Saved raw HTML to {path}")
        logger.info(f"   → Waiting {delay!s}s before next request")
        time.sleep(delay)

    logger.info("3) Fetch loop complete. Files in data/raw/")
    # …then call parse, render, etc., each wrapped in logger.info()

    # logger.info("4) Parsing raw HTML → JSON")
    # for each file…
    # logger.info(f"   → Parsing {raw_file}")
    # …save processed JSON
    # logger.info(f"   ✔ Wrote JSON to {processed_file}")



def render_md(data_files, template_path, output_path):
    env = Environment(loader=FileSystemLoader('templates'))
    tmpl = env.get_template(template_path)
    combined = []
    for f in data_files:
        with open(f, 'r', encoding='utf-8') as j:
            combined.append(json.load(j))
    out = tmpl.render(pages=combined)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(out)


def render_docx(data_files, template_path, output_path):
    tpl = DocxTemplate(os.path.join('templates', template_path))
    context = {'pages': []}
    for f in data_files:
        data = json.load(open(f, 'r', encoding='utf-8'))
        # handle images in docx
        for sec in data.get('sections', []):
            sec['images'] = [InlineImage(tpl, img, width=Inches(4)) for img in sec.get('images', [])]
        context['pages'].append(data)
    tpl.render(context)
    tpl.save(output_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--format', choices=['md','docx'], default='md')
    args = parser.parse_args()

    proc = 'data/processed'
    data_files = [os.path.join(proc, f) for f in os.listdir(proc) if f.endswith('.json')]

    if args.format=='md':
        render_md(data_files, 'handbook_template.md', 'output/handbook.md')
    else:
        render_docx(data_files, 'handbook_template.docx', 'output/handbook.docx')

if __name__=='__main__':
    main()
