---
name: llms-txt
description: 'astudio llms.txt and agent-readable pages: check and draft /llms.txt and llms-full.txt to the llmstxt.org spec, Markdown twins of key pages (rel=alternate text/markdown), /pricing.md for buying agents - with an honest note on what llms.txt does and does not do. Use for "сделай llms.txt", "llms-full.txt", "версия сайта для нейросетей", "markdown-версии страниц", "agent-ready site". Part of astudio-ai-seo.'
argument-hint: "[site URL or repo path]"
---

# astudio · llms.txt

`<root>` = two levels above this skill's base dir. Tool: `<root>/scripts/llms_txt.py` (`check`, `draft`).
Spec summary: `<root>/reference/facts.md` § llms.txt.

## What to tell the client first
llms.txt is a map for language models and coding agents. Google says it ignores it, and no search engine documents
ranking use, so it is not a ranking lever. It is useful for documentation, APIs, SaaS and any site that agents read
on a user's behalf. It costs an hour. Report its presence; give it no weight in scores.

## Workflow
1. `llms_txt.py check <site>/llms.txt`. If it exists and passes, review the descriptions only.
2. Draft: `llms_txt.py draft --name "<Brand>" --summary "<one sentence>" --sitemap <site>/sitemap.xml`.
3. Edit by hand: keep 10–40 pages a newcomer needs (what we do, prices, delivery/terms, contacts, docs, key guides);
   write one factual line per link ("Тарифы и условия возврата, цены в рублях с НДС"); put secondary links under
   `## Optional`; remove thin, duplicate, private and parameter URLs.
4. Optional `llms-full.txt`: the same pages' text in Markdown, for docs sites. Keep it under ~200 KB or split by section.
5. Markdown twins for key pages (`/pricing.md`, `/docs/x.md`) with `<link rel="alternate" type="text/markdown" href="…">`.
   Their facts must match the HTML exactly; keep them generated from the same source.
6. Serve as `text/plain` or `text/markdown; charset=utf-8`, status 200, not blocked in robots.txt.
7. Show the files, get a yes, commit.

## Format
```
# Кофейня «Зерно»

> Кофейня и обжарка в Казани: меню, доставка по городу, оптовые поставки зерна.

## Главное
- [Меню и цены](https://zerno.ru/menu): напитки и десерты, цены в рублях
- [Доставка](https://zerno.ru/delivery): зоны, сроки и стоимость

## Optional
- [Блог](https://zerno.ru/blog): статьи об обжарке
```
