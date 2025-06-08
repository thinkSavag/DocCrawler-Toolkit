# src/visio_handbook/cli.py
import argparse
from visio_handbook.crawler import crawl
from visio_handbook.utils import load_config, get_processed_files, build_context
from visio_handbook.renderer import render_md, render_docx

def main():
    parser = argparse.ArgumentParser(prog="visio-handbook")
    parser.add_argument(
        "--format", choices=["md", "docx"], default="md",
        help="Output format"
    )
    parser.add_argument(
        "--max-depth", type=int, default=1,
        help="Maximum crawl depth for TOC links"
    )
    parser.add_argument(
        "--delay", type=float, default=1.0,
        help="Delay between requests in seconds"
    )

    args = parser.parse_args()
    cfg = load_config()  # loads configs/crawler.yaml

    crawl(cfg["start_urls"], args.delay, args.max_depth)

    data_files = get_processed_files()
    context = build_context(cfg)

    if args.format == "md":
        render_md(
            data_files,
            "visio_handbook_template.md",
            "output/handbook.md",
            context
        )
    else:
        render_docx(
            data_files,
            "visio_handbook_template.docx",
            "output/handbook.docx",
            context
        )

if __name__ == "__main__":
    main()
