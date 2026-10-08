#!/usr/bin/env python3
"""Daily live follower check (Instagram + Facebook) for thirdskin.online.

Runs on GitHub Actions (every 6 hours) and from the daily Claude routine.
For each platform it tries, in order:
  0. a count passed on the command line (--ig 323300 --source vidiq), used by
     the Claude routine, which reads the public profile through vidIQ
  1. Meta Graph API (official, exact) if META_ACCESS_TOKEN + the account id env var are set
  2. Instagram's public profile JSON (web_profile_info), Instagram only
  3. the public profile page's og:description ("322K Followers, ...")
Every real count is saved to seo/data/followers-readings.csv, and gainPerDay
on the site is the real average daily growth between the oldest and newest
reading of the last 30 days, so the counter keeps moving between checks.
It rejects numbers that look wrong (unparseable, or more than 10% away from
the number currently on the site), and only then patches CONFIG.stats in
app.js and _src/app.part. Never writes anything else. Exit code is always 0
so a blocked platform never breaks the workflow; the report says what happened.
"""
import argparse, csv, datetime, json, os, re, sys, urllib.request, urllib.error

IG_URL = "https://www.instagram.com/decor.with.farnaz/"
FB_URL = "https://www.facebook.com/817038121486364"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
MAX_JUMP = 0.10
OUT = "seo/data"
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=4)))  # Dubai


ap = argparse.ArgumentParser()
ap.add_argument("--ig", type=int, help="Instagram count read elsewhere (e.g. vidIQ)")
ap.add_argument("--fb", type=int, help="Facebook count read elsewhere")
ap.add_argument("--source", default="manual", help="where --ig/--fb came from")
args = ap.parse_args()
READINGS = f"{OUT}/followers-readings.csv"


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9", **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def to_number(num, suffix):
    n = float(num.replace(",", ""))
    mult = {"k": 1e3, "m": 1e6}.get((suffix or "").lower(), 1)
    return int(round(n * mult))


def from_meta(html):
    """Parse '322K Followers' / '68,123 followers' from og:description or title."""
    tags = re.findall(r'<meta[^>]+(?:property|name)="(?:og:description|description)"[^>]+content="([^"]*)"', html)
    tags += re.findall(r'<meta[^>]+content="([^"]*)"[^>]+(?:property|name)="(?:og:description|description)"', html)
    for t in tags:
        m = re.search(r'([\d][\d.,]*)\s*([KkMm])?\s+[Ff]ollowers', t)
        if m:
            return to_number(m.group(1), m.group(2))
    return None


def from_graph(obj_id):
    token = os.environ.get("META_ACCESS_TOKEN")
    if not (token and obj_id):
        return None
    d = json.loads(get(f"https://graph.facebook.com/v21.0/{obj_id}?fields=followers_count&access_token={token}"))
    return int(d["followers_count"])


def from_ig_json():
    d = json.loads(get("https://i.instagram.com/api/v1/users/web_profile_info/?username=decor.with.farnaz",
                       {"x-ig-app-id": "936619743392459"}))
    return int(d["data"]["user"]["edge_followed_by"]["count"])


def current_value(platform):
    js = open("app.js", encoding="utf-8").read()
    m = re.search(platform + r":\{followers:([0-9.e+]+)", js)
    return int(float(m.group(1))) if m else None


def fetch(platform, url, id_env):
    notes = []
    given = getattr(args, platform)
    if given:
        return given, args.source, notes
    try:
        v = from_graph(os.environ.get(id_env))
        if v:
            return v, "graph-api", notes
    except Exception as e:
        notes.append(f"graph api failed: {str(e)[:80]}")
    if platform == "ig":
        try:
            return from_ig_json(), "public-json", notes
        except Exception as e:
            notes.append(f"public json failed: {str(e)[:80]}")
    try:
        v = from_meta(get(url))
        if v:
            return v, "public-page", notes
        notes.append("public page had no follower count (login wall or changed layout)")
    except Exception as e:
        notes.append(f"public page failed: {str(e)[:80]}")
    return None, None, notes


def patch(platform, value):
    changed = []
    for path, pat, rep in [
        ("app.js", platform + r":\{followers:[0-9.e+]+,", f"{platform}:{{followers:{value},"),
        ("_src/app.part", platform + r": \{ followers: [0-9]+,", f"{platform}: {{ followers: {value},"),
    ]:
        if not os.path.exists(path):
            continue
        s = open(path, encoding="utf-8").read()
        s2 = re.sub(pat, rep, s, count=1)
        if s2 != s:
            open(path, "w", encoding="utf-8").write(s2)
            changed.append(path)
    return changed


