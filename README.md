# Visio-Handbook

A Python toolkit that crawls Microsoft Support’s Visio documentation—following sidebar TOC links breadth-first—extracts metadata, article content, headers, tables, and images, and renders a structured handbook in Markdown or Word.

---

## 📦 Features

+- **Configurable Crawl**  
+  - Breadth-first over H1/H2 landing-page links *and* sidebar TOC links (restricted to support.microsoft.com)  
+- **Strict Parsing Scope**  
+  - Metadata from `<head>` + content from `<article>`  
+  - Collect all `<h1>`–`<h6>` as `headers`  
+  - Group `<h2>`/`<h3>` sections with their text, tables, and images  
+- **Duplicate-safe**  
+  - Skips any URL already fetched, even if referenced multiple times  
+- **Image Handling**  
+  - Downloads all `<img>` assets locally and rewrites references  
+- **Multi-format Rendering**  
+  - Markdown (`.md`) via Jinja2 templates  
+  - Word (`.docx`) via docxtpl and `handbook_template.docx`  
+- **Structured Logging**  
+  - `logger.info` at each major step with timestamps  


---

## 🚀 Quickstart

### 1. Clone & setup

 ```bash
 git clone https://github.com/<your-username>/Visio-Handbook.git
 cd Visio-Handbook
 python -m venv .venv
 # Windows:
 .venv\Scripts\activate.bat
 # macOS/Linux:
 source .venv/bin/activate
  # Install the package in editable mode
  pip install -e ".[dev]"
 ```

 ### 2. Configure
 
 * Edit configs/crawler.yaml:

 ```bash
 start_urls:
  - https://support.microsoft.com/.../select-a-template-in-visio-...
delay_seconds: 1.0
 ```

 ### 3. Run the crawler

 ```bash
 # Markdown output
 visio-handbook --format md
 # Word (.docx) output
visio-handbook --format docx
```

 ### 4. Run tests

 ```bash
 pytest -q
 ```

 ### 5. Inspect results
- Raw HTML: data/raw/
- Parsed JSON: data/processed/
- Final handbook: output/handbook.md or output/handbook.docx

---

Feel free to adjust any URLs or add example screenshots of the generated handbook. This revision makes clear the BFS-TOC behavior, parsing scope, duplicate filtering, and dual-format output.
