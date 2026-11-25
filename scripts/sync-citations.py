#!/usr/bin/env python3
"""Import generated citation guidance from the independent GREEN authority."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
REPOSITORY = "Green-Phys/green-citations"
DEFAULT_REF = "main"
GENERATED_MARKER = "Generated from Green-Phys/green-citations; do not edit."


def fetch(url: str, accept: str | None = None) -> bytes:
    headers = {"User-Agent": "green-phys-citation-sync"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if accept:
        headers["Accept"] = accept
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def resolve(ref: str) -> str:
    if len(ref) == 40 and all(character in "0123456789abcdef" for character in ref):
        return ref
    payload = fetch(
        f"https://api.github.com/repos/{REPOSITORY}/commits/{ref}",
        "application/vnd.github+json",
    )
    return json.loads(payload)["sha"]


def outputs(commit: str) -> dict[pathlib.Path, bytes]:
    base = f"https://raw.githubusercontent.com/{REPOSITORY}/{commit}"
    guidance = fetch(f"{base}/CITATION.md").decode("utf-8")
    bibtex = fetch(f"{base}/references.bib")
    heading = "# Citing GREEN\n\n"
    if not guidance.startswith(heading):
        raise ValueError("canonical CITATION.md has an unexpected heading")
    guidance = guidance.removeprefix(heading)
    source = f"https://github.com/{REPOSITORY}/tree/{commit}"
    page = f"""---
title: Papers and Citations
linkTitle: Papers and Citations
description: "Green Papers and Citations"
icon: auto-story
weight: 5
---

<!-- {GENERATED_MARKER} -->

Green is released under the MIT license. We ask users to acknowledge GREEN when
it contributes to their work and to cite the original literature for the
scientific methods actually used.

The records and mappings below come from the independent
[GREEN citation authority]({source}) at commit `{commit[:12]}`.

{guidance}"""
    bibtex_header = f"% {GENERATED_MARKER}\n% Source: {source}\n\n".encode("utf-8")
    generated_bibtex = bibtex_header + bibtex
    first_entry = bibtex.decode("utf-8").split("\n\n@", 1)[0] + "\n"
    legacy_entry = first_entry.replace(
        "@article{green-weakcoupling-2025,",
        "@article{ISKAKOV2025109380,",
        1,
    ).encode("utf-8")
    return {
        ROOT / "content/docs/publications/_index.md": page.encode("utf-8"),
        ROOT / "static/data/green-references.bib": generated_bibtex,
        # Preserve the established download URL while moving ownership to the
        # independent authority, including its established BibTeX key. New
        # links use green-references.bib for the complete catalog.
        ROOT / "static/data/iskakov2025.bib": bibtex_header + legacy_entry,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", default=os.environ.get("GREEN_CITATIONS_REF", DEFAULT_REF))
    args = parser.parse_args()

    commit = resolve(args.ref)
    for path, content in outputs(commit).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    print(f"citation-sync-ok: {commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
