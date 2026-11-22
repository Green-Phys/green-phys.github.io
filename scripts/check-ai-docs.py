#!/usr/bin/env python3
"""Check the published machine-oriented GREEN documentation index."""

from __future__ import annotations

import pathlib
import re
import sys
from urllib.parse import urlparse


ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = ROOT / "static/llms.txt"
LINK = re.compile(r"^- \[([^]]+)]\((https://green-phys\.org/[^)]+)\): (.+)$")
SKILL_URL = (
    "https://github.com/Green-Phys/green-mbpt/blob/main/"
    ".agents/skills/green-mbpt-run/SKILL.md"
)
AUTHORITY_URL = "https://github.com/Green-Phys/green-citations"
GUIDANCE_URL = f"{AUTHORITY_URL}/blob/main/CITATION.md"
REQUIRED_CITATION_URLS = {
    "https://green-phys.org/docs/publications/",
    "https://green-phys.org/docs/acknowledgment/",
    "https://green-phys.org/data/green-references.bib",
}
GENERATED_MARKER = "Generated from Green-Phys/green-citations; do not edit."


def content_target(path: str) -> pathlib.Path | None:
    clean = path.strip("/")
    if not clean:
        return ROOT / "content/_index.md"
    direct = ROOT / "content" / f"{clean}.md"
    index = ROOT / "content" / clean / "_index.md"
    if direct.is_file():
        return direct
    if index.is_file():
        return index
    static = ROOT / "static" / clean
    if static.is_file():
        return static
    return None


def main() -> int:
    errors: list[str] = []
    if not INDEX.is_file():
        print("missing static/llms.txt", file=sys.stderr)
        return 1

    text = INDEX.read_text(encoding="utf-8")
    urls: list[str] = []
    for number, line in enumerate(text.splitlines(), 1):
        if not line.startswith("- ["):
            continue
        if SKILL_URL in line:
            if not line.partition("): ")[2].strip():
                errors.append(f"line {number}: skill link has no description")
            continue
        if AUTHORITY_URL in line:
            if not line.partition("): ")[2].strip():
                errors.append(f"line {number}: citation authority link has no description")
            continue
        match = LINK.match(line)
        if not match:
            errors.append(f"line {number}: malformed or undescribed index link")
            continue
        _, url, description = match.groups()
        if not description.strip():
            errors.append(f"line {number}: empty link description")
        if url in urls:
            errors.append(f"line {number}: repeated URL: {url}")
        urls.append(url)
        target = content_target(urlparse(url).path)
        if target is None:
            errors.append(f"line {number}: no Hugo content for {url}")

    if not urls:
        errors.append("static/llms.txt has no local documentation links")
    if SKILL_URL not in text:
        errors.append("static/llms.txt does not link the green-mbpt-run skill")
    for url in (AUTHORITY_URL, GUIDANCE_URL):
        if url not in text:
            errors.append(f"static/llms.txt does not link citation authority: {url}")
    missing_citations = sorted(REQUIRED_CITATION_URLS.difference(urls))
    for url in missing_citations:
        errors.append(f"static/llms.txt does not link required citation guidance: {url}")

    for relative in (
        "content/docs/publications/_index.md",
        "static/data/green-references.bib",
        "static/data/iskakov2025.bib",
    ):
        generated = ROOT / relative
        if not generated.is_file() or GENERATED_MARKER not in generated.read_text(
            encoding="utf-8"
        ):
            errors.append(f"missing generated citation marker: {relative}")

    if errors:
        print("AI documentation validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"ai-docs-ok: {len(urls)} local documentation links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

