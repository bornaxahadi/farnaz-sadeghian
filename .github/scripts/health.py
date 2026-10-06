#!/usr/bin/env python3
"""Daily live-site health + speed report for thirdskin.online.

Runs on GitHub Actions (which can reach the public internet) and writes
seo/data/health-latest.md, seo/data/health-latest.json and appends a row to
seo/data/health-history.csv, so the SEO agent can read real numbers even when
its own sandbox cannot reach the site. Exit code 1 if any URL is unhealthy.
"""
import csv, datetime, json, os, subprocess, sys, time, urllib.error, urllib.request

BASE = "https://thirdskin.online"
URLS = ["/", "/sitemap.xml", "/robots.txt", "/llms.txt", "/manifest.webmanifest",
        "/sw.js", "/media-kit.pdf", "/privacy/", "/img/og-image.jpg", "/app.js"]
OUT = "seo/data"
now = datetime.datetime.now(datetime.timezone.utc)


def check(path):
    url = BASE + path
    t0 = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "thirdskin-health-check"})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read()
            return {"url": url, "status": r.status, "ms": int((time.time() - t0) * 1000),
                    "bytes": len(body), "final": r.geturl()}
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code, "ms": int((time.time() - t0) * 1000), "bytes": 0, "final": url}
    except Exception as e:
        return {"url": url, "status": 0, "ms": int((time.time() - t0) * 1000), "bytes": 0,
                "final": url, "error": str(e)[:120]}


def lighthouse(preset):
    out = f"lh-{preset}.json"
    cmd = ["npx", "--yes", "lighthouse@12", BASE + "/", "--quiet",
           "--chrome-flags=--headless=new --no-sandbox", "--output=json", f"--output-path={out}",
           "--only-categories=performance,seo,accessibility,best-practices"]
    if preset == "desktop":
        cmd.append("--preset=desktop")
    try:
        subprocess.run(cmd, check=True, timeout=600, capture_output=True, text=True)
        d = json.load(open(out))
        a = d["audits"]
        g = lambda k: a[k].get("numericValue")
        return {
            "performance": round(d["categories"]["performance"]["score"] * 100),
            "seo": round(d["categories"]["seo"]["score"] * 100),
            "accessibility": round(d["categories"]["accessibility"]["score"] * 100),
            "best_practices": round(d["categories"]["best-practices"]["score"] * 100),
            "lcp_s": round(g("largest-contentful-paint") / 1000, 2),
            "cls": round(g("cumulative-layout-shift"), 3),
            "tbt_ms": round(g("total-blocking-time")),
            "page_kb": round(g("total-byte-weight") / 1024),
            "failed": sorted(k for k, v in a.items()
                             if v.get("score") is not None and v["score"] < 0.9
                             and v.get("scoreDisplayMode") in ("numeric", "binary"))[:15],
        }
    except Exception as e:
        return {"error": str(e)[:200]}


checks = [check(p) for p in URLS]
bad = [c for c in checks if c["status"] != 200]
lh = {"mobile": lighthouse("mobile"), "desktop": lighthouse("desktop")}

report = {"checked_at": now.isoformat(timespec="seconds"), "healthy": not bad,
          "checks": checks, "lighthouse": lh}
os.makedirs(OUT, exist_ok=True)
json.dump(report, open(f"{OUT}/health-latest.json", "w"), indent=2)

md = [f"# Live site health and speed - {now:%Y-%m-%d %H:%M} UTC", "",
      f"**Status: {'HEALTHY' if not bad else 'PROBLEM - ' + str(len(bad)) + ' URL(s) failing'}**", "",
      "| URL | HTTP | ms | KB |", "|---|---|---|---|"]
md += [f"| {c['url']} | {c['status']} | {c['ms']} | {c['bytes'] // 1024} |" for c in checks]
md += ["", "## Lighthouse (home page)", "",
       "| | Perf | SEO | A11y | Best practices | LCP s | CLS | TBT ms | Page KB |",
       "|---|---|---|---|---|---|---|---|---|"]
for k, v in lh.items():
    if "error" in v:
        md.append(f"| {k} | error: {v['error']} |")
    else:
        md.append(f"| {k} | {v['performance']} | {v['seo']} | {v['accessibility']} | {v['best_practices']} | "
                  f"{v['lcp_s']} | {v['cls']} | {v['tbt_ms']} | {v['page_kb']} |")
for k, v in lh.items():
    if v.get("failed"):
        md += ["", f"Audits below 90 ({k}): " + ", ".join(v["failed"])]
open(f"{OUT}/health-latest.md", "w").write("\n".join(md) + "\n")

hist = f"{OUT}/health-history.csv"
new = not os.path.exists(hist)
with open(hist, "a", newline="") as f:
    w = csv.writer(f)
    if new:
        w.writerow(["date", "healthy", "failing_urls", "mobile_perf", "mobile_lcp_s", "mobile_cls",
                    "mobile_tbt_ms", "desktop_perf", "page_kb"])
    m, d = lh["mobile"], lh["desktop"]
    w.writerow([now.date(), int(not bad), len(bad), m.get("performance"), m.get("lcp_s"), m.get("cls"),
                m.get("tbt_ms"), d.get("performance"), m.get("page_kb")])

print("\n".join(md))
sys.exit(1 if bad else 0)
