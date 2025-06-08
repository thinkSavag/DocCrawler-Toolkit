# Visio-Handbook

A Python toolkit that crawls Microsoft Visio support pages, extracts headings, text, tables and images, and generates a fully-formatted handbook in Markdown or Word.

---

## 📦 Features

- **Crawl** Visio documentation pages starting from a set of URLs in `configs/crawler.yaml`
- **Parse** out:
  - Page title (`<h1>`)
  - Section headings (`<h2>`, `<h3>`)
  - Paragraph text
  - Tables (converted to JSON → templated Markdown/Word tables)
  - Images (downloaded locally)
- **Render** into:
  - `output/handbook.md`
  - `output/handbook.docx`

---

## 🚀 Quickstart

1. **Clone the repo** (or unzip your code directory):  
   ```bash
   git clone https://github.com/<your-username>/Visio-Handbook.git
   cd Visio-Handbook


---

# Handbook-Generator

A lightweight Python toolkit to crawl web pages, extract structured content (titles, table of contents, sections with text/tables/images), and render polished handbooks in Markdown or Word (`.docx`) via Jinja2/docxtpl templates.

---

## Features

- **Configurable crawl** of one or more start URLs (YAML-driven)
- **Throttled requests** to respect server load
- **Sidebar & in-page TOC** extraction (H1–H3 hierarchy)
- **Section parsing**: paragraphs, HTML tables → JSON
- **Image download** and embedding in final document
- **Multi-format render**: Markdown (`.md`) or Word (`.docx`)
- **Structured logging** with console & timestamped log files
- **Clean directory layout** and `.gitignore` to exclude generated data

---

## Prerequisites

- Python 3.8+  
- Git (to version-control your code)  
- Optional: Word (to view `.docx`)

---

## Installation

```bash
# 1. Clone or create your repo
git clone https://github.com/YourUsername/Handbook-Generator.git
cd Handbook-Generator

# 2. Create & activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
"# DocCrawler-Toolkit" 
"# Visio-Handbook" 
