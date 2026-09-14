#!/usr/bin/env python3
"""Check the deployable report for broken local references and unintended files.

Standard library only. This validates the publication surface, not research claims.
Run from any directory: python3 scripts/validate_report_site.py
"""

from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys
import re


SITE = Path(__file__).resolve().parents[1] / "site"
PRIVATE_REFERENCES = re.compile(
    r"""github\.com/mlhouse-project/(?!website(?:[/#?\s\"'<>]|$))"""
    r"|github\.com/user-attachments/files/"
    r"|\b(?:PR|pull\s+request|issue)\s*#\s*\d+\b"
    r"|\b(?:audit-summary|observed-examples)\.md\b",
    re.IGNORECASE,
)


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.references = []
        self.in_reference_entry = False
        self.errors = []
        self.headings = []
        self.captions = 0
        self.tables = 0
        self.has_lang = False
        self.has_title = False
        self.has_viewport = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "html":
            self.has_lang = bool(attrs.get("lang"))
        if tag == "title":
            self.has_title = True
        if tag == "meta" and attrs.get("name") == "viewport":
            self.has_viewport = True
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings.append(int(tag[1]))
        if tag == "img" and "alt" not in attrs:
            self.errors.append("Image missing alt attribute")
        if tag == "table":
            self.tables += 1
        if tag == "caption":
            self.captions += 1
        if tag == "th" and attrs.get("scope") not in ("row", "col", "rowgroup", "colgroup"):
            self.errors.append("Table header missing valid scope")
        if tag == "iframe":
            self.errors.append("Unexpected embedded external content")
        if tag == "li" and attrs.get("id", "").startswith("ref-"):
            self.in_reference_entry = True
        if tag == "a" and self.in_reference_entry:
            if urlsplit(attrs.get("href", "")).scheme != "https":
                self.errors.append("Bibliography entries must link to external sources")
        for key in ("href", "src"):
            if key in attrs:
                self.references.append(attrs[key])

    def handle_endtag(self, tag):
        if tag == "li":
            self.in_reference_entry = False


def validate():
    errors = []
    pages = {}
    allowed_suffixes = {".html", ".css", ".js", ".svg", ".jpg", ".md"}
    for path in SITE.rglob("*"):
        if path.is_symlink():
            errors.append(f"Symlink in publication directory: {path.relative_to(SITE)}")
        elif path.is_file():
            if path.name in {"audit-summary.md", "observed-examples.md"}:
                errors.append(f"Internal working note in publication directory: {path.relative_to(SITE)}")
            if path.name not in {".nojekyll", "CNAME"} and path.suffix not in allowed_suffixes:
                errors.append(f"Unexpected published file: {path.relative_to(SITE)}")
            if path.suffix in {".html", ".css", ".js", ".svg", ".md"}:
                content = path.read_text(encoding="utf-8")
                if PRIVATE_REFERENCES.search(unquote(unescape(content))):
                    errors.append(f"Private working reference in published file: {path.relative_to(SITE)}")
            if path.suffix == ".html":
                page = Page(path)
                page.feed(content)
                page.close()
                pages[path.resolve()] = page
                if "<!-- REPORT_SECTIONS -->" in content:
                    errors.append("Unfinished report section marker")
    if (SITE / "index.html").resolve() not in pages:
        errors.append("Missing index.html")

    reference_count = 0
    for path, page in pages.items():
        name = str(path.relative_to(SITE))
        errors.extend(f"{name}: {error}" for error in page.errors)
        for value, count in Counter(page.ids).items():
            if count > 1:
                errors.append(f"{name}: duplicate ID {value}")
        if not all((page.has_lang, page.has_title, page.has_viewport)):
            errors.append(f"{name}: missing language, title, or viewport metadata")
        if page.headings.count(1) != 1:
            errors.append(f"{name}: expected one primary heading")
        if any(b > a + 1 for a, b in zip(page.headings, page.headings[1:])):
            errors.append(f"{name}: skipped heading level")
        if page.tables != page.captions:
            errors.append(f"{name}: each data table needs a caption")
        for reference in page.references:
            reference_count += 1
            url = urlsplit(reference)
            if (
                url.scheme == "mailto"
                and re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", url.path)
                and not any((url.netloc, url.query, url.fragment))
            ):
                continue
            if url.scheme or url.netloc:
                # Preserve an original HTTP source URL for a crawled example;
                # bibliography links above still require HTTPS.
                if url.scheme not in {"http", "https"} or url.hostname in {"localhost", "127.0.0.1"}:
                    errors.append(f"{name}: invalid external publication link: {reference}")
                continue
            if url.path.startswith("/"):
                errors.append(f"{name}: root-relative reference breaks project Pages paths: {reference}")
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not target.is_relative_to(SITE):
                errors.append(f"{name}: reference escapes the publication directory: {reference}")
                continue
            if not target.is_file():
                errors.append(f"{name}: missing local file: {reference}")
                continue
            if url.fragment and (target not in pages or unquote(url.fragment) not in pages[target].ids):
                errors.append(f"{name}: missing anchor: {reference}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    size = sum(path.stat().st_size for path in SITE.rglob("*") if path.is_file())
    print(f"Report valid: {len(pages)} HTML page(s), {reference_count} references, {size:,} published bytes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(validate())
