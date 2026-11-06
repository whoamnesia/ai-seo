---
name: yandex-alice
description: 'astudio Yandex AI search: getting a site into Alice AI answers in Yandex Search (formerly Нейро) and YandexGPT fast answers - how Yandex selects sources, YandexAdditional / YandexAdditionalBot in robots.txt, Yandex Webmaster "Видимость сайта в Алисе AI" share-of-voice report, Yandex microdata validator, regional and commercial factors that are actually documented, and Russian compliance (152-ФЗ, ad marking). Use for "Алиса AI", "Нейро", "попасть в ответы Яндекса", "быстрые ответы", "YandexAdditional", "Яндекс Вебмастер", "ИИ-поиск в России". Part of astudio-ai-seo.'
argument-hint: "[site] [region] [key queries]"
---

# astudio · Yandex Alice AI

`<root>` = two levels above this skill's base dir. Facts with sources: `<root>/reference/facts.md` § Yandex.

## What Yandex documents (and nothing more)
- Alice AI answers in Search (44% of Search queries in Q3 2026) are built from pages that **rank high in Yandex Search**
  and are expert, useful, original and substantive. The model splits the query into sub-questions and writes the answer
  from blocks; it quotes verbatim only direct speech. Answers are not edited by hand.
- Opt-out: `YandexAdditional` / `YandexAdditionalBot` Disallow in robots.txt, effective in 2–14 days. It also removes
  the site from YandexGPT fast answers.
- Measurement: Yandex Webmaster → «Видимость сайта в Алисе AI»: share of Alice AI answers that mention the site among
  queries where the site already ranks; 3 months, weekly, no clicks; it cannot be used to steer inclusion.
- No official statement on llms.txt or on whether Alice uses structured data. Do not claim either.
- Lists of "N Yandex commercial ranking factors" without a Yandex source are folklore; say so.

## Workflow
1. **Access**: robots.txt has no unintended `YandexAdditional` block; if a `User-agent: Yandex` group exists, the needed
   Allow/Disallow lines are repeated there (Yandex robots then ignore `*`). Run `<root>/scripts/robots_audit.py`.
2. **Index health in Webmaster**: pages in search, excluded pages and reasons, region set for the site, Яндекс Бизнес
   card for local companies, site quality index (ИКС) as context only.
3. **Classic ranking first** for the target queries (Wordstat for demand, the site's positions for them). If the site is
   not in the top results, Alice AI will rarely cite it; fix that before writing for AI.
4. **Content** with `astudio-ai-seo:citable-content`: answer-first passages, prices in rubles, Russian units and terms,
   region in the text, real authors, dates.
5. **Trust signals Yandex shows to users**: full contacts and legal details (ИНН/ОГРН) on the site, delivery, returns
   and payment terms, reviews on Яндекс Картах / Маркете that match the site.
6. **Baseline and tracking**: Webmaster SoV export plus a prompt portfolio in Alice (see `ai-visibility-tracking`),
   weekly, with dates.

## Compliance notes for Russian sites
- 152-ФЗ: a privacy policy and consent checkbox on forms; personal data of Russian citizens stored in Russia.
- Ad marking (ФЗ «О рекламе», ст. 18.1): advertising content on the site or in posts carries «Реклама», the advertiser
  and the erid token.
- Do not put competitor brand names into hidden text or markup.
