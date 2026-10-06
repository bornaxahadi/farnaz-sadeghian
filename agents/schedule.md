# Journal posting time

Current go-live time: **16:00 Dubai** (blog routine fires at 15:38).

The blog agent may move this itself, following these rules:
- Check once a week, on its "Week in review" run, using the "Posting time"
  part of the Insights digest (`agents/insights_digest.py`).
- Move only when the digest verdict says SUGGEST (300+ visitors in the last
  30 days) and the suggested time is 2 or more hours away from the current
  one. At most one move per 7 days.
- Go-live time must be between 09:00 and 21:00 Dubai (the SEO agent runs
  at 06:46).
- To move: update its own routine (`update_trigger` on
  trig_01RedQdouzkH1yuX8Jxz7n3e) with cron
  `CRON_TZ=Asia/Dubai 38 <go-live hour minus 1> * * *`, keep the prompt as is.
  Then update the line above and add a row below. If the change is refused,
  leave a note on board.md and tell the owner in the run's reply.
- Two weeks after a move, compare journal page views per day before and
  after. If they fell, move back and log it.

| Date | Change | Evidence |
|---|---|---|
| 2026-10-06 | Start at 16:00 | Owner's choice; 29 visitors in 30 days, too little data to decide |
