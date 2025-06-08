# Crawler Specification

1. **Scope**  
   - Only crawl content within `<main>…</main>`.
   - Follow all links in your left-nav (`div.supLeftNavCategory…`).

2. **TOC Extraction**  
   - H1 titles in nav → level 2 entries  
   - Sub-articles in nav (the `<ul.supLeftNavArticles>`) → level 2 entries  
   - In-page H2 → level 2, H3 → level 3 entries  
   - Include text and `[link]` if `href` present

3. **Section Content**  
   - Gather all siblings until next H2/H3  
   - Extract paragraphs, tables, images  
   - Download images locally and reference by path

4. **Nesting**  
   - Nest multi-level nav entries accordingly (repeat until no more new links)

5. **Logging**  
   - At each major step (config load, page fetch, TOC parse, sections parse, image download, template render), emit a `logger.info("…")` call.

6. **Output**  
   - Raw HTML in `data/raw/…`  
   - JSON in `data/processed/…`  
   - Final markdown in `output/handbook.md`
