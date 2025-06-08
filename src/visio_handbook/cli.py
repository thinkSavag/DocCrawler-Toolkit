import argparse
import os
from datetime import datetime

from .utils import (
    load_config,
    setup_logging,
    get_processed_files,
    build_context,
)
from .crawler import crawl
from .renderer import render_md, render_docx

logger = setup_logging()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Crawl Microsoft Support and render a handbook")
    parser.add_argument('--format', choices=['md', 'docx'], help='Output format. If omitted you will be prompted')
    parser.add_argument('--max-depth', type=int, default=1, help='Maximum crawl depth for TOC links')
    parser.add_argument('--delay', type=float, help='Delay between requests in seconds')
    args = parser.parse_args(argv)

    fmt = args.format
    if not fmt:
        while True:
            ans = input("Select output format (md/docx): ").strip().lower()
            if ans in ("md", "docx"):
                fmt = ans
                break
            print("Please enter 'md' or 'docx'.")
    args.format = fmt

    cfg = load_config()
    start_urls = cfg.get("start_urls", [])
    delay = args.delay if args.delay is not None else cfg.get("delay_seconds", 1.0)

    crawl(start_urls, delay, max_depth=args.max_depth)

    data_files = get_processed_files()

    context = build_context(cfg)
    context.update({
        "date": datetime.now().strftime("%Y-%m-%d"),
    })

    template_dir = "templates"
    if args.format == 'md':
        template = os.path.join(template_dir, 'visio_handbook_template.md')
        render_md(data_files, template, 'output/handbook.md', context)
    else:
        template = os.path.join(template_dir, 'visio_handbook_template.docx')
        render_docx(data_files, template, 'output/handbook.docx', context)


if __name__ == '__main__':
    main()
