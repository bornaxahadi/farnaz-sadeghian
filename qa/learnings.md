# Site keeper learnings

Read first, update last, every run. Keep under 120 lines: merge or drop
stale items.

## How this site works (facts)
- Follower cards count up from 0 when they scroll into view; on phones the
  Facebook card sits beside the Instagram card, so it only counts once it
  is scrolled into view (the test does this). Not a bug.
- Browsers cache `app.js?v=<hash>`; the hash only changes on a rebuild or a
  followers.py run. A change to app.js without a new hash is invisible to
  returning visitors.
- Followers: Instagram is read daily via vidIQ; Facebook needs a Meta
  token (seo/SETUP.md section 6), until then the owner sends screenshots.

## Ideas from other sites (URL, what, fits? status)
- 2026-10-09 kellywearstler.com: credibility from named brand partners and a footer Press page; weekly-updates signup with a clear thank-you state. Fits only with real partners Farnaz already lists; never invent. OPEN.
- 2026-10-09 amberinteriordesign.com: very quiet homepage, Contact is only a nav link, books get top-level links. Our site already does more; confirms the book section is a good anchor. NOTED.
- 2026-10-09 own phone review: under 520px the nav hides "Get in touch", so on phones the only contact path is the WhatsApp bubble; the hero buttons are Instagram + Brand collaborations. Candidate: a small "Book a consultation" text link under the hero buttons on phones (English copy already exists in i18n?). CHECK space and RTL first. OPEN.
- 2026-10-09 blog phone header: "Style Journal" and "Book a consultation" both wrap to two lines at 390px (blog lane, note sent to BLOG). OPEN.

## What worked / what did not
- 2026-10-09: studiomcgee.com blocks fetches; pick other sites.
- Full-page screenshots repeat the fixed header in each slice; that is the capture, not a bug.
