# astudio-ai-seo — AI-search visibility (GEO / AEO) for Claude Code

**English** · [Русский](README.ru.md)

Author: **astudio.one** — [astudio.one](https://astudio.one) · License: MIT · Version 1.0.0

One plugin that teaches an agent how ChatGPT search, Claude, Perplexity, Google AI Overviews / AI Mode, Copilot and Yandex Alice AI find, read and cite a website — and how to audit and fix a site for them without myths. Every fact is dated and sourced, search and training bots are never confused, and every number in a report is labelled Measured, User-provided or Estimated.

## What it does

- Full AI-visibility audit with a fixed report template and a prioritised fix plan
- robots.txt policy by bot purpose (search / training / user fetch / Yandex AI answers), including YandexAdditional
- llms.txt and Markdown twins to the llmstxt.org spec, with an honest note on what they do
- schema.org JSON-LD that matches the page, with retired rich results flagged (FAQ ended 2026-05-07)
- Answer-first, citable passages in Russian and English, based on the measured GEO paper results
- Yandex Alice AI: what Yandex actually documents, Webmaster share-of-voice report, Russian compliance
- Repeatable measurement: prompt portfolio, 3–5 runs per prompt, citation vs mention vs recommendation

## Install

In Claude Code:

```
/plugin marketplace add whoamnesia/astudio-ai-seo
/plugin install astudio-ai-seo@astudio-ai-seo
```

Restart Claude Code. Skills appear in the `/` menu as `astudio-ai-seo:astudio-ai-seo` …

Pinned install (what aiocenter.ru does): clone the repository, check out the published commit, then `/plugin marketplace add ~/.aiocenter/packages/astudio-ai-seo`.

Other agents (Cursor, Codex, Gemini CLI): every skill is a plain `skills/<name>/SKILL.md` with references; point the agent at the folder or copy it into the agent's rules.

## Skills

| Skill | What it does |
|---|---|
| `astudio-ai-seo` | Main skill and router: brief, preflight, full audit, report, fixes with consent |
| `ai-crawlers` | robots.txt and page-level controls for AI search and training bots, claim → bot matrix |
| `llms-txt` | Check and draft llms.txt, llms-full.txt and Markdown twins |
| `schema-markup` | JSON-LD by page template, linting, retired types |
| `citable-content` | Question map and answer-first rewriting of pages |
| `yandex-alice` | Alice AI in Yandex Search, YandexAdditional, Webmaster report, RU compliance |
| `ai-visibility-tracking` | Prompt portfolio, repeated runs, share of voice, monthly report |

## Tools

Python 3.9+, standard library only. They read what you pass them and write nothing unless you redirect the output.

| Script | Purpose |
|---|---|
| `scripts/robots_audit.py` | robots.txt verdict per AI bot, grouped by purpose, Yandex rules included |
| `scripts/llms_txt.py` | Validate llms.txt against the spec or draft one from a sitemap |
| `scripts/schema_lint.py` | Lint JSON-LD: parse, retired types, recommended fields, values visible on the page |
| `scripts/citability.py` | Heuristic RU/EN passage scorer with concrete fixes (Estimated) |

## Safety

- Read-only by default. Changes to robots.txt, markup, llms.txt or texts are shown as a diff and applied only after the human says yes; the old file is backed up.
- Scripts make at most one GET per URL you pass, send nothing anywhere else and write nothing.
- No cloaking, hidden text, fake reviews or mass-generated pages; no promises of rankings or citations.

## Layout

```
astudio-ai-seo/
  .claude-plugin/plugin.json, marketplace.json
  skills/<7 skills>/SKILL.md
  reference/  evidence-policy.md · facts.md (dated, sourced) · geo-paper.md
  data/       ai-bots.json (purpose of every AI robot token)
  scripts/    robots_audit.py · llms_txt.py · schema_lint.py · citability.py
  README.md · README.ru.md · LICENSE · NOTICE.md
```

## Training track

This plugin is the package of the aiocenter.ru track «Видимость в ИИ-поиске»: digests, agent memo and an exam with a signed certificate — https://aiocenter.ru/tracks/ai-seo/

## Credits

Built by astudio.one on ideas from the best open-source projects in this field; see [NOTICE.md](NOTICE.md) for sources and licences.
