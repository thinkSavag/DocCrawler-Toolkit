# Crawler Specification

## Rule 1: Follow only `support.microsoft.com` links
## Rule 2: Delay 1 sec between requests
## Rule 3: Save raw HTML under `data/raw/`
## Rule 4: Parse pages into JSON with title, TOC and sections
## Rule 5: Download images locally and update references
## Rule 6: Write parsed JSON files to `data/processed/`
## Rule 7: Emit `logger.info` messages at every major step
## Rule 8: Render all pages with `handbook_template.md` into `output/handbook.md`
