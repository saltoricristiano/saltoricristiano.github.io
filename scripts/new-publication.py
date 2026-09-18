#!/usr/bin/env python3
"""Create a publication draft without inventing citation metadata."""

import argparse
import json
from pathlib import Path
import re
import unicodedata


ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--year", required=True, type=int)
    parser.add_argument("--venue", required=True)
    parser.add_argument("--slug", help="Optional directory name, such as my-paper")
    args = parser.parse_args()
    if not args.title.strip() or not args.venue.strip():
        parser.error("Title and venue must not be empty.")
    if not 1900 <= args.year <= 2100:
        parser.error("Year must be between 1900 and 2100.")
    normalized = unicodedata.normalize("NFKD", args.title).encode("ascii", "ignore").decode()
    slug = args.slug or re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        parser.error("Use a slug containing lowercase letters, digits, and single hyphens.")
    destination = ROOT / "content" / "publications" / slug
    try:
        destination.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error(f"Publication already exists: {destination.relative_to(ROOT)}")
    quote = lambda value: json.dumps(value, ensure_ascii=False)
    content = f'''+++
title = {quote(args.title.strip())}
date = "{args.year}-01-01"
year = {args.year}
venue = {quote(args.venue.strip())}
draft = true
featured = false
authors = []
paper_url = ""
# code_url = ""
# project_url = ""
# image = "images/publications/{slug}.webp"
# image_alt = "Describe what the teaser shows."
# Copy the exact BibTeX from the paper's publisher or author project page.
bibtex = \'\'\'
\'\'\'
+++

'''
    target = destination / "index.md"
    target.write_text(content, encoding="utf-8")
    print(f"Created {target.relative_to(ROOT)}")
    print("Fill in authors, paper URL, and verified citation. Add an optional teaser.")
    print("Preview with hugo server --buildDrafts. Set draft = false when ready.")


if __name__ == "__main__":
    main()
