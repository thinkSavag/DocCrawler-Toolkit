import json
import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Inches

from .utils import setup_logging

logger = setup_logging()


def render_md(data_files, template_path, output_path, context):
    """Render collected JSON pages into a Markdown handbook."""
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))
    pages = []
    for path in sorted(data_files):
        with open(path, "r", encoding="utf-8") as f:
            pages.append(json.load(f))

    ctx = dict(context)
    ctx["pages"] = pages

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template.render(ctx))
    logger.info(f"Rendered Markdown to {output_path}")


def render_docx(data_files, template_path, output_path, context):
    """Render collected JSON pages into a Word handbook."""
    doc = DocxTemplate(template_path)
    pages = []
    for path in sorted(data_files):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for sec in data.get("sections", []):
            sec["images"] = [InlineImage(doc, img, width=Inches(3))
                             for img in sec.get("images", [])
                             if os.path.exists(img)]
        pages.append(data)

    ctx = dict(context)
    ctx["pages"] = pages

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.render(ctx)
    doc.save(output_path)
    logger.info(f"Rendered Word doc to {output_path}")
