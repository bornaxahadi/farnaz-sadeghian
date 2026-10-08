# Search and AI visibility checks

Monthly snapshot using the small-business plugin's `seo-ai-visibility`
method: ask what a real customer would ask, record exactly what came back.
Results change from run to run; this is direction, not a ranking. No scores.

Fixed queries (keep the same ones so months compare):
1. "best interior decorator Dubai apartment consultation"
2. "Farnaz Sadeghian interior designer Dubai"
3. "Japandi vs Scandinavian interior style differences"

## 2026-10-08 (first run, web search)
| Query | thirdskin.online shown? | Who showed up |
|---|---|---|
| 1 | no | yellowpages-uae.com directory pages (937 interior decorators), techbullion, propertyfinder blog, luxxu |
| 2 | no | other people named Farnaz on LinkedIn; nothing about her or the site |
| 3 | no | homestyler, homedesigns.ai, bellastaging.ca, probuilder, meltflexai |

On-site check (repo files, the live site could not be fetched from the
sandbox): robots.txt allows all search and AI crawlers; llms.txt is complete;
homepage has ProfessionalService/LocalBusiness, Person, Book and FAQPage
schema and ~1,650 words in plain HTML; journal posts have BlogPosting,
FAQPage and BreadcrumbList. On-site is in good shape.

What this means: the gap is off-site. Even a search for her own name does
not find the site yet, so listings and mentions on other sites (Google
Business Profile, Yellow Pages UAE, Houzz, press quotes) are the priority.
Opening hours are not stated anywhere (only matters for a Google Business
Profile; ask Farnaz, never invent them).
