import argparse

from visio_handbook.crawl import crawl, render_md, render_docx
from visio_handbook.utils import (
    load_config,
    setup_logging,
    get_processed_files,
    build_context,
)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="visio-handbook")
    parser.add_argument("--format", choices=["md", "docx"], default="md")
    args = parser.parse_args(argv)

    logger = setup_logging()
    cfg = load_config()
    start_urls = cfg.get("start_urls", [])
    delay = cfg.get("delay_seconds", 1.0)

    crawl(start_urls, delay)

    files = get_processed_files()
    context = build_context(files)

    if args.format == "md":
        render_md(context, "templates/handbook_template.md", "output/handbook.md")
    else:
        render_docx(context, "templates/handbook_template.docx", "output/handbook.docx")


if __name__ == "__main__":
    main()
