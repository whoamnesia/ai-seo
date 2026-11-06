---
name: citable-content
description: 'astudio citable content for AI answers: map customer questions to pages, then rewrite pages into self-contained, answer-first passages with real numbers, named sources and quotations (per the measured GEO paper results), clear headings, comparison tables, author and date - in Russian or English, without keyword stuffing or mass-generated pages. Includes a passage citability scorer. Use for "чтобы нейросети цитировали", "переписать страницу под ИИ-поиск", "контент для ответов Алисы", "GEO-тексты", "make this page citable", "content plan for AI answers". Part of astudio-ai-seo.'
argument-hint: "[page URL / file / topic] [questions the page must answer]"
---

# astudio · Citable content

`<root>` = two levels above this skill's base dir. Scorer: `<root>/scripts/citability.py` (heuristic, label it
Estimated). Numbers: `<root>/reference/geo-paper.md`.

## What gets quoted
AI engines split a question into sub-questions, fetch pages that rank, and lift passages that answer one sub-question
on their own. Yandex says Alice AI prefers expert, useful, original, substantive pages; Google says the same in its
own words. The GEO paper measured the largest lifts from quotations (+40.9%), statistics (+30.6%), fluent writing
(+28.0%) and cited sources (+27.5%); keyword stuffing lost 8.3%.

## Workflow
1. **Question map.** Collect 20–50 real questions: the client's support inbox and sales calls, Wordstat / Google
   "People also ask", marketplace questions, forum threads. Group by intent (what is, how much, how to choose, vs,
   problem). Assign each to one page or mark a gap.
2. **Score** the existing pages: `citability.py <page> --top 10`.
3. **Rewrite passage by passage** (40–170 words each, one sub-question each):
   - Heading = the question in the customer's words ("Сколько стоит доставка по Казани?").
   - First sentence = the answer with the number ("Доставка по Казани стоит 300 ₽ и занимает до 2 часов.").
   - Then the conditions, exceptions and one proof: a source with a date, a quotation from a named expert, a table.
   - Name the subject instead of "it/this/он/это"; each passage must make sense pasted alone.
4. **Page furniture**: author with a real profile and credentials, "updated" date, comparison tables in HTML
   (`<table>`), a short summary at the top, prices and terms in text (not only in images).
5. **Original value**: own data (orders, tests, prices over time), photos, cases. Pages that only restate others are not cited.
6. **Re-score**, then show before/after to the human. Publish after a yes.

## Content types that earn citations
Definitions and explainers; comparisons and "X vs Y" with criteria; prices and terms; step-by-step guides; original
research and statistics; local pages with full NAP and hours; glossaries for the niche.

## Rules
- Facts only from the client or a cited source; mark unknowns `[уточнить]` instead of guessing.
- No keyword stuffing, no doorway pages per city, no scaled AI-written pages: they violate Google's spam policies and
  Yandex's quality rules, and the GEO paper shows stuffing lowers visibility.
- Russian text: « » quotes, `—` with spaces, non-breaking space before ₽ and units, numbers grouped with thin spaces.
- Keep marketing adjectives out of answer sentences ("лучший", "уникальный"): engines skip them, people distrust them.
