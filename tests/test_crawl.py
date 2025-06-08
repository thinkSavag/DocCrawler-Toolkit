import os
import json

from visio_handbook.crawler import crawl
from visio_handbook.utils import load_config


def test_smoke():
    cfg = load_config()
    seed = cfg.get("start_urls", [])[:1]
    crawl(seed, delay=0, max_depth=1)

    raw_files = [f for f in os.listdir("data/raw") if f.endswith(".html")]
    proc_files = [f for f in os.listdir("data/processed") if f.endswith(".json")]
    assert raw_files, "No raw HTML saved"
    assert proc_files, "No processed JSON saved"

    found_header = False
    found_toc = False
    for pf in proc_files:
        with open(os.path.join("data/processed", pf), "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("headers"):
            found_header = True
        if data.get("toc_links"):
            found_toc = True
    assert found_header, "Headers missing"
    assert found_toc, "TOC links missing"
    print("Smoke test passed")


if __name__ == "__main__":
    test_smoke()
