---
name: schema-markup
description: 'astudio schema.org structured data (JSON-LD): choose types that still matter in 2026 (Organization, LocalBusiness, Product + Offer + AggregateRating, Article, BreadcrumbList, VideoObject, Event, JobPosting, Course, QAPage), write them to match the visible page, lint them, and flag retired rich results (FAQPage, HowTo and the 2025 batch). Covers Google Rich Results Test and the Yandex microdata validator. Use for "микроразметка", "schema.org", "JSON-LD", "rich snippets", "расширенные сниппеты", "разметка товара", "разметка организации". Part of astudio-ai-seo.'
argument-hint: "[page URL or file] [page type: home | product | article | local | event | job]"
---

# astudio · Schema markup

`<root>` = two levels above this skill's base dir. Lint: `<root>/scripts/schema_lint.py`. Status of types:
`<root>/reference/facts.md` § Rich results status.

Structured data is not required for AI answers (Google says so), but it states facts unambiguously: who you are, what
the product costs, where you are, who wrote the article. That helps rich results, knowledge panels and every consumer
that reads JSON-LD. It only helps when it matches what the page shows.

## Workflow
1. Inventory page templates (home, category, product, article, contacts, events, vacancies).
2. Lint what exists: `schema_lint.py <url>` per template.
3. Choose types per template (table below). One `@graph` per page; give entities stable `@id` values
   (`https://site.ru/#organization`) and reference them instead of repeating.
4. Write JSON-LD from the same data source as the page (CMS fields), never by hand-copying numbers.
5. Validate: `schema_lint.py`, then Google Rich Results Test and Schema Markup Validator, and for Russia the Yandex
   Webmaster microdata validator. Paste the results into the report.
6. Show the diff; deploy after a yes.

## Types by template
| Template | Types | Must match the page |
|---|---|---|
| Home | Organization (or LocalBusiness subtype), WebSite | name, logo, contacts; `sameAs` to official profiles (VK, Telegram, Яндекс Карты, 2ГИС, Wikipedia) |
| Product | Product + Offer (+ AggregateRating, Review if shown) | price, currency `RUB`, availability, rating value and count |
| Category | BreadcrumbList, ItemList (optional) | breadcrumb text |
| Article / blog | Article/BlogPosting + Person (author) | headline, author name with a profile page, dates |
| Contacts / branch | LocalBusiness subtype with address, geo, openingHoursSpecification, telephone | the same NAP as maps and directories |
| Video page | VideoObject | thumbnail, upload date, duration |
| Events / courses / jobs | Event, Course, JobPosting | dates, price, location, salary |
| Q&A forum page | QAPage | real user questions and answers |

## Retired or no-effect types (do not sell them as wins)
FAQPage (no Google rich result since 2026-05-07), HowTo (2023), ClaimReview, EstimatedSalary, Learning Video,
SpecialAnnouncement, Vehicle Listing, Book Actions (2025-06-12). Keep FAQPage/HowTo only if they mirror visible content
and someone else consumes them; say there is no Google SERP effect.

## Rules
- Mark up only what users can see. Hidden ratings, self-serving reviews of your own organisation and prices that differ
  from the page violate Google policy and can bring a manual action.
- Prices: number without spaces in `price` ("4990"), `priceCurrency: "RUB"`; show the same price in the HTML.
- Dates in ISO 8601 with time zone (`2026-11-06T10:00:00+03:00`).
- One organisation entity per site, referenced by `@id`.

## Example: LocalBusiness
```json
{"@context":"https://schema.org","@graph":[{"@type":"CafeOrCoffeeShop","@id":"https://zerno.ru/#org",
"name":"Кофейня «Зерно»","url":"https://zerno.ru/","logo":"https://zerno.ru/logo.svg","telephone":"+7 843 000-00-00",
"address":{"@type":"PostalAddress","streetAddress":"ул. Баумана, 1","addressLocality":"Казань","postalCode":"420111","addressCountry":"RU"},
"geo":{"@type":"GeoCoordinates","latitude":55.7887,"longitude":49.1221},
"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"08:00","closes":"22:00"}],
"sameAs":["https://vk.com/zerno","https://yandex.ru/maps/org/000"]}]}
```
