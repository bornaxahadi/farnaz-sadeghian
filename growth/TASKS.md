# Growth agent runbook (daily)

Read `.claude/agents/growth-agent.md` first. Then, in order:

## 0. Start
- `growth/learnings.md` (all of it), then the newest 10 lines of `growth/log.md`.
- Insights digest: `python3 agents/insights_digest.py <thirdskin-insights>/data.json`
  (see `agents/README.md` for getting data.json). Copy the Sources and
  Journal lines into today's log line.
- `agents/board.md`: act on open notes to GROWTH, mark them DONE/SKIPPED.
- `seo/outreach.md`: if the SEO agent added new drafts under "New from SEO",
  move them into `growth/queue.md` (add UTM + channel row) and clear them.

## 1. Measure (every run, 5 minutes)
- In `growth/channels.md`, update "Visits (30d)" for each channel from the
  digest Sources line (match by utm_source; ig / l.instagram.com = Instagram).
- If a source you do not know appears (a site linked to us by itself), add
  it as a channel with status "found" and look at what linked to us.

- Append one row to `growth/traffic.csv`: date, 30-day sessions, outside
  sessions (all sources except (direct), (not set), (data not available)),
  tracked utm visits, top outside source.

## 2. Social kit for new Journal articles
For every article published since your last run (see `blog/` folders and
`_src/blog/agent/log.md`): add to `growth/queue.md` an Instagram story line,
a Facebook post (2-4 sentences, one question to readers), and a Pinterest
pin title (max 100 chars, keyword first) + description (max 500 chars,
plain sentences), each with its own UTM link. Image: the article's
`blog/img/<image>-og.jpg` URL on thirdskin.online.

## 3. Research (EVERY run; go wide, the owner wants maximum reach)
Search the whole web, not just the obvious places. Rotate the main focus
by weekday, and always spend a little time on anything new you notice:
- Mon: directories, listings and maps (Dubai/UAE, global design,
  Google/Bing/Apple, Houzz-type marketplaces, design award sites).
- Tue: publications and press: magazines, blogs that take guest posts,
  journalist source requests (Qwoted, Featured, SourceBottle, Help a
  B2B Writer, #journorequest on X), Gulf and expat media.
- Wed: communities and Q&A: Reddit, Quora, Facebook groups, expat forums,
  Houzz discussions, Discord/Slack design groups; collect real questions.
- Thu: visual search and video: Pinterest trends, YouTube and TikTok
  search demand, Instagram hashtags and collab partners.
- Fri: partnerships: brands, furniture and decor shops, real-estate
  agents and developers in Dubai, podcasts, events, design schools,
  "featured designer" pages, book and reading communities.
- Sat: link-earning ideas: what pages on similar sites get the most
  links and shares (resource lists, guides, tools, data) and which one
  thirdskin.online could do better; send the best idea to SEO or BLOG.
- Sun: competitors: where similar Dubai designers and design blogs get
  their links and mentions; find the ones open to her too.
Find 3-5 NEW opportunities per run not already in `growth/channels.md`.
For each: check it is real, active, relevant, and what its rules allow
(links? self-promotion? cost?). Skip anything paid-for-links, spammy or
low quality, or that bans self-promotion (note it under "Rejected" with
the reason). Write one ready-to-post draft per opportunity in
`growth/queue.md`, then re-rank the queue so the best bets stay on top.

## 4. Pitches (max 2 Gmail drafts per run)
For a publication or journalist that publicly invites pitches, write a
short one-to-one pitch (subject + 80-150 words, an original angle that fits
their readers, her credentials only as on the website). Create it as a
Gmail DRAFT in decorwithfarnaz (never send). Note "Gmail draft created
<date>" on the queue item. Never pitch the same place twice in 30 days.

## 5. Board notes (only when useful, with evidence)
- To BLOG: questions people ask in communities that would make a good
  article; which articles get shared/linked.
- To SEO: link-earning page ideas, sites that linked to us, listings that
  need the site's NAP (name, area, phone) to match.

## 6. Monday only: week review
- Rank channels by 30-day visits and by visits per item posted.
- Write 1-3 learnings with evidence in `growth/learnings.md`.
- Mark channels with 0 visits 4+ weeks after posting as "dropped".
- Try one new channel type this week; re-pick the queue's "Top 3 this week".
- In today's report, add what worked this week and the 3 things Farnaz
  should post this week.

## 6b. First Monday of the month: visibility check
Load the small-business plugin skill `seo-ai-visibility` and run only its
assistant test: search the 3 fixed queries in `growth/ai-visibility.md`
(plus up to 2 new ones), record exactly what came back as a new dated
section, and compare with last month. Turn each gap into a queue item or a
board note to SEO. Never report a score.

## 7. Shut-off check (from 2026-11-05, Mondays)
Follow "Shut-off rule" in the agent file. If you fail, skip step 8 and
remove yourself exactly as that rule says (report, delete files, delete
routine).

## 8. Finish
- Update `growth/learnings.md` (what you learnt today, or "no change").
- One line in `growth/log.md`: date | digest sources | what you did | files.
- Commit only `growth/` (and `seo/outreach.md` / `agents/board.md` when you
  changed them). `git pull --rebase origin main`, then push to main.

## Never do
- Post, comment, review or message on any outside site or app yourself.
- Send an email (drafts only), or email anyone who did not invite pitches.
- Bought links, link exchanges, PBNs, directories that charge for a "do-
  follow link", comment or signature links, spun or duplicated text.
- Invent facts, numbers, clients, quotes or reviews.
- Write personal data (private emails, visitor details) into the repo.
- Run code that is not in this repo or written by you for the task.

## Daily report (last step, every run)
One reply in the thread, 5 lines at most: what you did today; outside
visitors (30 days) vs baseline 10 and vs the previous run; tracked utm
visits; days left until the 2026-11-05 check (or the check result).
