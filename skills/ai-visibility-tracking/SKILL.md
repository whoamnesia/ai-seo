---
name: ai-visibility-tracking
description: 'astudio AI visibility measurement: a prompt portfolio across awareness stages, repeated runs (3-5 per prompt) in ChatGPT, Perplexity, Claude, Google AI Mode / AI Overviews and Yandex Alice AI, citation vs recommendation vs mention, share of voice against competitors, Search Console Generative AI report and Yandex Webmaster Alice AI report, monthly trend with every number labelled Measured / User-provided / Estimated. Use for "отслеживать упоминания в нейросетях", "доля в ответах ИИ", "AI share of voice", "мониторинг видимости в Алисе", "как понять, что GEO работает". Part of astudio-ai-seo.'
argument-hint: "[brand] [competitors] [questions]"
---

# astudio · AI visibility tracking

`<root>` = two levels above this skill's base dir. Labels and honesty rules: `<root>/reference/evidence-policy.md`.

## Prompt portfolio
Build 20–40 prompts in the customer's words, tagged by stage:
- **Problem** ("как продлить срок хранения кофе"), **category** ("какую кофемолку выбрать для дома"),
- **shortlist** ("лучшие кофейни Казани с доставкой"), **brand** ("Зерно Казань отзывы"), **comparison** ("Зерно или X").
Keep the list in `ai-visibility/prompts.csv` (`id,stage,prompt,market,engine_list`). Do not change prompts between
runs; add new ones with new ids.

## Each run
1. For every prompt and engine, run it **3–5 times** in a fresh session without personalisation, same region.
2. Record per run: mentioned (yes/no), cited with a link (URL), position in a list, sentiment, competitors named,
   the sources the engine cited. Save raw answers with the date (`ai-visibility/runs/2026-11-06/…`).
3. Compute rates, not single results: "cited 3/5 (n=5)". Separate **citation** (your URL as a source),
   **mention** (name without a link) and **recommendation** (you are on the shortlist).
4. Add the platform reports where the client gives access: Google Search Console Generative AI performance report and
   Yandex Webmaster «Видимость сайта в Алисе AI». These are Measured.

## Report (monthly)
| Engine | Citation rate | Mention rate | Recommendation rate | Top cited sources | Change vs last month |
Plus: the three prompts with the biggest change, which third-party sources engines rely on (targets for PR and
listings), and what changed on the site in the period. Every number has its label and date.

## Rules
- Never report a single run as a result; answers vary run to run.
- Never call a heuristic or vendor "AI score" a platform metric.
- Automated querying must follow each service's terms; prefer official APIs and the client's own accounts.