def save_reading(platform, value, source):
    new = not os.path.exists(READINGS)
    with open(READINGS, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["time", "platform", "followers", "source"])
        w.writerow([now.isoformat(timespec="seconds"), platform, value, source])


def gain_per_day(platform):
    """Real average daily growth between the oldest and newest reading of the last 30 days."""
    if not os.path.exists(READINGS):
        return None
    rows = [(datetime.datetime.fromisoformat(r["time"]), int(r["followers"]))
            for r in csv.DictReader(open(READINGS)) if r["platform"] == platform]
    rows = sorted(r for r in rows if (now - r[0]).days <= 30)
    if len(rows) < 2:
        return None
    days = (rows[-1][0] - rows[0][0]).total_seconds() / 864e2
    if days < 1:
        return None
    return max(0, round((rows[-1][1] - rows[0][1]) / days))


def patch_gain(platform, gain):
    for path, pat, rep in [
        ("app.js", r"(" + platform + r":\{followers:[0-9.e+]+,gainPerDay:)[0-9.e+]+", r"\g<1>" + str(gain)),
        ("_src/app.part", r"(" + platform + r": \{ followers: [0-9]+, +gainPerDay: )[0-9]+", r"\g<1>" + str(gain)),
    ]:
        if os.path.exists(path):
            s = open(path, encoding="utf-8").read()
            open(path, "w", encoding="utf-8").write(re.sub(pat, rep, s, count=1))


def patch_asof():
    stamp = now.strftime("%Y-%m-%dT%H:%M:%S+04:00")
    for path, pat, rep in [("app.js", r'asOf:"[^"]*"', f'asOf:"{stamp}"'),
                           ("_src/app.part", r'asOf: "[^"]*"', f'asOf: "{stamp}"')]:
        if os.path.exists(path):
            s = open(path, encoding="utf-8").read()
            open(path, "w", encoding="utf-8").write(re.sub(pat, rep, s, count=1))


results = {}
any_change = False
for platform, url, id_env in [("ig", IG_URL, "IG_USER_ID"), ("fb", FB_URL, "FB_PAGE_ID")]:
    cur = current_value(platform)
    val, source, notes = fetch(platform, url, id_env)
    r = {"site_now": cur, "found": val, "source": source, "notes": notes, "status": "", "files": []}
    if val is None:
        r["status"] = "NOT UPDATED - could not read live count"
    elif cur and abs(val - cur) / cur > MAX_JUMP:
        r["status"] = f"REJECTED - {val} is more than {int(MAX_JUMP*100)}% away from site value {cur}"
    elif val == cur:
        r["status"] = "unchanged"
        save_reading(platform, val, source)
    else:
        save_reading(platform, val, source)
        r["files"] = patch(platform, val)
        r["status"] = f"UPDATED {cur} -> {val}" if r["files"] else "NOT UPDATED - could not find CONFIG.stats to patch"
        any_change = any_change or bool(r["files"])
    results[platform] = r

if any_change:
    patch_asof()
    for p in ("ig", "fb"):
        g = gain_per_day(p)
        if g is not None and results[p]["files"]:
            patch_gain(p, g)
            results[p]["gain_per_day"] = g

os.makedirs(OUT, exist_ok=True)
report = {"checked_at": now.isoformat(timespec="seconds"), "results": results}
json.dump(report, open(f"{OUT}/followers-latest.json", "w"), indent=2)

md = [f"# Live followers - {now:%Y-%m-%d %H:%M} Dubai", "",
      "| Platform | On site before | Live count found | Source | Result |", "|---|---|---|---|---|"]
for p, name in (("ig", "Instagram"), ("fb", "Facebook")):
    r = results[p]
    md.append(f"| {name} | {r['site_now']} | {r['found']} | {r['source']} | {r['status']} |")
notes = [f"- {n}: {x}" for p in results for n in [p] for x in results[p]["notes"]]
if notes:
    md += ["", "Notes:"] + notes
if any(r["found"] is None for r in results.values()):
    md += ["", "To make this reliable, add repo secrets META_ACCESS_TOKEN, IG_USER_ID, FB_PAGE_ID "
           "(see seo/SETUP.md, section 6)."]
open(f"{OUT}/followers-latest.md", "w").write("\n".join(md) + "\n")

hist = f"{OUT}/followers-history.csv"
new = not os.path.exists(hist)
with open(hist, "a", newline="") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["date", "ig_found", "ig_status", "fb_found", "fb_status"])
    w.writerow([now.date(), results["ig"]["found"], results["ig"]["status"].split(" ")[0],
                results["fb"]["found"], results["fb"]["status"].split(" ")[0]])
print("\n".join(md))
sys.exit(0)
