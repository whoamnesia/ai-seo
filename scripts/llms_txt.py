#!/usr/bin/env python3
"""astudio-ai-seo · llms_txt.py — validate or draft an llms.txt (spec: https://llmstxt.org).

  python3 llms_txt.py check llms.txt            # or a URL
  python3 llms_txt.py draft --name "Brand" --summary "One line" --sitemap https://site.ru/sitemap.xml [--max 40]
  python3 llms_txt.py draft --name "Brand" --summary "..." --urls urls.txt > llms.txt

check: structure per spec (H1 required and first; optional blockquote; H2 sections of
"- [name](url): notes" links; "Optional" section), broken link syntax, duplicates,
relative URLs, size. draft: prints a skeleton to stdout for a human to edit; it never
writes into a site. Network: only when a URL or sitemap URL is given (GET).
Policy reminder: Google says it ignores llms.txt; no engine documents ranking use.
It helps coding agents and doc readers. Report presence, assign it no ranking weight.
"""
import argparse, re, sys, pathlib, urllib.request, xml.etree.ElementTree as ET
from collections import OrderedDict
from urllib.parse import urlparse

UA = {"User-Agent": "astudio-ai-seo/1.0 (+https://astudio.one)"}
LINK = re.compile(r"^-\s+\[([^\]]+)\]\(([^)\s]+)\)(?::\s*(.*))?$")


def fetch(src):
    if re.match(r"^https?://", src):
        with urllib.request.urlopen(urllib.request.Request(src, headers=UA), timeout=20) as r:
            return r.read().decode("utf-8", "replace")
    return pathlib.Path(src).read_text(encoding="utf-8")


def check(text):
    problems, notes = [], []
    lines = text.lstrip("﻿").splitlines()
    body = [l for l in lines if l.strip()]
    if not body or not body[0].startswith("# "):
        problems.append("first non-empty line must be the H1 with the project/site name ('# Name')")
    if sum(1 for l in lines if re.match(r"^#\s", l)) > 1:
        problems.append("only one H1 is allowed")
    if len(body) > 1 and body[1].startswith(">"):
        notes.append("summary blockquote present")
    else:
        notes.append("no summary blockquote (optional, but recommended: one sentence on what the site is)")
    section, links, seen = None, 0, set()
    for i, l in enumerate(lines, 1):
        if l.startswith("### ") or l.startswith("#### "):
            problems.append(f"line {i}: only H1 and H2 headings are defined by the spec")
        if l.startswith("## "):
            section = l[3:].strip()
            continue
        if l.startswith("- "):
            m = LINK.match(l.strip())
            if not m:
                problems.append(f"line {i}: list item is not '- [name](url): notes'")
                continue
            if section is None:
                problems.append(f"line {i}: link before any H2 section")
            url = m.group(2)
            if not re.match(r"^https?://", url):
                notes.append(f"line {i}: relative URL {url}; absolute URLs are safer for agents that copy the file")
            if url in seen:
                problems.append(f"line {i}: duplicate URL {url}")
            seen.add(url)
            links += 1
    if any(re.match(r"^##\s+Optional\s*$", l) for l in lines):
        notes.append("has an 'Optional' section (agents may skip it)")
    size = len(text.encode("utf-8"))
    if size > 200_000:
        problems.append(f"{size} bytes: too large for a context window; move detail into llms-full.txt or .md twins")
    notes.append(f"{links} links, {size} bytes")
    return problems, notes


def sitemap_urls(src, limit):
    out = []
    xml = fetch(src)
    root = ET.fromstring(xml.encode("utf-8"))
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for loc in root.findall(".//s:loc", ns):
        out.append(loc.text.strip())
        if len(out) >= limit:
            break
    return out


def draft(name, summary, urls):
    groups = OrderedDict()
    for u in urls:
        p = urlparse(u)
        seg = [s for s in p.path.split("/") if s]
        key = seg[0] if seg else "main"
        groups.setdefault(key, []).append(u)
    print(f"# {name}\n\n> {summary}\n")
    print("<!-- Edit: one line per page saying what a reader gets there. Delete pages that are thin, duplicated or private. -->\n")
    for key, us in groups.items():
        title = "Main pages" if key == "main" else key.replace("-", " ").capitalize()
        print(f"## {title}\n")
        for u in us:
            last = [s for s in urlparse(u).path.split("/") if s]
            label = (last[-1] if last else name).replace("-", " ").replace(".html", "")
            print(f"- [{label}]({u}): TODO describe")
        print()
    print("## Optional\n\n- [Sitemap](" + (urls[0].split('/')[0] + '//' + urlparse(urls[0]).netloc + '/sitemap.xml' if urls else 'https://example.com/sitemap.xml') + "): full list of pages")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("src")
    d = sub.add_parser("draft"); d.add_argument("--name", required=True); d.add_argument("--summary", required=True)
    d.add_argument("--sitemap"); d.add_argument("--urls"); d.add_argument("--max", type=int, default=40)
    a = ap.parse_args()
    if a.cmd == "check":
        problems, notes = check(fetch(a.src))
        for n in notes: print("·", n)
        for p in problems: print("✗", p)
        print("✓ valid llms.txt" if not problems else f"{len(problems)} problem(s)")
        return 1 if problems else 0
    urls = sitemap_urls(a.sitemap, a.max) if a.sitemap else [l.strip() for l in pathlib.Path(a.urls).read_text().splitlines() if l.strip()][: a.max] if a.urls else []
    draft(a.name, a.summary, urls)
    return 0


if __name__ == "__main__":
    sys.exit(main())
