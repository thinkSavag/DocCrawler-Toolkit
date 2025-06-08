import argparse
import json
import os
import time

import requests
from jinja2 import Environment, FileSystemLoader
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches

from utils import setup_logging, save_raw, load_config

logger = setup_logging()


def crawl():
    """Fetch start URLs and store raw HTML in ``data/raw``."""
    logger.info("1) Loading config from configs/crawler.yaml")
    cfg = load_config()
    start_urls = cfg.get("start_urls", [])
    delay = cfg.get("delay_seconds", 1.0)
    out_dir = cfg.get("output_folder", "data/raw")
    os.makedirs(out_dir, exist_ok=True)
    logger.info(f"2) Will fetch {len(start_urls)} start URLs")

    for url in start_urls:
        logger.info(f"3) Fetching {url!r}")
        resp = requests.get(url)
        name = url.rstrip("/").split("/")[-1] + ".html"
        save_raw(out_dir, name, resp.text)
        logger.info(f"   Saved {os.path.join(out_dir, name)}")
        time.sleep(delay)

    logger.info("4) Crawl complete")


def render_md(data_files, template_path, output_path):
    """Render parsed JSON pages into Markdown."""
    env = Environment(loader=FileSystemLoader('templates'))
    tmpl = env.get_template(template_path)
    pages = [json.load(open(f, 'r', encoding='utf-8')) for f in data_files]
    out = tmpl.render(pages=pages)
    with open(output_path, 'w', encoding='utf-8') as fh:
        fh.write(out)
    logger.info(f"✅ Rendered Markdown to {output_path}")


def render_docx(data_files, template_path, output_path):
    """Render parsed JSON pages into a Word document."""
    tpl = DocxTemplate(os.path.join('templates', template_path))
    context = {'pages': []}
    for f in data_files:
        data = json.load(open(f, 'r', encoding='utf-8'))
        for sec in data.get('sections', []):
            sec['images'] = [InlineImage(tpl, img, width=Inches(4))
                             for img in sec.get('images', [])]
        context['pages'].append(data)
    tpl.render(context)
    tpl.save(output_path)
    logger.info(f"✅ Rendered DOCX to {output_path}")


def main():
    """Render all processed JSON into the chosen output format."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--format', choices=['md', 'docx'], default='md')
    args = parser.parse_args()

    proc = 'data/processed'
    data_files = [os.path.join(proc, f) for f in os.listdir(proc)
                  if f.endswith('.json')]

    if args.format == 'md':
        render_md(data_files, 'handbook_template.md', 'output/handbook.md')
    else:
        render_docx(data_files, 'handbook_template.docx',
                    'output/handbook.docx')


if __name__ == '__main__':
    main()
