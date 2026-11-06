# GEO paper: what was actually measured

Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan, Deshpande. "GEO: Generative Engine Optimization", arXiv 2311.09735
(v3 2024-06-28), KDD 2024. https://arxiv.org/abs/2311.09735

## Table 1, GEO-bench, Position-Adjusted Word Count (baseline 19.3)

| Method | PAWC | Change |
|---|---|---|
| Quotation Addition | 27.2 | **+40.9%** |
| Statistics Addition | 25.2 | **+30.6%** |
| Fluency Optimization | 24.7 | +28.0% |
| Cite Sources | 24.6 | +27.5% |
| Technical Terms | 22.7 | +17.6% |
| Easy-to-Understand | 22.0 | +14.0% |
| Authoritative | 21.3 | +10.4% |
| Unique Words | 20.5 | +6.2% |
| Keyword Stuffing | 17.7 | **−8.3%** |

Real-engine check on Perplexity.ai: Quotation about +22% (PAWC), Statistics about +37% (subjective impression).
Keyword stuffing was worse than baseline there too.

## Context you must give with these numbers
- The engine in the main table is simulated; only one real engine (Perplexity) was tested.
- Gains concentrate in **lower-ranked** sources: Cite Sources gave +115.1% for the rank-5 site and −30.3% for the top-ranked one.
- Effects depend on the domain: quotations suit people/society/history; statistics suit law/government/opinion;
  cited sources suit factual and legal statements.
- Fluency + Statistics together beat any single method by more than 5.5%.
- Popular skills misquote this table (e.g. "Cite sources +40%"). Use the numbers above.

## Practical reading
Add real quotations from named people, real statistics with a source and a date, and links to primary sources. Write
fluently. Do not stuff keywords.
