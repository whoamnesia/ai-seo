# Dated facts (checked 2026-11-06)

Re-check anything older than six months before quoting it.

## Google (AI Overviews, AI Mode)
- AI features are "rooted in our core Search ranking and quality systems"; no special files, markup or Markdown are
  needed; Google **ignores llms.txt**; no need to chunk content; structured data is not required for AI features but
  still powers rich results. A site must be included in "Search generative AI features" in Search Console, and the
  Search Console "Generative AI performance report" measures it. Source: AI optimization guide, updated 2026-07-10,
  https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Controls: Googlebot in robots.txt, `nosnippet`, `data-nosnippet`, `max-snippet`, `noindex`.
- Google-Extended controls Gemini training and grounding in other Google products; it does not affect Search and has
  no user-agent string of its own.
- Query fan-out: the model issues several related queries at once. Pages built to manipulate AI answers can violate the
  scaled content abuse policy.

## Rich results status
- FAQ rich results: stopped 2026-05-07; documentation removed 2026-06-15.
- HowTo: removed in 2023.
- Retired 2025-06-12: Book Actions, Course Info, ClaimReview, Estimated Salary, Learning Video, Special Announcement,
  Vehicle Listing. Practice Problem deprecated 2025-11-05.
- Still useful: Organization, LocalBusiness, Product (+Offer, Review, AggregateRating), Article, BreadcrumbList,
  VideoObject, Event, JobPosting, Course list, QAPage, Dataset (Dataset Search).

## OpenAI, Anthropic, Perplexity crawlers
- OAI-SearchBot: ChatGPT search. Sites that block it are not shown in ChatGPT search answers. GPTBot: training.
  ChatGPT-User: user-initiated; robots.txt may not apply. https://developers.openai.com/api/docs/bots
- Claude-SearchBot: search; ClaudeBot: training; Claude-User: user retrieval. All honour robots.txt.
  https://support.claude.com/en/articles/8896518
- PerplexityBot: search, not training; Perplexity-User generally ignores robots.txt.
  https://docs.perplexity.ai/docs/resources/perplexity-crawlers.md

## Yandex
- Нейро launched 2024-04-16; Alice AI replaced it in Search in May 2025.
- Alice AI splits a query into sub-questions, searches, and builds the answer from pages that rank high and are
  expert, useful, original and substantive. It does not reproduce text verbatim except direct quotes. Answers are not
  edited manually. https://yandex.ru/support/webmaster/ru/alice
- Opt-out: `User-agent: YandexAdditional` (or `YandexAdditionalBot`) + `Disallow`, effective in 2–14 days; it also
  covers YandexGPT fast answers (generated only for Russia).
- If a `User-agent: Yandex` group exists, Yandex robots ignore `*`.
- Webmaster report "Видимость сайта в Алисе AI" (since 2026-04-07): share of Alice AI answers that mention the site,
  among queries where the site already ranks high; last 3 months; weekly; no clicks.
  https://yandex.ru/support/webmaster/ru/service/alice-answers
- Q3 2026: Alice AI answers 44% of Search queries; fast answers reach 54.8M users a month.
  https://yandex.ru/company/news/29-10-2026-01
- No official Yandex statement on llms.txt was found (Yandex publishes llms.txt for its own help, which is not the same).

## llms.txt (https://llmstxt.org)
- `/llms.txt` or a subpath; the most specific file covers its path.
- H1 with the name (the only required part) → optional blockquote → optional text → H2 sections with
  `- [name](url): notes` → optional `## Optional` section.
- Pages may have Markdown twins (`page.md`, `page.html.md`), discoverable through `<link rel="alternate" type="text/markdown">`.
