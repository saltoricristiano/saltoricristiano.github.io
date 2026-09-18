#!/usr/bin/env python3
"""Check publication metadata and a Hugo build without network access (Python 3.11+)."""

import argparse
from datetime import date, datetime
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import tomllib
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = set()
        self.refs = []
        self.errors = []
        self.lang = ""
        self.title = ""
        self.in_title = False
        self.main_count = 0
        self.h1_count = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        element_id = attrs.get("id")
        if element_id:
            if element_id in self.ids:
                self.errors.append(f"duplicate id: {element_id}")
            self.ids.add(element_id)
        if tag == "html":
            self.lang = attrs.get("lang", "")
        elif tag == "title":
            self.in_title = True
        elif tag == "main":
            self.main_count += 1
        elif tag == "h1":
            self.h1_count += 1
        if tag == "img" and "alt" not in attrs:
            self.errors.append(f"image is missing alt: {attrs.get('src', '(no src)')}")
        for attr in ("href", "src", "poster"):
            if attr in attrs:
                value = attrs[attr] or ""
                if not value.strip():
                    self.errors.append(f"empty {attr} on <{tag}>")
                else:
                    self.refs.append(value)
        # The site uses local teaser assets; support common responsive image lists too.
        if attrs.get("srcset") and not attrs["srcset"].startswith("data:"):
            self.refs.extend(item.strip().split()[0] for item in attrs["srcset"].split(",") if item.strip())

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def metadata_errors():
    errors = []
    publication_count = 0
    for path in sorted((ROOT / "content" / "publications").glob("*/index.md")):
        label = path.relative_to(ROOT)
        parts = path.read_text(encoding="utf-8").split("+++", 2)
        if len(parts) != 3 or parts[0].strip():
            errors.append(f"{label}: expected TOML front matter between +++ delimiters")
            continue
        try:
            entry = tomllib.loads(parts[1])
        except tomllib.TOMLDecodeError as exc:
            errors.append(f"{label}: {exc}")
            continue
        if "draft" in entry and not isinstance(entry["draft"], bool):
            errors.append(f"{label}: draft must be true or false")
        if entry.get("draft") is True:
            continue
        publication_count += 1
        for field in ("title", "venue", "paper_url"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f"{label}: missing {field}")
        authors = entry.get("authors")
        if not isinstance(authors, list) or not authors or any(not isinstance(a, str) or not a.strip() for a in authors):
            errors.append(f"{label}: authors must list the verified names in paper order")
        year = entry.get("year")
        if type(year) is not int or not 1900 <= year <= 2100:
            errors.append(f"{label}: year must be an integer between 1900 and 2100")
        try:
            entry_date = entry.get("date")
            if isinstance(entry_date, str):
                entry_date = datetime.fromisoformat(entry_date.replace("Z", "+00:00"))
            if not isinstance(entry_date, (date, datetime)) or entry_date.year != year:
                raise ValueError
        except ValueError:
            errors.append(f"{label}: date must be ISO format and match year")
        if "featured" in entry and not isinstance(entry["featured"], bool):
            errors.append(f"{label}: featured must be true or false")
        for field in ("paper_url", "code_url", "project_url"):
            if value := entry.get(field):
                parsed = urlsplit(str(value))
                if parsed.scheme not in {"https", "http"} or not parsed.netloc:
                    errors.append(f"{label}: {field} must be a full http(s) URL")
        if "bibtex" in entry and not isinstance(entry["bibtex"], str):
            errors.append(f"{label}: bibtex must be a string when supplied")
        elif entry.get("bibtex", "").strip() and not entry["bibtex"].lstrip().startswith("@"):
            errors.append(f"{label}: bibtex must contain a citation beginning with @")
        if image := entry.get("image"):
            image_path = (ROOT / "static" / str(image).lstrip("/")).resolve()
            if not image_path.is_relative_to((ROOT / "static").resolve()) or not image_path.is_file():
                errors.append(f"{label}: teaser does not exist in static/: {image}")
            if not str(entry.get("image_alt", "")).strip():
                errors.append(f"{label}: a teaser needs descriptive image_alt")
        if animation := entry.get("animation"):
            animation_path = (ROOT / "static" / str(animation).lstrip("/")).resolve()
            if not animation_path.is_relative_to((ROOT / "static").resolve()) or not animation_path.is_file():
                errors.append(f"{label}: animation does not exist in static/: {animation}")
            elif animation_path.read_bytes()[:6] not in (b"GIF87a", b"GIF89a"):
                errors.append(f"{label}: animation must be a valid GIF asset")
            if not entry.get("image"):
                errors.append(f"{label}: animation requires a static image fallback")
            if not str(entry.get("animation_alt", "")).strip():
                errors.append(f"{label}: animation needs descriptive animation_alt")
    if not publication_count:
        errors.append("No published publication entries found.")
    for name in ("profile", "news"):
        path = ROOT / "data" / f"{name}.json"
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"data/{name}.json: {exc}")
    return errors, publication_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-dir", type=Path, default=ROOT / "public")
    parser.add_argument("--base-url", help="Use the same URL passed to hugo --baseURL.")
    args = parser.parse_args()
    public = args.public_dir.resolve()
    base_url = args.base_url
    if not base_url:
        for name in ("hugo.toml", "config.toml"):
            if (ROOT / name).is_file():
                config = tomllib.loads((ROOT / name).read_text(encoding="utf-8"))
                base_url = config.get("baseURL") or config.get("baseurl")
                if base_url:
                    break
    base_url = (base_url or "https://saltoricristiano.github.io/").rstrip("/") + "/"
    base = urlsplit(base_url)
    if base.scheme not in {"http", "https"} or not base.netloc:
        parser.error("--base-url must be a full http(s) URL")
    errors, publication_count = metadata_errors()
    if not (public / "index.html").is_file():
        errors.append(f"Missing {public / 'index.html'}; run hugo first.")
    pages = {}
    for path in sorted(public.rglob("*.html")):
        page = Page(path)
        page.feed(path.read_text(encoding="utf-8"))
        pages[path] = page
        label = path.relative_to(public)
        if not page.lang:
            page.errors.append("<html> needs a language")
        if not page.title.strip():
            page.errors.append("page title is missing")
        if page.main_count != 1:
            page.errors.append("expected one <main> landmark")
        if page.h1_count != 1:
            page.errors.append("expected one <h1> heading")
        errors.extend(f"{label}: {error}" for error in page.errors)

    def check_ref(source, ref):
        if ref.startswith(("data:", "mailto:", "tel:")):
            return
        origin = urljoin(base_url, source.relative_to(public).as_posix())
        resolved = urlsplit(urljoin(origin, ref))
        if resolved.scheme not in {"http", "https"}:
            errors.append(f"{source.relative_to(public)}: unsupported URL scheme: {ref}")
            return
        if resolved.netloc != base.netloc:
            return  # External reachability needs a separate, online review.
        path = unquote(resolved.path)
        prefix = unquote(base.path)
        if path == prefix.rstrip("/"):
            path += "/"
        if not path.startswith(prefix):
            errors.append(f"{source.relative_to(public)}: link escapes base URL path: {ref}")
            return
        target = (public / path[len(prefix):]).resolve()
        if not target.is_relative_to(public):
            errors.append(f"{source.relative_to(public)}: invalid local path: {ref}")
            return
        if target.is_dir():
            target /= "index.html"
        if not target.is_file():
            errors.append(f"{source.relative_to(public)}: missing local target: {ref}")
        elif resolved.fragment and target in pages and unquote(resolved.fragment) not in pages[target].ids:
            errors.append(f"{source.relative_to(public)}: missing anchor target: {ref}")

    for path, page in pages.items():
        for ref in page.refs:
            check_ref(path, ref)
    for path in public.rglob("*.css"):
        for match in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", path.read_text(encoding="utf-8")):
            check_ref(path, match.group(1).strip())
    if errors:
        print("Website validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {publication_count} publications and {len(pages)} HTML pages; local links, assets, anchors, and basic markup passed.")
    print("External URL availability and citation accuracy require source review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
