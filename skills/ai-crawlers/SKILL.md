---
name: ai-crawlers
description: 'astudio AI crawler policy: audit and write robots.txt rules for AI search and training bots (OAI-SearchBot, GPTBot, ChatGPT-User, Claude-SearchBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended, Bingbot, YandexBot, YandexAdditional), meta robots / X-Robots-Tag / nosnippet, server rendering checks, and log checks - keeping search and training decisions separate. Use for "robots.txt для ИИ", "заблокировать обучение нейросетей", "ChatGPT не видит сайт", "разрешить ИИ-ботов", "GPTBot", "YandexAdditional". Part of astudio-ai-seo.'
argument-hint: "[robots.txt URL or path] [policy: cite-but-no-training | open | closed]"
---

# astudio · AI crawlers

`<root>` = two levels above this skill's base dir. Bot table: `<root>/data/ai-bots.json`. Tool: `<root>/scripts/robots_audit.py`.

## Claim → bot (check the right bot for the claim you make)
| Claim | Bot that decides it |
|---|---|
| "We can appear in ChatGPT search" | OAI-SearchBot (not GPTBot) |
| "Our content is not used to train OpenAI models" | GPTBot |
| "Claude can find us in search" | Claude-SearchBot (not ClaudeBot) |
| "Perplexity can cite us" | PerplexityBot |
| "We can appear in Google AI Overviews / AI Mode" | Googlebot + snippet controls (not Google-Extended) |
| "Gemini may not train on us" | Google-Extended (robots token only) |
| "Copilot can cite us" | Bingbot |
| "Alice AI / YandexGPT fast answers may use us" | YandexAdditional / YandexAdditionalBot (plus YandexBot indexing) |
User-triggered fetchers (ChatGPT-User, Perplexity-User) may ignore robots.txt: robots.txt is not access control. Use
authentication for private content.

## Workflow
1. Run `robots_audit.py <robots> --paths / <sections>`; read it by purpose group.
2. Ask the business decision once: *cite us but do not train on us* (most common), *open*, or *closed*.
3. Write the rules. Prefer **one `User-agent: *` group plus named exceptions**: a named allow-list silently excludes
   every bot you did not list. Remember that a `User-agent: Yandex` group makes all Yandex robots ignore `*`, so
   repeat needed rules there.
4. Check page-level controls: `<meta name="robots">`, `X-Robots-Tag`, `nosnippet`/`max-snippet` (these also limit
   AI Overviews), and canonical tags.
5. Check rendering: the main text, prices and contacts must be in the server HTML. Many AI fetchers do not run JavaScript.
6. If logs are available: count hits per user-agent for 30 days; verify claimed Googlebot/Bingbot by reverse DNS before trusting the user-agent string.
7. Show the robots.txt diff, wait for a yes, keep the old file as `robots.txt.bak`.

## Template: cite but do not train
```
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /cart/

User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Applebot-Extended
Disallow: /

Sitemap: https://example.ru/sitemap.xml
```
OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot, Bingbot, YandexBot and YandexAdditional fall under `*` and stay allowed.

## Rules
- State the effect of each line in plain words in the report ("GPTBot: training only; you stay in ChatGPT search").
- Blocking YandexAdditional removes the site from Alice AI answers and YandexGPT fast answers in 2–14 days; ask before doing it.
- Never block CSS/JS needed to render the page for Googlebot or YandexBot.
