# Daily SEO runbook

Run in order. Write results to seo/log.md.

## 1. Technical audit (English page https://thirdskin.online/ only)
Other language folders are out of scope: do not audit or edit them.
- Title < 60 chars, meta description < 160
- canonical, html lang="en" (leave existing hreflang tags untouched)
- og:* and twitter:* tags, og-image exists
- One H1, logical H2/H3
- Images: alt text, width/height, WebP, lazy-loading
- JSON-LD valid and matches visible text
- sitemap.xml: update lastmod only for the English URL when it changed
- robots.txt allows crawlers; llms.txt facts match the site
- Live check: WebFetch https://thirdskin.online/, confirm HTTP 200 and
  that the live page matches the repo

## 1b. Website health and speed (every day)
Health (live site, https://thirdskin.online/):
- HTTP 200 for /, /sitemap.xml, /robots.txt, /llms.txt, /manifest.webmanifest,
  /sw.js, /media-kit.pdf; HTTPS valid; no redirect loops; CNAME intact
- Every <img>, <script>, <link> and internal #anchor on the English page
  resolves (no 404s); no JavaScript errors in app.js logic you can see
- Structured data and HTML still parse after yesterday's changes
Speed:
- Run Google PageSpeed Insights (mobile + desktop):
  https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://thirdskin.online/&strategy=mobile
  Record performance score, LCP, CLS, INP/TBT, page weight in seo/log.md
- Known heavy files (fix first): img/third-skin-animated-logo.gif (~1.8 MB),
  JPG images that have WebP twins, index.html (~190 KB)
Fix automatically when something is wrong:
- Convert/resize oversized images to WebP (keep the original file name base,
  update references, keep the old file until the new one is verified live)
- Replace heavy GIFs with video/WebP or smaller versions
- Add width/height, loading="lazy" (not on the hero), fetchpriority on hero
- defer/async non-critical scripts, font-display: swap, preload hero + fonts
- Repair broken links/paths; restore anything the last run broke
- If a fix makes things worse (score drops, page breaks), revert it at once
Do not remove features or change the design to gain speed.

## 2. Fix safe items (see "MAY change" in the agent file)

## 3. Search and visitor data (if set up, see seo/SETUP.md)
- Read newest files in seo/data/ (Search Console exports, analytics export)
- Report: visitors, top countries, top pages, top queries
- Quick wins: queries at position 5-20; pages with high impressions and
  low click-through rate -> rewrite title/description

## 4. Email signup
- Confirm the signup form exists on the English page and has consent
  checkbox and privacy link
- Report signup count if the owner supplied it
- Suggest one improvement (placement, lead magnet, wording)

## 5. Growth ideas (pick 1-3 per run, keep a list in seo/ideas.md)
- A new visible FAQ item answering a real search query
- An internal-link or heading improvement
- A shareable page idea (e.g. "50 interior styles" from the book)
- Instagram/Facebook post that links to a specific page (UTM-tagged)
- Google Business Profile post / photo / review request

## 6. Real-traffic outreach (see seo/TRAFFIC.md)
- Research 3-5 new places real interior design fans gather (communities,
  directories, blogs, collaborators, questions on Quora/Reddit)
- Check their rules; draft helpful, honest, non-spammy posts or pitches
- Add them to seo/outreach.md under "Ready for Farnaz" with a UTM link
- Review which sources sent visitors (analytics) and update the plan

## 7. Publish
Run `bash _src/build.sh` after editing `_src/`, check the diff, commit and push to main, then ping IndexNow with the changed URLs (key and format in the agent file).

## 8. Log
Add a row to seo/log.md: date | change | files.
