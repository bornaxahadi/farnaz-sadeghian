# SEO change log

| Date | Change | Files |
|------|--------|-------|
| 2026-10-06 | Created seo-agent, keywords and log | .claude/agents/seo-agent.md, seo/ |
| 2026-10-06 | Agent expanded: daily runbook, setup guide, safety rules | .claude/agents/seo-agent.md, seo/ |
| 2026-10-06 | Scope changed to English page only | .claude/agents/seo-agent.md, seo/ |
| 2026-10-06 | Full autonomy: agent publishes directly to main, no approvals | .claude/agents/seo-agent.md, seo/SETUP.md |
| 2026-10-06 | Added daily health + speed check and auto-fix | seo/TASKS.md, .claude/agents/seo-agent.md |
| 2026-10-06 | Agent files published to main; noted Search Console verification file | .claude/, seo/ |
| 2026-10-06 | Shortened English title (84 to 57 chars) and meta/og/twitter/JSON-LD description (188 to 147 chars, dropped follower count from the snippet only; still shown on page). Edited index.html directly and mirrored in _src/i18n.js and _src/seo_alts.py (esbuild missing here, so no rebuild; other languages untouched) | index.html, _src/i18n.js, _src/seo_alts.py |
| 2026-10-06 | Health: live checks BLOCKED (sandbox egress proxy returns 403 for thirdskin.online; PageSpeed API returned 429). No live HTTP status or PSI numbers today. Local checks OK: all 44 img tags have alt/width/height, all local src/href exist, no broken #anchors, one H1, JSON-LD parses, sitemap lastmod 2026-10-06 | none |
| 2026-10-06 | Images: img/third-skin-animated-logo.gif (1.78 MB) and big JPGs (farnaz-carpet, book-cover, etc.) are NOT referenced by the English page or app.js; the JPGs are used by other-language pages (out of scope), the GIF by nothing. Left in place (no visitor cost, nothing to convert); delete GIF later if confirmed unused | none |
| 2026-10-06 | Outreach: 5 drafts added (FindMyDesignerDubai, Houzz, Pinterest, Home Renovation AE guest post, Dubai Design Week 3-8 Nov) | seo/outreach.md |
| 2026-10-06 | Data/email: seo/data empty (no data yet). Launch-list form with consent + privacy link per SETUP.md; FormSubmit must be activated by owner; signup count not supplied | none |
| 2026-10-06 | Added daily live follower check (Action + agent task 1c) | .github/scripts/followers.py, seo/TASKS.md |
| 2026-10-07 | Team: Insights digest. 32 visitors, 53 sessions, 83 views in 30 days. Top: / 62, /fa/ 14, journal 4 views (scandinavian 2, moroccan 1, persian 1); ratings 4.0 x2. Sources: direct 39, not set 35, ig 4. Board note to SEO closed (posts in sitemap). 3 notes left for blog (title/meta length, Japandi vs Scandinavian topic, early numbers) | agents/board.md |
| 2026-10-07 | Fixed Instagram count mismatch: llms.txt and the static counter said 321,000, while the live counter (CONFIG.stats) says 322,000. Total 390K unchanged | _src/build2.py, _src/body.part, all built pages, llms.txt |
| 2026-10-07 | llms.txt now lists every journal article with its title and summary, added automatically on each build, so AI assistants can cite the posts | _src/build2.py, llms.txt |
| 2026-10-07 | Health: all 10 URLs 200. Lighthouse mobile 46 (LCP 4.48 s, TBT 2010 ms, CLS 0.002), desktop 100. Mobile has varied 90 / 60 / 46 across runs. The 90 and 60 were on the same code 8 minutes apart, so a single run is noisy. A local trace with 4x CPU slowdown shows mostly style/layout work from many infinite CSS animations (hero art); yesterday's code ~340 ms blocking vs today ~450 ms, a small change. No fix pushed: it is the design, and the rules say don't change design for speed. Owner option: pause the decorative animations on phones or until first scroll | none |
| 2026-10-07 | Skipped: English title is 80 chars and description 160+, but the owner tuned both on 6 Oct with Keyword Planner data after my shortening, so I left them. meta-viewport audit fails (user-scalable=no blocks pinch zoom; accessibility). Left for owner to decide | none |
| 2026-10-07 | Followers: NOT UPDATED for 2 days (IG login wall, FB HTTP 400). Site keeps 322K + 68K. If still failing tomorrow, owner needs the Meta token (SETUP.md section 6) | none |
| 2026-10-07 | Outreach: 5 drafts added (Instagram journal links, Pinterest journal pins, Style Curator pitch, Clutch listing, Japandi vs Scandinavian answers) | seo/outreach.md |
| 2026-10-08 | Team: 49 visitors, 84 sessions, 121 views (30 days). Top / 85, /fa/ 22; journal: moroccan 4, mid-century 2, scandinavian 2, persian 1. First Google visit (1) and ig 7. Closed the blog's note (mid-century post is in sitemap + llms.txt). Left 2 notes for blog (Dubai angle vs local competitors; Moroccan leading) | agents/board.md |
| 2026-10-08 | IndexNow: the sandbox cannot reach api.indexnow.org (proxy 403), so the GitHub Action now also pings the homepage and llms.txt when they change (it already handled blog/) | .github/workflows/blog-indexnow.yml |
| 2026-10-08 | Health: all URLs 200. Lighthouse mobile 64 (LCP 2.92 s, TBT 1701 ms), desktop 100. Last 4 runs 90/60/46/64: noisy, no new regression. Cause is still the decorative animations (design, left as is) | none |
| 2026-10-08 | Followers: NOT UPDATED 3 days in a row (6-8 Oct). Public pages are blocked; marked SETUP.md section 6 as BLOCKED. The owner needs to add the Meta token. Numbers stay at 322K + 68K; no guessing | seo/SETUP.md |
| 2026-10-08 | Outreach: 4 drafts added (Bing Places, Gulf News expert source, Homeadore project, Expat.com forum) | seo/outreach.md |
| 2026-10-08 | No English page change today: title/meta left as the owner set them; audit otherwise clean (1 H1, JSON-LD valid, all images have alt and size) | none |
