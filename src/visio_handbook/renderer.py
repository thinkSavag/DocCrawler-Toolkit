# src/visio_handbook/renderer.py

from jinja2 import Environment, FileSystemLoader
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches
import os

def render_md(data_files, template_filename, output_path, context):
    """
    Combine all JSON pages into a single Markdown file.
    """
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_filename)

    # Load all page data
    pages = []
    for f in sorted(data_files):
        with open(f, "r", encoding="utf-8") as fp:
            pages.append(fp.read())

    md = template.render(pages=pages, **context)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fp:
        fp.write(md)

def render_docx(data_files, template_filename, output_path, context):
    """
    Combine all JSON pages into a single Word document.
    """
    tpl = DocxTemplate(os.path.join("templates", template_filename))

    # Prepare context: list of page dicts
    pages = []
    for f in sorted(data_files):
        pages.append(__import__("json").load(open(f, "r", encoding="utf-8")))

    context = { **context, "pages": pages }
    tpl.render(context)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tpl.save(output_path)


# What this does
# #  render_md: Uses Jinja2 to loop over each page’s raw Markdown (or JSON) and outputs one handbook.md.
# #  render_docx: Uses DocxTemplate to merge all page JSON into one Word doc via your visio_handbook_template.docx.