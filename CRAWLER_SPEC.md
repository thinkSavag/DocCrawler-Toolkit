# Crawler Specification

## Rule 1: Follow only `support.microsoft.com` links  
## Rule 2: Delay 1 sec between requests  
## Rule 3: Save raw HTML under `data/raw/`  
## Rule 4: Strictly parse **only**:
   - `<head>` metadata (outside the `<article>`)  
   - `<article>` content  
   *(aside from extracting the TOC sidebar)*  
## Rule 5: Exception—extract TOC sidebar content into JSON (title + link list)  
## Rule 6: Download images locally and update references  
## Rule 7: Write parsed JSON files to `data/processed/`  
## Rule 8: Emit `logger.info` messages at every major step  
## Rule 9: Render all pages with `visio_handbook_template.md` **or** `visio_handbook_template.docx` into `/output/handbook.*`  

---

## What Needs To Be Done Now (Visio-Specific)

1. **Seed from Landing-Page Headings**  
   - On the Visio “Intro” landing page, treat each `<h1>` as a chapter and each nested `<h2>` as a sub-chapter.  
   - While you collect the `<h1>` text and `<h2>` text, also grab their `href` targets (the links).

2. **Expand BFS to Chapter & Sub-Chapter URLs**  
   - After enqueuing your initial `start_urls`, immediately enqueue every link found in those H1/H2 elements.  
   - As each chapter/sub-chapter page is fetched, apply the same `<head>`/`<article>` parse rules.

3. **Reflect the Book-Like Structure in JSON**  
   - Your JSON payload for each page should include:  
     ```json
     {
       "chapter":    "<h1 text>",
       "subChapter": "<h2 text or null>",
       "url":        "<canonical URL>",
       …
     }
     ```  
   - This ensures downstream rendering can nest sections under the correct chapter headings.

4. **Avoid Duplicate Crawls**  
   - Maintain a global `seen` set of URLs.  
   - Before enqueueing any link—from landing-page H1/H2 or sidebar TOC—check `if url not in seen:`.  
   - Once a URL has been fetched & parsed, skip it on any subsequent discovery.

5. **Verify End-to-End**  
   - Run the crawler and inspect `data/processed/` JSON:  
     - You should see one file per unique H1 or H2 page.  
     - Each JSON should carry its `chapter` and (if applicable) `subChapter` fields.  
   - Finally, render the handbook and confirm that chapters/subchapters appear in the correct order and hierarchy.

---

With these steps in place, your Visio handbook will mirror the structure of Microsoft’s “Visio training” sidebar—capturing every Intro-to-Visio topic exactly once, in the right nested order.
