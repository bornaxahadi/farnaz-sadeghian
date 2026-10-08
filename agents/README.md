# How the Third Skin agents work together

These automatic agents look after thirdskin.online. They share what they
learn through the files in this folder, so each one gets better from the
others' findings.

| Agent | When (Dubai) | Gives the others | Uses from the others |
|---|---|---|---|
| Insights (data collector) | every 3 hours | visitor numbers in `data.json` (repo bornaxahadi/thirdskin-insights): busiest hours, top pages, journal post views, star ratings, sources, countries, site health | (data source only) |
| SEO agent | 06:46 daily | keyword and search findings, topic ideas, title/meta advice for journal posts, technical problems | Insights numbers, new journal posts from the blog agent |
| Blog (Style Journal) agent | 15:38 daily (can move itself, see `schedule.md`) | what it published, its target keywords, reader questions | Insights numbers, SEO topic ideas and advice |
| Site keeper | 13:13 daily | daily test of every page, fixes, design/copy improvements, checks every agent ran and nudges it (board note, or one re-run) | everything: health report, Insights, every agent's log |
| Growth agent | 10:54 daily | which outside channels send visitors, questions people ask in communities, link-earning page ideas, sites that link to us | Insights sources, new journal posts, SEO outreach ideas |

## Every run, every writing agent (SEO, blog, growth)
1. Get the latest Insights data:
   `git clone --depth 1 https://github.com/bornaxahadi/thirdskin-insights /tmp/tsi`
   (or `git -C /tmp/tsi pull`; attach the repo with add_repo, read access,
   if the clone is refused), then
   `python3 agents/insights_digest.py /tmp/tsi/data.json`.
   Use the digest in your work and copy its key lines into your own log.
2. Read `board.md`: every open note addressed to you. Act on it, then mark
   it `DONE <date>: what you did` (or `SKIPPED <date>: why`).
3. Before you finish, add notes for the other agents when you have something
   useful for it (newest at the top of "Open notes"). One note = one
   concrete finding or request, with the evidence.

## Rules
- Facts only, from data or research. No personal data (no emails, no
  visitor details) in these files: the repo is public.
- Each agent changes only its own files. To change another agent's work,
  leave a note; do not edit its files.
- Only run code from this repository (like `insights_digest.py`).
- Nothing is ever posted on other people's websites automatically. The
  growth agent prepares drafts in `growth/queue.md`; Farnaz posts them.
