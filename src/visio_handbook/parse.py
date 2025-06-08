import json
import logging
import os
import re

from bs4 import BeautifulSoup

from visio_handbook.utils import (
    load_raw,
    save_processed,
    download_image,
    setup_logging,
)

logger = setup_logging()

# scripts/parse.py

def parse_html(html: str) -> dict:
    """Extract metadata, TOC links, headers, and sections from a support page."""
    soup = BeautifulSoup(html, 'html.parser')

    # 1) <head> metadata
    metadata = {tag.name: tag.get_text() for tag in soup.head.find_all()}

    # 2) Main <article> content
    article = soup.find("article")
    content_html = article.decode_contents() if article else ""

    # 3) Gather headers (h1–h6) inside the article
    headers = []
    if article:
        for h in article.find_all(re.compile("^h[1-6]$")):
            headers.append({"tag": h.name, "text": h.get_text(strip=True)})

    # 4) Extract sidebar TOC links
    toc_links = []
    sidebar = soup.select_one("div.supLeftNavCategory")
    if sidebar:
        for a in sidebar.find_all("a", href=True):
            toc_links.append(a["href"].split("#")[0])

    # 5) Build detailed sections (h2/h3 → paragraphs, tables, images)
    sections = []
    for h in soup.find_all(['h2', 'h3']):
        level = 2 if h.name == 'h2' else 3
        # Collect siblings until next same-or-higher header
        content_nodes = []
        for sib in h.find_next_siblings():
            if sib.name in ['h2', 'h3']:
                break
            content_nodes.append(sib)

        # Extract text
        texts = [n.get_text(strip=True) for n in content_nodes if n.name == 'p']
        # Extract tables
        tables = []
        for tbl in [n for n in content_nodes if n.name == 'table']:
            ths = [th.get_text(strip=True) for th in tbl.find_all('th')]
            rows = [
                [td.get_text(strip=True) for td in tr.find_all('td')]
                for tr in tbl.find_all('tr')
            ]
            tables.append({"headers": ths, "rows": rows})
        # Extract images (and download)
        imgs = []
        for img in [n for n in content_nodes if n.name == 'img' and n.get('src')]:
            local = download_image(img['src'], 'images')
            if local:
                imgs.append(local)

        sections.append({
            "level": level,
            "header": h.get_text(strip=True),
            "text": "\n\n".join(texts),
            "tables": tables,
            "images": imgs
        })

    # 6) Final payload
    payload = {
        "url": soup.find("link", rel="canonical")["href"],
        "title": soup.title.string.strip(),
        "metadata": metadata,
        "content": content_html,
        "headers": headers,
        "toc_links": toc_links,
        "sections": sections
    }

    logger.info(
        f"→ Parsed page {payload['title']!r}: "
        f"{len(toc_links)} TOC links, "
        f"{len(headers)} headers, "
        f"{len(sections)} sections"
    )
    return payload

def parse():
    """Parse all HTML files in ``data/raw`` and write JSON to ``data/processed``."""
    raw_dir = 'data/raw'
    proc_dir = 'data/processed'
    os.makedirs(proc_dir, exist_ok=True)
    logger.info(f"1) Parsing raw HTML from {raw_dir}")
    for fname in os.listdir(raw_dir):
        if not fname.endswith('.html'):
            continue
        logger.info(f"2) Processing {fname}")
        path = os.path.join(raw_dir, fname)
        html = load_raw(path)
        page = parse_html(html)
        out_name = fname.replace('.html', '.json')
        save_processed(proc_dir, out_name, page)
        logger.info(f"   → Saved {out_name}")

if __name__ == '__main__':
    parse()
