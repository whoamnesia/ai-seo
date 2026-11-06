#!/usr/bin/env python3
"""astudio-ai-seo · schema_lint.py — lint schema.org JSON-LD in an HTML page (file or URL).

  python3 schema_lint.py page.html
  python3 schema_lint.py https://site.ru/product/1 --json

Checks: JSON parses; @context is schema.org; types retired from Google rich results
(FAQPage, HowTo and the 2025 batch) are flagged with what to do; recommended
properties for the types that still produce rich results; values that must be
visible on the page (name, price, rating) actually appear in the visible text;
Organization/LocalBusiness have sameAs/url/logo. Never executes page scripts.
Network: one GET if a URL is given. Writes nothing.
"""
import argparse, json, re, sys, pathlib, urllib.request
from html.parser import HTMLParser

UA = {"User-Agent": "astudio-ai-seo/1.0 (+https://astudio.one)"}

RETIRED = {
    "FAQPage": "FAQ rich results stopped showing in Google Search on 2026-05-07. Keep only if it mirrors visible Q&A for other consumers; expect no Google SERP effect.",
    "HowTo": "HowTo rich results were removed in 2023. No Google effect; keep only if it mirrors visible steps.",
    "ClaimReview": "Retired from Google rich results 2025-06-12.",
    "EstimatedSalary": "Retired 2025-06-12; use JobPosting.baseSalary.",
    "LearningResource": "Learning Video retired 2025-06-12; use VideoObject.",
    "SpecialAnnouncement": "Retired 2025-06-12.",
    "Vehicle": "Vehicle Listing retired 2025-06-12; use Product with Offer.",
    "Book": "Book Actions retired 2025-06-12 (Book markup itself is still valid schema.org).",
}
RECOMMENDED = {
    "Organization": ["name", "url", "logo", "sameAs"],
    "LocalBusiness": ["name", "address", "telephone", "openingHoursSpecification", "geo", "url"],
    "Product": ["name", "image", "description", "offers"],
    "Offer": ["price", "priceCurrency", "availability"],
    "Article": ["headline", "author", "datePublished", "dateModified", "image"],
    "NewsArticle": ["headline", "author", "datePublished", "dateModified", "image"],
    "BlogPosting": ["headline", "author", "datePublished", "dateModified"],
    "BreadcrumbList": ["itemListElement"],
    "VideoObject": ["name", "thumbnailUrl", "uploadDate", "description"],
    "Event": ["name", "startDate", "location"],
    "JobPosting": ["title", "datePosted", "hiringOrganization", "jobLocation", "description"],
    "Course": ["name", "description", "provider"],
    "QAPage": ["mainEntity"],
    "Person": ["name"],
    "WebSite": ["name", "url"],
}
LOCAL_SUBTYPES = {"Restaurant", "CafeOrCoffeeShop", "Store", "MedicalClinic", "Dentist", "HairSalon", "AutoRepair", "Hotel", "LegalService", "BeautySalon"}


class Grab(HTMLParser):
    def __init__(self):
        super().__init__(); self.blocks, self.text, self._ld, self._skip, self._buf = [], [], False, 0, []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._ld, self._buf = True, []
        elif tag in ("script", "style", "noscript", "template"):
            self._skip += 1
    def handle_endtag(self, tag):
        if tag == "script" and self._ld:
            self.blocks.append("".join(self._buf)); self._ld = False
        elif tag in ("script", "style", "noscript", "template") and self._skip:
            self._skip -= 1
    def handle_data(self, d):
        if self._ld: self._buf.append(d)
        elif not self._skip: self.text.append(d)


def nodes(x):
    if isinstance(x, list):
        for i in x: yield from nodes(i)
    elif isinstance(x, dict):
        if "@graph" in x: yield from nodes(x["@graph"])
        if "@type" in x: yield x
        for k, v in x.items():
            if k != "@graph" and isinstance(v, (dict, list)): yield from nodes(v)


def types_of(n):
    t = n.get("@type"); return t if isinstance(t, list) else [t]


def norm(s): return re.sub(r"\s+", " ", str(s)).strip().lower()


def lint(html):
    g = Grab(); g.feed(html)
    visible = norm(" ".join(g.text))
    findings = []
    if not g.blocks:
        return [("info", "no JSON-LD found on the page")], []
    found_types = []
    for i, raw in enumerate(g.blocks, 1):
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            findings.append(("error", f"block {i}: JSON does not parse ({e.msg} at line {e.lineno})")); continue
        roots = data if isinstance(data, list) else [data]
        for r in roots:
            ctx = str(r.get("@context", "")) if isinstance(r, dict) else ""
            if "schema.org" not in ctx:
                findings.append(("error", f"block {i}: @context must be https://schema.org"))
        for n in nodes(data):
            for t in types_of(n):
                found_types.append(t)
                if t in RETIRED:
                    findings.append(("warn", f"{t}: {RETIRED[t]}"))
                key = "LocalBusiness" if t in LOCAL_SUBTYPES else t
                miss = [p for p in RECOMMENDED.get(key, []) if p not in n]
                if miss:
                    findings.append(("warn", f"{t}: missing recommended {', '.join(miss)}"))
                for prop in ("name", "headline"):
                    v = n.get(prop)
                    if isinstance(v, str) and len(v) > 3 and norm(v) not in visible:
                        findings.append(("error", f"{t}.{prop} «{v[:60]}» is not in the visible text: markup must describe what the user sees"))
                if t == "Offer" and "price" in n:
                    digits = re.sub(r"\D", "", str(n["price"]).split(".")[0])
                    if digits and digits not in re.sub(r"[\s  ]", "", visible):
                        findings.append(("error", f"Offer.price {n['price']} is not shown on the page"))
                if t == "AggregateRating" and str(n.get("ratingValue", "")) and str(n.get("ratingValue")).replace(".", ",") not in visible and str(n.get("ratingValue")) not in visible:
                    findings.append(("error", f"AggregateRating {n.get('ratingValue')} is not shown on the page (self-serving or hidden ratings violate Google policy)"))
    return findings, found_types


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if re.match(r"^https?://", a.src):
        with urllib.request.urlopen(urllib.request.Request(a.src, headers=UA), timeout=20) as r:
            html = r.read().decode("utf-8", "replace")
    else:
        html = pathlib.Path(a.src).read_text(encoding="utf-8", errors="replace")
    f, types = lint(html)
    if a.json:
        print(json.dumps({"types": types, "findings": [{"level": l, "message": m} for l, m in f]}, ensure_ascii=False, indent=2))
    else:
        print("types:", ", ".join(dict.fromkeys(t for t in types if t)) or "-")
        for l, m in f: print({"error": "✗", "warn": "!", "info": "·"}[l], m)
        if not any(l == "error" for l, _ in f): print("✓ no blocking errors")
    return 1 if any(l == "error" for l, _ in f) else 0


if __name__ == "__main__":
    sys.exit(main())
