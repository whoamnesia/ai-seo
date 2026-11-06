#!/usr/bin/env python3
"""astudio-ai-seo · robots_audit.py

Reads a robots.txt (file path or URL) and reports, for every AI-related robot in
data/ai-bots.json, whether it may fetch the given paths. Groups the answer by
purpose (search / training / user-fetch / AI-answer control) so search and
training bots are never merged into one finding.

Touches: network only when a URL is given (one GET). Writes nothing.

  python3 robots_audit.py https://example.ru/robots.txt --paths / /blog/ /catalog/
  python3 robots_audit.py robots.txt --json
"""
import argparse, json, pathlib, re, sys, urllib.request

HERE = pathlib.Path(__file__).resolve().parent
BOTS = json.loads((HERE.parent / "data" / "ai-bots.json").read_text(encoding="utf-8"))["bots"]


def load(src: str) -> str:
    if re.match(r"^https?://", src):
        req = urllib.request.Request(src, headers={"User-Agent": "astudio-ai-seo/1.0 (+https://astudio.one)"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", "replace")
    return pathlib.Path(src).read_text(encoding="utf-8", errors="replace")


def parse(text: str):
    """Return list of groups: {agents: [..], rules: [(allow:bool, pattern)]}."""
    groups, cur, last_was_agent = [], None, False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, val = [x.strip() for x in line.split(":", 1)]
        key = key.lower()
        if key == "user-agent":
            if cur is None or not last_was_agent:
                cur = {"agents": [], "rules": []}
                groups.append(cur)
            cur["agents"].append(val.lower())
            last_was_agent = True
        elif key in ("allow", "disallow") and cur is not None:
            last_was_agent = False
            if key == "disallow" and val == "":
                continue  # empty Disallow = allow all
            cur["rules"].append((key == "allow", val))
        else:
            last_was_agent = False
    return groups


def pick_group(groups, token: str):
    """Most specific matching group (RFC 9309): longest product token that matches; else '*'."""
    t = token.lower()
    best, best_len, name = None, -1, None
    for g in groups:
        for a in g["agents"]:
            if a != "*" and t.startswith(a) and len(a) > best_len:
                best, best_len, name = g, len(a), a
    if best is None:
        # Yandex robots also obey a 'User-agent: Yandex' group
        if t.startswith("yandex"):
            for g in groups:
                if "yandex" in g["agents"]:
                    return g, "yandex"
        for g in groups:
            if "*" in g["agents"]:
                return g, "*"
        return None, None
    return best, name


def rule_re(pattern: str):
    rx = re.escape(pattern).replace(r"\*", ".*")
    if rx.endswith(r"\$"):
        rx = rx[:-2] + "$"
    return re.compile("^" + rx)


def allowed(group, path: str) -> bool:
    if group is None:
        return True
    best, verdict = -1, True
    for allow, pat in group["rules"]:
        if rule_re(pat).match(path) and (len(pat) > best or (len(pat) == best and allow)):
            best, verdict = len(pat), allow
    return verdict


LABEL = {
    "search": "Search / answer engines (decide whether you can be cited)",
    "ai-answer-control": "AI-answer controls (Yandex Alice AI, YandexGPT fast answers)",
    "training": "Training crawlers (do NOT affect being cited in search answers)",
    "training-control": "Training-only tokens (no effect on Search)",
    "user-fetch": "User-triggered fetchers (often ignore robots.txt)",
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("robots", help="robots.txt path or URL")
    ap.add_argument("--paths", nargs="*", default=["/"], help="paths to test (default /)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    groups = parse(load(a.robots))
    rows = []
    for b in BOTS:
        g, via = pick_group(groups, b["token"])
        res = {p: allowed(g, p) for p in a.paths}
        rows.append({**b, "group": via or "(none: allowed)", "allowed": res})
    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    for purpose in LABEL:
        sel = [r for r in rows if r["purpose"] == purpose]
        if not sel:
            continue
        print(f"\n## {LABEL[purpose]}")
        for r in sel:
            st = ", ".join(f"{p} {'allow' if ok else 'BLOCK'}" for p, ok in r["allowed"].items())
            note = "" if r["honours_robots"] else "  (may ignore robots.txt)"
            print(f"- {r['token']:<20} {st:<40} group: {r['group']}{note}\n    {r['governs']}")
    blocked_search = [r["token"] for r in rows if r["purpose"] in ("search", "ai-answer-control") and not all(r["allowed"].values())]
    print("\n## Verdict")
    if blocked_search:
        print("Search/answer bots blocked on some paths: " + ", ".join(blocked_search) +
              ". Those engines cannot cite the blocked pages. Confirm this is intended.")
    else:
        print("All search and answer bots may fetch the tested paths.")
    print("Training bots are a separate business decision; blocking them does not remove you from AI search answers.")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        pass
