# Site keeper runbook (daily)

Playbook and rules: `.claude/agents/site-keeper.md`. Follow them.

## 0. Start
```
cd /home/claude/farnaz-sadeghian   # or clone bornaxahadi/farnaz-sadeghian
git fetch origin main && git checkout main && git reset --hard origin/main
mkdir -p /tmp/qa-deps && (cd /tmp/qa-deps && npm i playwright-core@1.56.1 >/dev/null)
npm i -g esbuild@0.24.0 >/dev/null
```
Read `qa/learnings.md`, the last 10 lines of `qa/log.md`, and
`agents/board.md` (notes to KEEPER).

## 1. Test
```
PW_DIR=/tmp/qa-deps/node_modules node qa/site_test.mjs --shots
```
- Tests every page (10 languages, Journal, posts, privacy) on desktop and
  phone: loads, JS errors, broken files/images/links, sideways scroll,
  follower counts shown match the data, titles, h1, alt text.
- Look at `qa/shots/*.png` yourself (Read the images): anything ugly,
  cut off, overlapping, empty or out of date counts as a bug.
- Live site: this sandbox may not reach thirdskin.online. Read
  `seo/data/health-latest.md` (written by the 06:00 Action from GitHub's
  servers) for live status codes and Lighthouse scores.
- Fix every FAIL in your lane now (rebuild, re-test). FAILs in another
  agent's lane: board note to that agent.

## 2. Agents
Check each row of the Team table in the playbook. Missing proof ->
`get_trigger` on its id (do not call list_triggers: the account has many routines and the list is huge), board note, and at most one `fire_trigger` per agent per
day if it is enabled and missed today. Record the result in the log line.

## 3. Learn
Insights digest:
```
git clone --depth 1 https://github.com/bornaxahadi/thirdskin-insights /tmp/tsi 2>/dev/null || git -C /tmp/tsi pull -q
python3 agents/insights_digest.py /tmp/tsi/data.json
```
Study 2-3 real sites (WebSearch/WebFetch). Add findings with URLs to
`qa/learnings.md`.

## 4. Improve (max 2 changes)
Pick the best idea from learnings that fits your lane. Edit `_src/`,
`bash _src/build.sh`, test again (0 FAIL), compare screenshots, commit
"Site keeper: <what>", push. Pull --rebase and retry if the push is
refused. Never leave main red.

## 5. Finish
- `qa/log.md`: one line `| date | tests | agents | change | idea |`.
- `qa/learnings.md`: update.
- Board notes for other agents (newest at top of Open notes).
- Commit `qa/` (not `qa/shots/`, it is git-ignored), push.
- Post the short report in your thread.
