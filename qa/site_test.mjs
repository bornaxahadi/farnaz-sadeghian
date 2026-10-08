// Daily end-to-end test of the built site (repo root), run by the site-keeper agent.
// Serves the repo locally, opens every page in desktop and phone size with Chromium,
// and checks: page loads, no JS errors, no broken local links/images, follower counts
// rendered and matching CONFIG.stats, no sideways scroll on phones, key sections present.
// Usage: node qa/site_test.mjs [--shots]   (needs playwright-core, see qa/TASKS.md)
// Writes qa/report.json + qa/report.md; exit code 1 if any check FAILS.
import { createServer } from 'node:http';
import { readFileSync, existsSync, statSync, writeFileSync, readdirSync, mkdirSync } from 'node:fs';
import { join, extname, resolve } from 'node:path';
import { createRequire } from 'node:module';

const ROOT = resolve(new URL('..', import.meta.url).pathname);
const require = createRequire(process.env.PW_DIR ? join(process.env.PW_DIR, 'x.js') : import.meta.url);
const { chromium } = require('playwright-core');
const CHROME = process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const SHOTS = process.argv.includes('--shots');

const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.avif': 'image/avif', '.woff2': 'font/woff2', '.xml': 'application/xml', '.txt': 'text/plain',
  '.pdf': 'application/pdf', '.webmanifest': 'application/manifest+json' };
const server = createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  let f = join(ROOT, p);
  if (!f.startsWith(ROOT)) { res.writeHead(403).end(); return; }
  if (existsSync(f) && statSync(f).isDirectory()) f = join(f, 'index.html');
  if (!existsSync(f)) { res.writeHead(404).end('not found'); return; }
  res.writeHead(200, { 'content-type': TYPES[extname(f)] || 'application/octet-stream' });
  res.end(readFileSync(f));
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
const BASE = `http://127.0.0.1:${server.address().port}`;

const LANGS = ['', 'fa/', 'ar/', 'ru/', 'es/', 'it/', 'zh/', 'ja/', 'de/', 'fr/'];
const posts = readdirSync(join(ROOT, 'blog'), { withFileTypes: true })
  .filter(d => d.isDirectory() && existsSync(join(ROOT, 'blog', d.name, 'index.html'))).map(d => `blog/${d.name}/`);
const PAGES = [...LANGS, 'blog/', ...posts, 'privacy/'].filter(p => existsSync(join(ROOT, p, 'index.html')));

const stats = (() => {
  const js = readFileSync(join(ROOT, 'app.js'), 'utf8');
  const n = p => +(js.match(new RegExp(p + ':\\{followers:([0-9.e+]+)')) || [])[1];
  return { ig: n('ig'), fb: n('fb') };
})();

const results = [];
const add = (page, check, ok, detail = '', level = 'FAIL') =>
  results.push({ page: '/' + page, check, status: ok ? 'ok' : level, detail: String(detail).slice(0, 300) });

