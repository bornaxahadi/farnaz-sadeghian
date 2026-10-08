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
(none yet)

## What worked / what did not
(none yet)
