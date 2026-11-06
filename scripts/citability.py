#!/usr/bin/env python3
"""astudio-ai-seo · citability.py — heuristic passage scorer for AI citation readiness (RU + EN).

  python3 citability.py page.html            # or a URL or a .md file
  python3 citability.py page.md --top 5 --json

Splits the page into passages under their headings and scores each 0-100:
  answer-first 30  · self-contained 25 · structure 20 · specifics 15 · sourcing 10
It is a heuristic, not a measurement of any engine: label results "Estimated".
What it rewards follows the GEO paper (Aggarwal et al., KDD 2024: quotations,
statistics and cited sources lifted visibility most; keyword stuffing hurt) and
Google/Yandex guidance (clear, original, substantive text). Writes nothing.
"""
import argparse, json, re, sys, pathlib, urllib.request
from html.parser import HTMLParser

UA = {"User-Agent": "astudio-ai-seo/1.0 (+https://astudio.one)"}
DEF = [r"\b\w+\s+(is|are|means|refers to)\s", r"\b\w+\s+[—–-]\s+(это|это\s+когда)\s", r"\bэто\s+\w+", r"\bназывают\b", r"\bпредставляет собой\b", r"\bозначает\b"]
PRON_START = r"^(it|this|that|they|these|those|он|она|оно|они|это|этот|эта|эти|такой|такие|там|тогда)\b"
NUM = r"\d[\d\s .,]*\s?(%|₽|руб|тыс|млн|млрд|\$|€|km|км|kg|кг|ч|мин|дн|day|hour|year|год|лет)"
YEAR = r"\b(19|20)\d{2}\b"
SRC = r"(according to|по данным|согласно|source:|источник|исследовани|study|report|отчёт|отчет|\bГОСТ\b|ФЗ|\bст\.\s?\d)"
QUOTE = r"[«\"“][^»\"”]{12,}[»\"”]"
HEDGE = r"\b(maybe|perhaps|might|possibly|возможно|наверное|как бы|в некотором роде|может быть)\b"


class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.out, self.skip, self.tag = [], 0, None
    def handle_starttag(self, t, a):
        if t in ("script", "style", "noscript", "nav", "footer", "template"): self.skip += 1
        if t in ("h1", "h2", "h3", "h4"): self.out.append("\n#H ")
        if t in ("p", "li", "div", "section", "br", "tr"): self.out.append("\n")
    def handle_endtag(self, t):
        if t in ("script", "style", "noscript", "nav", "footer", "template") and self.skip: self.skip -= 1
        if t in ("h1", "h2", "h3", "h4", "p", "li"): self.out.append("\n")
    def handle_data(self, d):
        if not self.skip: self.out.append(d)


def passages(text, md):
    if not md:
        p = Text(); p.feed(text); text = "".join(p.out)
    heading, buf, out = "", [], []
    for line in text.splitlines():
        s = line.strip()
        h = re.match(r"^(#H|#{1,4})\s+(.*)", s)
        if h:
            if buf: out.append((heading, " ".join(buf))); buf = []
            heading = h.group(2).strip(); continue
        if s: buf.append(s)
        elif buf and len(" ".join(buf).split()) > 40:
            out.append((heading, " ".join(buf))); buf = []
    if buf: out.append((heading, " ".join(buf)))
    return [(h, b) for h, b in out if len(b.split()) >= 15]


def score(heading, body):
    words = body.split(); n = len(words); first = " ".join(words[:60])
    s, why = {}, []
    a = 0
    if any(re.search(p, first, re.I) for p in DEF): a += 12
    if re.search(NUM, first, re.I): a += 8
    if heading.endswith("?"): a += 5
    sents = [x for x in re.split(r"(?<=[.!?])\s+", body) if x.strip()]
    if sents and len(sents[0].split()) <= 30: a += 5
    s["answer_first"] = min(a, 30)
    if a < 15: why.append("lead with the answer: a definition or the number in the first sentence")
    c = 25
    if re.match(PRON_START, body, re.I): c -= 10; why.append("starts with a pronoun: name the subject so the passage stands alone")
    if n < 40: c -= 8; why.append(f"{n} words: too short to stand alone (aim 40-170)")
    if n > 250: c -= 8; why.append(f"{n} words: split into passages of 40-170 words under clear headings")
    s["self_contained"] = max(c, 0)
    st = 0
    if heading: st += 8
    avg = n / max(len(sents), 1)
    st += 8 if avg <= 22 else 4 if avg <= 30 else 0
    if avg > 30: why.append(f"average sentence {avg:.0f} words: shorten")
    if re.search(r"(:\s|;\s|\d\)\s|—\s)", body): st += 4
    s["structure"] = min(st, 20)
    nums = len(re.findall(NUM, body, re.I)) + len(re.findall(YEAR, body))
    s["specifics"] = min(nums * 5, 15)
    if nums == 0: why.append("no numbers, dates or units: add a verifiable specific (GEO paper: statistics +30.6%)")
    src = (6 if re.search(SRC, body, re.I) else 0) + (4 if re.search(QUOTE, body) else 0)
    s["sourcing"] = src
    if src == 0: why.append("no source or quotation: cite where the fact comes from (GEO paper: quotations +40.9%, sources +27.5%)")
    if re.search(HEDGE, body, re.I): why.append("hedging words weaken extractable claims")
    total = sum(s.values())
    return total, s, why


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src"); ap.add_argument("--top", type=int, default=0); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if re.match(r"^https?://", a.src):
        with urllib.request.urlopen(urllib.request.Request(a.src, headers=UA), timeout=20) as r:
            raw = r.read().decode("utf-8", "replace"); md = False
    else:
        raw = pathlib.Path(a.src).read_text(encoding="utf-8", errors="replace"); md = a.src.endswith((".md", ".txt"))
    rows = []
    for h, b in passages(raw, md):
        t, parts, why = score(h, b)
        rows.append({"heading": h, "words": len(b.split()), "score": t, "parts": parts, "fix": why, "start": b[:90]})
    rows.sort(key=lambda r: r["score"])
    if a.top: rows = rows[: a.top]
    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2)); return 0
    if not rows:
        print("no passages of 15+ words found"); return 0
    avg = sum(r["score"] for r in rows) / len(rows)
    print(f"Estimated citability: {avg:.0f}/100 over {len(rows)} passages (weakest first)\n")
    for r in rows:
        print(f"[{r['score']:>3}] {r['heading'] or '(no heading)'} · {r['words']} words\n      «{r['start']}…»")
        for f in r["fix"]: print("      - " + f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