const browser = await chromium.launch({ executablePath: CHROME, args: ['--no-sandbox'] });
const linkSet = new Set();
for (const [vpName, vp] of [['desktop', { width: 1366, height: 900 }], ['phone', { width: 390, height: 844, isMobile: true, hasTouch: true }]]) {
  const ctx = await browser.newContext({ viewport: { width: vp.width, height: vp.height }, isMobile: !!vp.isMobile, hasTouch: !!vp.hasTouch });
  // keep tests offline and private: block analytics and other outside requests
  await ctx.route('**/*', r => r.request().url().startsWith(BASE) || r.request().url().startsWith('data:') ? r.continue() : r.abort());
  for (const p of PAGES) {
    const page = await ctx.newPage();
    const errors = [], bad = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => { if (m.type() === 'error' && !/net::ERR_FAILED|ERR_BLOCKED|Failed to load resource/.test(m.text())) errors.push(m.text()); });
    page.on('response', r => { if (r.url().startsWith(BASE) && r.status() >= 400) bad.push(`${r.status()} ${r.url().slice(BASE.length)}`); });
    const t0 = Date.now();
    let resp;
    try { resp = await page.goto(`${BASE}/${p}`, { waitUntil: 'load', timeout: 30000 }); }
    catch (e) { add(p, `${vpName}: loads`, false, e.message); await page.close(); continue; }
    const loadMs = Date.now() - t0;
    await page.waitForTimeout(1500);
    // scroll through so lazy sections, counters and images run
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } scrollTo(0, 0); });
    await page.waitForTimeout(1000);
    // follower cards count up from 0 once seen: bring them into view and let the count finish
    for (const k of ['ig', 'fb']) if (await page.$(`[data-count="${k}"]`)) {
      await page.evaluate(k => document.querySelector(`[data-count="${k}"]`).scrollIntoView({ block: 'center', inline: 'center' }), k);
      await page.waitForTimeout(3500);
    }
    add(p, `${vpName}: loads`, resp && resp.ok(), resp ? resp.status() : 'no response');
    add(p, `${vpName}: load time`, loadMs < 4000, `${loadMs} ms (local)`, 'WARN');
    add(p, `${vpName}: no JS errors`, errors.length === 0, errors.join(' | '));
    add(p, `${vpName}: no broken local files`, bad.length === 0, bad.join(', '));
    const info = await page.evaluate(() => ({
      title: document.title, h1: document.querySelectorAll('h1').length,
      overflow: document.documentElement.scrollWidth - innerWidth,
      brokenImgs: [...document.images].filter(i => i.complete && i.naturalWidth === 0 && !i.loading?.includes('lazy')).map(i => i.getAttribute('src')),
      noAlt: [...document.images].filter(i => !i.hasAttribute('alt')).length,
      ig: document.querySelector('[data-count="ig"]')?.textContent, fb: document.querySelector('[data-count="fb"]')?.textContent,
      links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')),
    }));
    add(p, `${vpName}: has title`, !!info.title, info.title);
    add(p, `${vpName}: one h1`, info.h1 === 1, `${info.h1} h1 tags`, 'WARN');
    add(p, `${vpName}: no sideways scroll`, info.overflow <= 1, `${info.overflow}px wider than screen`);
    add(p, `${vpName}: images load`, info.brokenImgs.length === 0, info.brokenImgs.join(', '));
    add(p, `${vpName}: images have alt`, info.noAlt === 0, `${info.noAlt} without alt`, 'WARN');
    if (info.ig !== undefined) {
      const num = s => +String(s || '').replace(/[۰-۹]/g, d => '۰۱۲۳۴۵۶۷۸۹'.indexOf(d)).replace(/[٠-٩]/g, d => '٠١٢٣٤٥٦٧٨٩'.indexOf(d)).replace(/[^0-9]/g, '');
      for (const k of ['ig', 'fb']) {
        const shown = num(info[k]);
        add(p, `${vpName}: ${k} count shown`, shown >= stats[k] && shown < stats[k] * 1.1, `shows ${info[k]}, data ${stats[k]}`);
      }
    }
    for (const h of info.links) if (h && !/^(https?:|mailto:|tel:|#|javascript:|whatsapp:)/.test(h)) linkSet.add(new URL(h, `${BASE}/${p}`).pathname);
    if (SHOTS && (p === '' || p === 'blog/')) {
      mkdirSync(join(ROOT, 'qa', 'shots'), { recursive: true });
      await page.screenshot({ path: join(ROOT, 'qa', 'shots', `${(p || 'home').replace(/\//g, '')}-${vpName}.png`), fullPage: false });
    }
    await page.close();
  }
  await ctx.close();
}
await browser.close();
for (const l of linkSet) {
  const f = join(ROOT, decodeURIComponent(l));
  const ok = existsSync(f) && (!statSync(f).isDirectory() || existsSync(join(f, 'index.html')));
  add(l.replace(/^\//, ''), 'internal link target exists', ok, l);
}
server.close();

const fails = results.filter(r => r.status === 'FAIL'), warns = results.filter(r => r.status === 'WARN');
const md = [`# Site test ${new Date().toISOString()}`, '',
  `${PAGES.length} pages x 2 screen sizes, ${linkSet.size} internal links. ${fails.length} FAIL, ${warns.length} WARN.`, ''];
for (const r of [...fails, ...warns]) md.push(`- ${r.status} ${r.page} ${r.check}: ${r.detail}`);
if (!fails.length && !warns.length) md.push('Everything passed.');
writeFileSync(join(ROOT, 'qa', 'report.md'), md.join('\n') + '\n');
writeFileSync(join(ROOT, 'qa', 'report.json'), JSON.stringify({ pages: PAGES, stats, results }, null, 1));
console.log(md.join('\n'));
process.exit(fails.length ? 1 : 0);
