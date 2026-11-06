# Evidence policy (shared by every astudio-ai-seo skill)

AI-search advice is full of confident, unsourced numbers. This plugin keeps three rules.

## 1. Primary source first
When community advice contradicts a vendor's own documentation, follow the vendor:
Google Search Central, OpenAI / Anthropic / Perplexity crawler pages, Yandex Webmaster help, llmstxt.org.
Quote the page and its "last updated" date. If a fact is older than 6 months, re-check it before relying on it.

## 2. Label every number
Every metric in a report carries one label:

| Label | Meaning | Example |
|---|---|---|
| **Measured** | produced by a tool or a log in this session, with the command or report named | "Alice AI share of voice 12% (Webmaster, 2026-10-01…2026-10-31)" |
| **User-provided** | given by the client; not verified | "organic leads 140/month (from the client)" |
| **Estimated** | a heuristic or model judgement | "citability 62/100 (citability.py heuristic)" |

Never present an Estimated score as a platform metric. No tool outside Google or Yandex sees their ranking systems.

## 3. Do not invent effects
- llms.txt: report whether it exists and is valid. Give it **no ranking weight**: Google says it ignores the file, and no
  engine documents ranking use. It does help coding agents and documentation readers.
- FAQPage / HowTo markup: no Google rich result any more (FAQ ended 2026-05-07, HowTo 2023).
- GEO paper numbers are quoted exactly as in `reference/geo-paper.md`, with the caveat that they come from a simulated engine plus a Perplexity check.
- "Ranking factor" lists for Yandex or AI engines without a primary source are red flags; say so.

## Safety
- Read-only by default. Any change to a site (robots.txt, markup, llms.txt, text) is shown as a diff first and applied only after the human says yes.
- Back up a file before editing it. Never touch production directly when a repository or staging copy exists.
- Scripts in `scripts/` make at most one GET per URL you pass, send nothing elsewhere, and write nothing unless `> file` is used.
