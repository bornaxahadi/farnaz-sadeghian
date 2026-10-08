# Journal learnings (read first every run, update last)

## Setup
- Comment inbox: Composio Gmail account `gmail_accite-tailor`
  (decorwithfarnaz@gmail.com, connected 6 Oct 2026). FormSubmit sends both
  blog comments ("New blog comment: ...") and site inquiries ("New inquiry: ...")
  there. Ignore messages from before 6 Oct 2026 and test messages
  (names/text containing "test", sent from bornaxahadi@gmail.com).
- Images: Higgsfield gpt_image_2 via the Composio workbench (about 2
  credits each). Grok image generation is blocked on this account.
  Higgsfield free plan: only ONE job at a time (submit one, wait, then the
  next) and it ran OUT OF CREDITS on 6 Oct 2026. If it says "Out of
  credits", use the fallback: `mcp__Figma__generate_image` (planKey
  `team::1685251187745843425`, model `gpt-image-2.5-sunburst`, 1536x1024),
  then download its asset URL in the workbench (expires in 7 days), crop
  and push to blog-assets like the Higgsfield files. Uses Figma AI credits.
- Workbench image saving: on 7 Oct 2026 the workbench's PIL could not save WebP
  ("unsupported image mode"). Workaround that works: push the raw PNG to
  blog-assets as `incoming/<name>-src.png`, fetch it locally and make the
  4 sizes with local Pillow (supports WebP).
- Workbench: the kernel is shared with other sessions, so prefix your
  globals `tsj_`; calls over ~60s time out client-side, so run long work in
  a background thread and poll.

Newest first. Keep under 150 lines. Facts the agent learned from data,
readers and its own runs. Merge and prune; do not just append.

## Starting assumptions (6 Oct 2026, to be confirmed by data)
- Audience: Instagram/Facebook followers (Iran & Central Asia ~31%, UAE ~28%,
  US ~25%, Europe ~10%: owner's estimate), plus Google searchers looking
  for "<style> interior design" guides. English posts first.
- Style guides are evergreen: search demand is steady, so depth (complete
  guide + FAQ + palette) should beat news-style posts. Test this.
- Titles: "<Style> Interior Design: The Complete Guide to ..." pattern is
  the baseline. Try variants and record which earn clicks in Search Console.
- Persian, Moroccan, Arabic/majlis and modern Mediterranean topics fit
  Farnaz's audience and Dubai; mention Dubai apartments where natural.
- The Persian post (6 Oct) set the format: first-person Farnaz voice, two
  photos, FAQ, further reading. Keep that quality bar.

## What worked
- 8 Oct digest: 53 visitors/30d, first Google visit. Journal views: moroccan 4
  (leads), mid-century 2, scandinavian 2, persian 1. SEO suggests Dubai angle in
  every guide (a short "In a Dubai apartment" part + one FAQ naming Dubai) and
  Moroccan-adjacent topics earlier if Moroccan keeps leading.
- Comparison posts ("X vs Y") use slug `x-vs-y`, link both guides in the intro,
  and need a room-by-room section to reach full length.
- 7 Oct: SEO agent asked for short title tags (seoTitle <= 38 chars, as
  " | Third Skin Interiors" adds 22) and metaDesc 150-155 chars. Pattern now:
  seoTitle "<Style> Interior Style Guide" / "<Style> Interior Design".
- First Insights digest (7 Oct): 39 visitors in 30 days, journal views tiny
  (moroccan 3, scandinavian 2, persian 1), traffic is direct + Instagram,
  Google not yet. Ratings 4.0 (persian, scandinavian). Too early to judge.

## What to avoid

## Reader questions (topic ideas)
- First comment 6 Oct (Scandinavian): a short thank-you, no question yet.

## Week in review
