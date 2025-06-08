import os
import json
from bs4 import BeautifulSoup
from utils import load_raw, save_processed, download_image

def parse_html(html):
      """
    Extract:
     - page title
     - toc: list of {level, text, link}
     - sections: list of {header, text, tables, images}
    """
    soup = BeautifulSoup(html, 'html.parser')
    data = {
        'title': soup.h1.get_text(strip=True) if soup.h1 else '',
        'toc': [],
        'sections': []
    }

    # ── Pull the left-nav sidebar as H2 entries ──
    nav = soup.select_one('div.supLeftNavCategory')
    if nav:
        # Category title
        title_link = nav.select_one('div.supLeftNavCategoryTitle > a.supLeftNavLink')
        if title_link:
            data['toc'].append({
                'level': 2,
                'text': title_link.get_text(strip=True),
                'link': title_link['href']
            })
        # Sub-articles
        for a in nav.select('ul.supLeftNavArticles a.supLeftNavLink'):
            data['toc'].append({
                'level': 2,
                'text': a.get_text(strip=True),
                'link': a['href']
            })

    # ── In-page H2 and H3 headers ──
    for h in soup.find_all(['h2', 'h3']):
        lvl = 2 if h.name == 'h2' else 3
        data['toc'].append({
            'level': lvl,
            'text': h.get_text(strip=True),
            'link': None
        })
        # Gather all content until the next H2/H3
        content = []
        for sib in h.find_next_siblings():
            if sib.name in ['h2', 'h3']:
                break
            content.append(sib)
        # Extract text from paragraphs in this section
        texts = [c.get_text(strip=True) for c in content if c.name == 'p']
        # Extract tables in this section
        tables = []
        for tbl in content:
            if tbl.name == 'table':
                headers = [th.get_text(strip=True) for th in tbl.find_all('th')]
                rows = [[td.get_text(strip=True) for td in tr.find_all('td')] 
                        for tr in tbl.find_all('tr')]
                tables.append({'headers': headers, 'rows': rows})
        # Download images in this section
        imgs = []
        for img in content:
            if img.name == 'img' and img.get('src'):
                local = download_image(img['src'], 'images')
                if local:
                    imgs.append(local)
        # Append the section data
        data['sections'].append({
            'header': h.get_text(strip=True),
            'text': "\n\n".join(texts),
            'tables': tables,
            'images': imgs
        })
    return data

def parse():
    raw_dir = 'data/raw'
    proc_dir = 'data/processed'
    os.makedirs(proc_dir, exist_ok=True)
    for fname in os.listdir(raw_dir):
        if not fname.endswith('.html'):
            continue
        path = os.path.join(raw_dir, fname)
        html = load_raw(path)
        data = parse_html(html)
        out_name = fname.replace('.html', '.json')
        save_processed(proc_dir, out_name, data)
        print(f"Processed {fname} -> {out_name}")

if __name__ == '__main__':
    parse()
