import os
import time
from collections import deque
import requests

from .utils import setup_logging, save_raw, save_processed
from .parser import parse_html

logger = setup_logging()


def fetch_page(url: str, delay: float) -> str:
    """Download a single page respecting the delay."""
    logger.info(f"Fetching {url!r}")
    resp = requests.get(url)
    time.sleep(delay)
    return resp.text


def crawl(start_urls, delay: float, max_depth: int = 1):
    """Fetch start URLs and follow TOC links breadth-first."""
    raw_dir = "data/raw"
    proc_dir = "data/processed"
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(proc_dir, exist_ok=True)

    queue = deque((url, 0) for url in start_urls)
    seen = set(start_urls)

    while queue:
        url, depth = queue.popleft()
        html = fetch_page(url, delay)
        name = url.rstrip("/").split("/")[-1] + ".html"
        save_raw(raw_dir, name, html)

        page_data = parse_html(html)
        json_name = name.replace(".html", ".json")
        save_processed(proc_dir, json_name, page_data)

        if depth < max_depth:
            for link in page_data.get("toc_links", []):
                if link not in seen:
                    seen.add(link)
                    queue.append((link, depth + 1))

    logger.info("Crawl complete")
