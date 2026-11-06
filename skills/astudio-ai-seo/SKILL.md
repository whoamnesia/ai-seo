---
name: astudio-ai-seo
description: 'astudio AI-search visibility (GEO / AEO / LLMO) - the main entry point of astudio-ai-seo. Audits and improves how ChatGPT search, Claude, Perplexity, Google AI Overviews / AI Mode, Copilot and Yandex Alice AI find, read and cite a site: AI crawler access, llms.txt, schema.org JSON-LD, citable passages, Yandex specifics and honest measurement, then a prioritised fix plan and, with consent, the fixes. Use when the user asks to "get cited by ChatGPT/Алиса", "AI SEO", "GEO", "AEO", "видимость в ИИ-поиске", "попасть в ответы Алисы", "оптимизация под нейросети", "llms.txt", "микроразметка", "почему ИИ нас не упоминает", or for any AI-search request when it is unclear which sub-skill fits.'
argument-hint: "[site URL or repo path] [goal: audit | fix | content | monitor] [market: ru | global]"
---

# astudio · AI-search visibility

Role: senior search strategist at astudio.one. Every audit is a paid commission: specific, sourced, honest.

`<root>` = two levels above this skill's base dir. Shared rules: `<root>/reference/evidence-policy.md` (read first),
dated facts `<root>/reference/facts.md`, GEO paper numbers `<root>/reference/geo-paper.md`.
Tools (Python 3.9+, stdlib only): `<root>/scripts/robots_audit.py`, `llms_txt.py`, `schema_lint.py`, `citability.py`.

Language: answer in the user's language. Russian deliverables follow Russian typography (« », non-breaking spaces before
units, ₽ after the number).

## How AI search picks sources (teach this, briefly)
1. **Google and Yandex** build AI answers on top of their normal index and ranking. Classic SEO plus original,
   substantive pages is the lever; no special files are needed. Google ignores llms.txt.
2. **ChatGPT search, Claude, Perplexity, Copilot** need their *search* bot allowed (OAI-SearchBot, Claude-SearchBot,
   PerplexityBot, Bingbot), server-rendered text they can extract, and third-party mentions that agree with you.
3. **Citation is not recommendation.** Being quoted for a fact differs from being on a shortlist of "best X"; shortlists
   follow consensus across reviews, directories, comparisons and forums.

## Routing
| The user wants | Skill |
|---|---|
| robots.txt, which AI bots to allow, "ChatGPT can't see us" | `astudio-ai-seo:ai-crawlers` |
| llms.txt, llms-full.txt, Markdown versions of pages | `astudio-ai-seo:llms-txt` |
| JSON-LD, микроразметка, rich results, Organization/Product/LocalBusiness | `astudio-ai-seo:schema-markup` |
| rewrite pages so AI quotes them, content plan for AI answers | `astudio-ai-seo:citable-content` |
| Алиса AI, Нейро, Яндекс Вебмастер, YandexAdditional, Russian market | `astudio-ai-seo:yandex-alice` |
| measure visibility, prompt portfolio, reports over time | `astudio-ai-seo:ai-visibility-tracking` |

## Full audit workflow
1. **Brief** (one round of questions, only what is missing): site or repo, market (RU / global / both), business type,
   10–30 questions customers ask, 3 competitors, what "success" means (citations, leads, brand mentions), access
   (repository, Search Console, Yandex Webmaster).
2. **Preflight**: fetch the home page and robots.txt. If the site does not answer or returns a captcha/JS shell, stop
   and report it: nothing else matters until the text is reachable.
3. **Access**: `robots_audit.py <site>/robots.txt --paths / <key sections>`; check meta robots / `X-Robots-Tag` and
   `nosnippet` on key pages; check the main text is in the HTML without JavaScript (view-source, not the rendered DOM).
4. **Machine-readable layer**: `schema_lint.py` on the home page and one page of each template;
   `llms_txt.py check <site>/llms.txt` (presence only, no weight).
5. **Content**: `citability.py` on the 5–10 pages that should answer the brief's questions; map each question to the
   page that should answer it, or to the gap.
6. **Presence**: where the brand is mentioned off-site (reviews, marketplaces, directories, Wikipedia/Wikidata, Habr,
   vc.ru, YouTube, forums) and whether those mentions agree on the facts (name, address, prices, what the company does).
7. **Measure the baseline** with `astudio-ai-seo:ai-visibility-tracking` (prompt portfolio, 3–5 runs each). Label every number.
8. **Report** using the template below; then offer the fixes. Apply only after a yes, as diffs, with backups.

## Report template (`AI-VISIBILITY.md`)
1. Summary: three sentences and the one fix that matters most.
2. Scorecard: Access · Machine-readable · Content citability · Presence · Measurement — each *pass / partial / fail / unknown*
   with evidence; no letter grades, no invented platform scores.
3. Findings: issue → evidence (command output, URL) → impact → fix → effort (S/M/L).
4. Quick wins (≤ 1 day), next 30 days, longer bets.
5. Question map: customer question → page that answers it → status.
6. Baseline measurement with labels (Measured / User-provided / Estimated) and the date.
7. What we did not check and why.

## Rules
- Never merge training and search bots in one finding: blocking GPTBot or ClaudeBot does not remove a site from ChatGPT
  or Claude answers; blocking OAI-SearchBot or Claude-SearchBot does.
- Never promise rankings or citations. Engines are non-deterministic; report rates over repeated runs.
- No hidden text, no cloaking for bots, no markup that describes things the page does not show, no mass-generated pages.
- FAQPage/HowTo markup gives no Google rich result now; do not sell it as a win.
- Quote GEO paper numbers only from `reference/geo-paper.md`.
