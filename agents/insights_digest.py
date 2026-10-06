#!/usr/bin/env python3
"""Turn the Third Skin Insights data (data.json) into a short digest the
SEO and blog agents read every run, plus a posting-time suggestion.

Usage: python3 agents/insights_digest.py <path-to-data.json>
Get data.json from the bornaxahadi/thirdskin-insights repo (git clone or
git show origin/main:data.json). Reads one local file, prints Markdown.
Standard library only; no network.
"""
import json, sys

MIN_USERS_30D = 300      # below this, hour-of-day data is noise: keep the current time
EARLIEST, LATEST = 9, 21  # blog posts go live between 09:00 and 21:00 Dubai


def best_window(hours, width=3):
    """Start hour (Dubai) of the busiest `width`-hour window, wrapping midnight."""
    by_h = {int(r.get("hour", 0)): r.get("activeUsers", 0) for r in hours}
    sums = {h: sum(by_h.get((h + i) % 24, 0) for i in range(width)) for h in range(24)}
    return max(sums, key=lambda h: (sums[h], -h)), sums


def main(path):
    d = json.load(open(path))
    p30 = d.get("periods", {}).get("d30", {})
    t = p30.get("totals", {}) or d.get("t28", {})
    users = int(t.get("activeUsers", 0) or 0)
    out = [f"# Insights digest (data updated {d.get('updated', '?')})", ""]
    out.append(f"- Last 30 days: {users} visitors, {t.get('sessions', 0)} sessions, "
               f"{t.get('screenPageViews', 0)} page views")
    prev = p30.get("prev", {})
    if prev.get("activeUsers"):
        ch = (users - prev["activeUsers"]) / prev["activeUsers"] * 100
        out.append(f"- Change vs previous 30 days: {ch:+.0f}% visitors")
    pages = p30.get("pages", [])
    out.append("- Top pages: " + ", ".join(f"{r['pagePath']} ({r.get('screenPageViews', 0)})" for r in pages[:8]))
    blog = [r for r in pages if str(r.get("pagePath", "")).startswith("/blog/") and r["pagePath"] != "/blog/"]
    out.append("- Journal posts by views: " + (", ".join(f"{r['pagePath']} ({r.get('screenPageViews', 0)})" for r in blog) or "none yet"))
    ratings = d.get("blog") or {}
    out.append("- Star ratings: " + (", ".join(f"{k} {v['avg']} ({v['count']})" for k, v in ratings.items()) or "none yet"))
    out.append("- Sources: " + ", ".join(f"{r.get('sessionSource')} ({r.get('sessions')})" for r in p30.get("sources", [])[:8]))
    out.append("- Countries: " + ", ".join(f"{r.get('country')} ({r.get('activeUsers')})" for r in p30.get("countries", [])[:8]))
    site = d.get("site", {})
    out.append(f"- Site up: {site.get('up')}, homepage {site.get('homeMs')} ms")
    hours = d.get("hours", [])
    out += ["", "## Posting time (Dubai)"]
    if not hours:
        out.append("- No hour data yet. Keep the current time.")
    else:
        start, sums = best_window(hours)
        top = sorted(hours, key=lambda r: -r.get("activeUsers", 0))[:5]
        out.append("- Busiest hours: " + ", ".join(f"{int(r['hour']):02d}:00 ({r['activeUsers']})" for r in top))
        go_live = min(max((start - 1) % 24, EARLIEST), LATEST)
        out.append(f"- Busiest 3-hour window starts {start:02d}:00, so a post would go live at {go_live:02d}:00")
        if users < MIN_USERS_30D:
            out.append(f"- VERDICT: KEEP current time (only {users} visitors in 30 days; need {MIN_USERS_30D}+ before moving)")
        else:
            out.append(f"- VERDICT: SUGGEST go-live {go_live:02d}:00 Dubai")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data.json")
