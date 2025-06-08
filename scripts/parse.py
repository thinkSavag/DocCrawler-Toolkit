import json
import logging
import os

from bs4 import BeautifulSoup

from utils import load_raw, save_processed, download_image, setup_logging

logger = setup_logging()


def parse_html(html):
    """Extract title, TOC and section data from a Visio support page."""
    soup = BeautifulSoup(html, 'html.parser')
    data = {
        'title': soup.h1.get_text(strip=True) if soup.h1 else '',
        'toc': [],
        'sections': []
    }

    nav = soup.select_one('div.supLeftNavCategory')
    if nav:
        title_link = nav.select_one('div.supLeftNavCategoryTitle > a.supLeftNavLink')
        if title_link:
            data['toc'].append({'level': 2,
                                'text': title_link.get_text(strip=True),
                                'link': title_link['href']})
        for a in nav.select('ul.supLeftNavArticles a.supLeftNavLink'):
            data['toc'].append({'level': 2,
                                'text': a.get_text(strip=True),
                                'link': a['href']})

    for h in soup.find_all(['h2', 'h3']):
        lvl = 2 if h.name == 'h2' else 3
        data['toc'].append({'level': lvl,
                            'text': h.get_text(strip=True),
                            'link': None})
        content = []
        for sib in h.find_next_siblings():
            if sib.name in ['h2', 'h3']:
                break
            content.append(sib)
        texts = [c.get_text(strip=True) for c in content if c.name == 'p']
        tables = []
        for tbl in content:
            if tbl.name == 'table':
                headers = [th.get_text(strip=True) for th in tbl.find_all('th')]
                rows = [[td.get_text(strip=True) for td in tr.find_all('td')]
                        for tr in tbl.find_all('tr')]
                tables.append({'headers': headers, 'rows': rows})
        imgs = []
        for img in content:
            if img.name == 'img' and img.get('src'):
                local = download_image(img['src'], 'images')
                if local:
                    imgs.append(local)
        data['sections'].append({'header': h.get_text(strip=True),
                                'text': "\n\n".join(texts),
                                'tables': tables,
                                'images': imgs})

    logger.info(f"→ Parsed page {data['title']!r} with "
                f"{len(data['toc'])} TOC entries and "
                f"{len(data['sections'])} sections")
    return data


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
