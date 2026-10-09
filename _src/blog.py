"""Style Journal (blog) builder for thirdskin.online.

Posts live in blog/posts/<slug>.json, images in blog/img/<name>-{480,800,1536}.webp + -og.jpg.
build(SITE, I18N) writes dist/blog/... and returns (home_cards_html, sitemap_urls_xml).
Adding a post = drop a new JSON + images in, run build2.py, deploy.
"""
import json, os, re, glob, html, shutil, datetime

FORM = 'https://formsubmit.co/ajax/2b4ca41127912ca3bbac2accd0ee54b0'
INSIGHTS = 'https://bornaxahadi.github.io/thirdskin-insights/data.json'
GA = 'G-MZWRKFNXNN'
# styles queued for the next days (shown as "coming next" cards while there are fewer than 3 posts)
QUEUE = ['Scandinavian', 'Japandi', 'French Country', 'Mid-Century Modern', 'Art Deco', 'Wabi-Sabi', 'Mediterranean', 'Industrial', 'Bohemian', 'Classic', 'Minimalist', 'Moroccan']
esc = lambda s: html.escape(str(s), quote=True)
plain = lambda s: html.unescape(re.sub(r'<[^>]+>', '', s))


def load_posts():
    posts = []
    for f in glob.glob('blog/posts/*.json'):
        p = json.load(open(f))
        if p.get('draft'):
            continue
        words = ' '.join(x[1] if isinstance(x[1], str) else ' '.join(x[1]) for x in p['body'])
        p['words'] = len(plain(words).split())
        p['mins'] = max(2, round(p['words'] / 220))
        p['dt'] = datetime.date.fromisoformat(p['date'])
        p['nice'] = p['dt'].strftime('%-d %b %Y')
        posts.append(p)
    posts.sort(key=lambda p: (p['dt'], p['slug']), reverse=True)
    return posts


def srcset(base, name):
    return f'{base}{name}-480.webp 480w, {base}{name}-800.webp 800w, {base}{name}-1536.webp 1536w'


def card(p, base='/blog/', imgbase='/blog/img/', lazy=True, read='Read more'):
    return (f'<article class="jr-card"><a href="{base}{p["slug"]}/">'
            f'<figure><img src="{imgbase}{p["image"]}-800.webp" srcset="{srcset(imgbase, p["image"])}" sizes="(min-width:960px) 360px, (min-width:620px) 45vw, 88vw" '
            f'width="800" height="533" alt="{esc(p["imageAlt"])}" decoding="async"{" loading=\"lazy\"" if lazy else ""}><span class="jr-tag">{esc(p["style"])}</span></figure>'
            f'<div class="jr-body"><p class="jr-meta"><time datetime="{p["date"]}">{p["nice"]}</time> · {p["mins"]} min read</p>'
            f'<h3>{esc(p["title"])}</h3><p class="jr-ex">{esc(p["excerpt"])}</p><span class="jr-more">{read} <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-5-5 5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span></div></a></article>')


def soon_card(style):
    return (f'<article class="jr-card jr-soon" aria-label="Coming next: {esc(style)} style"><div><figure><span class="jr-tag">{esc(style)}</span><span class="jr-soon-ic">✦</span></figure>'
            f'<div class="jr-body"><p class="jr-meta">Coming next</p><h3>{esc(style)} interior style</h3><p class="jr-ex">A new style guide every day: where it comes from, what defines it, and how to use it at home.</p></div></div></article>')


# ---------------------------------------------------------------- shared page chrome
def fonts_css():
    keep = []
    for blk in re.findall(r'@font-face\{[^}]*\}', open('fonts/fonts.css').read()):
        if ("'Playfair Display'" in blk or "'Outfit'" in blk) and ('-latin.woff2' in blk):
            keep.append(blk.replace('url(fonts/', 'url(/fonts/'))
    return '\n'.join(keep)


CSS = r"""
:root{--cream:#F5EDE2;--linen:#E8D8C4;--paper:#FBF7F1;--ink:#2B1517;--muted:#76605A;--line:#D9C9B5;--wine:#561C24;--wine-2:#6D2932;--gold:#C9A464;--teal:#1C6E69;
--f-display:"Playfair Display",Didot,Georgia,serif;--f-body:"Outfit","Avenir Next","Segoe UI",system-ui,sans-serif;--max:1180px;--g:clamp(16px,4vw,48px)}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
body{margin:0;background:var(--cream);color:var(--ink);font:400 17px/1.75 var(--f-body)}
a{color:var(--wine)}img{max-width:100%;height:auto;display:block}
.wrap{max-width:var(--max);margin:0 auto;padding-inline:var(--g)}
.top{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--cream) 88%,transparent);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;height:64px;gap:16px}
.top img{height:34px;width:auto}
.top nav{display:flex;gap:22px;align-items:center;font-size:14px;letter-spacing:.04em}
.top nav a{text-decoration:none;color:var(--ink);white-space:nowrap}
.top nav a.cta{background:var(--wine);color:var(--paper);padding:9px 16px;border-radius:999px}
@media(max-width:640px){.top nav a.hide-s{display:none}}
@media(max-width:480px){.top nav .hide-xs{display:none}.top nav{gap:14px}.top img{height:30px}}
.prog{position:fixed;top:0;left:0;height:3px;width:0;background:linear-gradient(90deg,var(--wine),var(--gold));z-index:30}
.crumbs{font-size:13px;color:var(--muted);margin:26px 0 0}.crumbs a{color:var(--muted);text-decoration:none}.crumbs a:hover{color:var(--wine)}
.eyebrow{font:500 12px/1 var(--f-body);letter-spacing:.22em;text-transform:uppercase;color:var(--wine)}
h1,h2,h3{font-family:var(--f-display);font-weight:500;line-height:1.15;color:var(--ink)}
.post-head{max-width:820px;margin:28px auto 0;text-align:center}
.post-head h1{font-size:clamp(34px,5.2vw,58px);margin:14px 0 18px;letter-spacing:-.01em}
.post-head .dek{font-size:clamp(18px,1.8vw,21px);color:var(--muted);margin:0 auto 22px;max-width:62ch}
.byline{display:inline-flex;align-items:center;gap:12px;font-size:14px;color:var(--muted)}
.byline img{width:42px;height:42px;border-radius:50%;object-fit:cover;object-position:50% 20%}
.byline b{color:var(--ink);font-weight:500}
.hero-img{margin:34px auto 0;max-width:1180px;border-radius:22px;overflow:hidden;box-shadow:0 30px 60px -40px rgba(43,21,23,.6)}
.hero-img img{width:100%;aspect-ratio:3/2;object-fit:cover}
.cap{font-size:13px;color:var(--muted);text-align:center;margin:10px 0 0}
.layout{display:grid;gap:48px;max-width:1080px;margin:48px auto 0}
@media(min-width:1000px){.layout{grid-template-columns:220px minmax(0,1fr)}}
.toc{font-size:14px}.toc nav{position:sticky;top:90px}
.toc b{display:block;font:500 11px/1 var(--f-body);letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
.toc a{display:block;text-decoration:none;color:var(--ink);padding:6px 0 6px 12px;border-left:2px solid var(--line);line-height:1.35}
.toc a.on{border-color:var(--wine);color:var(--wine)}
@media(max-width:999px){.toc{display:none}}
.article{max-width:700px}
.article>p:first-of-type::first-letter{font-family:var(--f-display);float:left;font-size:4.2em;line-height:.8;margin:.08em .1em 0 0;color:var(--wine)}
.article h2{font-size:clamp(28px,3vw,36px);margin:52px 0 12px;scroll-margin-top:90px}
.article h3{font-size:23px;margin:34px 0 8px}
.article ul{padding-inline-start:0;list-style:none}.article li{position:relative;padding-inline-start:28px;margin:10px 0}
.article li::before{content:"";position:absolute;inset-inline-start:4px;top:.72em;width:9px;height:9px;border-radius:50%;background:var(--gold)}
.article figure{margin:36px 0}.article figure img{border-radius:18px;width:100%;aspect-ratio:3/2;object-fit:cover}
.article blockquote{margin:30px 0;padding:6px 0 6px 22px;border-left:3px solid var(--gold);font:italic 22px/1.5 var(--f-display);color:var(--wine)}
.box{background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:24px}
.faq{margin-top:56px}.faq details{border-bottom:1px solid var(--line);padding:14px 0}.faq summary{cursor:pointer;font:500 19px/1.35 var(--f-display);list-style:none;display:flex;justify-content:space-between;gap:12px}
.faq summary::after{content:"+";color:var(--wine);font-family:var(--f-body)}.faq details[open] summary::after{content:"–"}.faq details p{margin:10px 0 0;color:var(--muted)}
.refs{margin-top:40px;font-size:15px}.refs h2{font-size:24px;margin:0 0 10px}.refs a{word-break:break-word}
.share{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:40px 0 0;font-size:14px;color:var(--muted)}
.share a,.share button{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;padding:9px 14px;font:500 13px/1 var(--f-body);text-decoration:none;cursor:pointer}
.share a:hover,.share button:hover{border-color:var(--wine);color:var(--wine)}
.rate{margin-top:40px;text-align:center}.rate h2{font-size:26px;margin:0 0 6px}
.stars{display:inline-flex;gap:6px;margin:10px 0 6px;direction:ltr}
.stars button{background:none;border:0;padding:4px;cursor:pointer;font-size:34px;line-height:1;color:var(--line);transition:transform .15s,color .15s}
.stars button.on,.stars button.hov{color:var(--gold)}.stars button:hover{transform:scale(1.15)}
.rate small{display:block;color:var(--muted);font-size:14px}
.comments{margin-top:40px}.comments h2{font-size:26px;margin:0 0 4px}
.cm{border-top:1px solid var(--line);padding:16px 0}.cm .cm{margin-inline-start:22px;padding-bottom:4px}.cm .cm.fz b{color:var(--wine)}.cm-r{background:none;border:0;padding:6px 0 0;font:500 13px/1 var(--f-body);letter-spacing:.04em;color:var(--wine);cursor:pointer}.cm-r:hover{text-decoration:underline}.replying{display:flex;gap:10px;align-items:center;font-size:14px;color:var(--muted)}.replying[hidden]{display:none}.replying button{background:none;border:0;color:var(--wine);cursor:pointer;font:inherit;text-decoration:underline;padding:0}.cm b{font-weight:500}.cm time{color:var(--muted);font-size:13px;margin-inline-start:8px}.cm p{margin:6px 0 0}
.cform{display:grid;gap:12px;margin-top:18px}.cform .row2{display:grid;gap:12px}@media(min-width:620px){.cform .row2{grid-template-columns:1fr 1fr}}
.cform input,.cform textarea{width:100%;font:400 16px/1.5 var(--f-body);color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:12px 14px}
.cform input:focus,.cform textarea:focus{outline:2px solid color-mix(in srgb,var(--wine) 35%,transparent);border-color:var(--wine)}
.cform textarea{min-height:120px;resize:vertical}.cform .hp{position:absolute;left:-9999px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;padding:13px 24px;border-radius:999px;font:500 14px/1 var(--f-body);letter-spacing:.06em;text-decoration:none;border:1px solid var(--wine);cursor:pointer;background:transparent;color:var(--wine)}
.btn-solid{background:var(--wine);color:var(--paper)}
.note{font-size:13px;color:var(--muted)}
.ok{color:var(--teal);font-weight:500}
.author{display:flex;gap:18px;align-items:center;margin-top:48px}.author img{width:84px;height:84px;border-radius:50%;object-fit:cover;object-position:50% 20%;flex:none}
.author h3{margin:0 0 4px;font-size:20px}.author p{margin:0;font-size:15px;color:var(--muted)}
.cta-box{margin-top:40px;background:radial-gradient(120% 120% at 90% 0,#6D2932,#3a1016);color:var(--cream);border-radius:22px;padding:30px;text-align:center}
.cta-box h2{color:var(--cream);font-size:28px;margin:0 0 8px}.cta-box p{margin:0 0 18px;color:#E7D3C6}.cta-box .btn{background:var(--cream);color:var(--wine);border-color:var(--cream)}
.pn{display:grid;gap:12px;margin-top:40px}@media(min-width:620px){.pn{grid-template-columns:1fr 1fr}}
.pn a{text-decoration:none;color:var(--ink)}.pn small{display:block;color:var(--muted);font-size:12px;letter-spacing:.14em;text-transform:uppercase}.pn span{font-family:var(--f-display);font-size:18px}
.related{background:var(--linen);margin-top:72px;padding:64px 0}
.related h2,.arch h1{font-size:clamp(30px,4vw,44px);margin:0 0 26px}
/* cards (shared with homepage) */
.jr-grid{display:grid;gap:24px;grid-template-columns:1fr}
@media(min-width:620px){.jr-grid{grid-template-columns:repeat(2,1fr)}}@media(min-width:960px){.jr-grid{grid-template-columns:repeat(3,1fr)}}
.jr-card>a,.jr-card>div{display:flex;flex-direction:column;height:100%;text-decoration:none;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:22px;overflow:hidden;transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s}
.jr-card>a:hover{transform:translateY(-4px);box-shadow:0 26px 50px -32px rgba(86,28,36,.55)}
.jr-card figure{margin:0;position:relative;aspect-ratio:3/2;overflow:hidden;background:var(--linen)}
.jr-card figure img{width:100%;height:100%;object-fit:cover;transition:transform .8s cubic-bezier(.2,.7,.2,1)}.jr-card>a:hover figure img{transform:scale(1.05)}
.jr-tag{position:absolute;left:14px;top:14px;background:rgba(251,247,241,.92);color:var(--wine);font:500 11px/1 var(--f-body);letter-spacing:.16em;text-transform:uppercase;padding:7px 10px;border-radius:999px}
.jr-body{padding:20px 22px 22px;display:flex;flex-direction:column;flex:1}
.jr-meta{margin:0;font-size:12.5px;color:var(--muted);letter-spacing:.04em}
.jr-card h3{font-family:var(--f-display);font-weight:500;font-size:22px;line-height:1.25;margin:8px 0 8px}
.jr-ex{margin:0 0 16px;font-size:15px;line-height:1.6;color:var(--muted);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.jr-more{margin-top:auto;display:inline-flex;align-items:center;gap:8px;font:500 13px/1 var(--f-body);letter-spacing:.08em;text-transform:uppercase;color:var(--wine)}
.jr-more svg{width:18px;height:18px;transition:transform .25s}.jr-card>a:hover .jr-more svg{transform:translateX(4px)}
.jr-soon figure{display:grid;place-items:center;background:repeating-linear-gradient(135deg,var(--linen) 0 14px,#EFE3D3 14px 28px)}
.jr-soon-ic{font-size:40px;color:var(--gold)}.jr-soon h3{color:var(--muted)}
/* archive */
.arch{padding:40px 0 80px}.arch .lead{color:var(--muted);max-width:60ch;margin:0 0 26px}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 22px}.filters button{border:1px solid var(--line);background:var(--paper);border-radius:999px;padding:9px 14px;font:500 13px/1 var(--f-body);cursor:pointer;color:var(--ink)}
.filters button[aria-pressed="true"]{background:var(--wine);color:var(--paper);border-color:var(--wine)}
.search{width:100%;max-width:420px;font:400 16px/1.4 var(--f-body);padding:12px 16px;border:1px solid var(--line);border-radius:999px;background:var(--paper);margin-bottom:18px}
footer.bf{border-top:1px solid var(--line);padding:34px 0 46px;font-size:13px;color:var(--muted)}
footer.bf .wrap{display:flex;flex-wrap:wrap;gap:14px;justify-content:space-between;align-items:center}footer.bf a{color:var(--muted)}
footer.bf .credit{flex-basis:100%;text-align:center;margin:8px 0 0;padding-top:16px;border-top:1px solid var(--line);font-size:12px;letter-spacing:.06em}
footer.bf .credit b{color:var(--wine);font-weight:600}
@media (prefers-reduced-motion:reduce){*{transition:none!important;scroll-behavior:auto!important}}
"""

ANALYTICS = """<script>
window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}
function track(n,p){try{gtag('event',n,p||{})}catch(e){}}
(function(){var c=null;try{c=localStorage.getItem('tsi-consent')}catch(e){}
var tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}
var eu=/^(Europe|Atlantic\\/(Reykjavik|Canary|Madeira|Azores))/.test(tz);
if(c==='no'||(eu&&c!=='yes')||location.hostname!=='thirdskin.online')return;
gtag('js',new Date());gtag('config','GA_ID');
var go=function(){if(go.d)return;go.d=1;var s=document.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id=GA_ID';document.head.appendChild(s)};
['scroll','pointerdown','keydown'].forEach(function(e){addEventListener(e,go,{once:true,passive:true})});setTimeout(go,4000)})();
</script>""".replace('GA_ID', GA)


def head(title, desc, canonical, og_img, extra='', ld=None, keywords=''):
    return f'''<!doctype html>
<html lang="en" dir="ltr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{f'<meta name="keywords" content="{esc(keywords)}">' if keywords else ''}
<meta name="author" content="Farnaz Sadeghian">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="msvalidate.01" content="1018AD3EBC6FFB01FED16CB0AD633B59">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{canonical}"><link rel="alternate" hreflang="x-default" href="{canonical}">
<link rel="alternate" type="application/rss+xml" title="Style Journal by Farnaz Sadeghian" href="/blog/feed.xml">
<meta property="og:site_name" content="Third Skin Interiors"><meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="800">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{og_img}">
{extra}
<meta name="theme-color" content="#F5EDE2">
<link rel="icon" href="/img/icon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/img/icon-192.png">
<link rel="preload" href="/fonts/Outfit-n300-800-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>{FONTS}{CSS}</style>
{'<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(",", ":")) + '</script>' if ld else ''}
{ANALYTICS}
</head><body>'''


TOPBAR = '''<div class="prog" id="prog"></div>
<header class="top"><div class="wrap"><a href="/" aria-label="Third Skin Interiors home"><img src="/img/tsi-lockup.svg" alt="Third Skin Interiors by Farnaz Sadeghian" width="160" height="36"></a>
<nav aria-label="Main"><a href="/blog/"><span class="hide-xs">Style </span>Journal</a><a class="hide-s" href="/#about">About</a><a class="cta" href="/#contact">Book<span class="hide-xs"> a consultation</span></a></nav></div></header>'''

FOOTER = '''<footer class="bf"><div class="wrap"><span>© 2026 Third Skin Interiors by Farnaz Sadeghian · Dubai, UAE</span>
<span style="display:flex;gap:16px"><a href="/blog/">Style Journal</a><a href="https://www.instagram.com/decor.with.farnaz/" target="_blank" rel="noopener">Instagram</a><a href="/#contact">Contact</a><a href="/privacy/">Privacy</a><a href="/blog/feed.xml">RSS</a></span>
<p class="credit">Website designed &amp; developed by <b>Borna Ahadi</b></p></div></footer>'''

PUBLISHER = {'@type': 'Organization', '@id': 'https://thirdskin.online/#business', 'name': 'Third Skin Interiors', 'url': 'https://thirdskin.online/',
             'logo': {'@type': 'ImageObject', 'url': 'https://thirdskin.online/img/icon-512.png', 'width': 512, 'height': 512}}
AUTHOR = {'@type': 'Person', 'name': 'Farnaz Sadeghian', 'url': 'https://thirdskin.online/#about', 'jobTitle': 'Certified interior decorator',
          'sameAs': ['https://www.instagram.com/decor.with.farnaz/', 'https://www.facebook.com/817038121486364']}


def body_html(p, imgbase):
    out, toc = [], []
    for kind, val in p['body']:
        if kind == 'p':
            out.append(f'<p>{val}</p>')
        elif kind == 'h2':
            sid = re.sub(r'[^a-z0-9]+', '-', plain(val).lower()).strip('-')
            toc.append((sid, plain(val)))
            out.append(f'<h2 id="{sid}">{val}</h2>')
        elif kind == 'h3':
            out.append(f'<h3>{val}</h3>')
        elif kind == 'ul':
            out.append('<ul>' + ''.join(f'<li>{x}</li>' for x in val) + '</ul>')
        elif kind == 'quote':
            out.append(f'<blockquote>{val}</blockquote>')
        elif kind == 'img2' and p.get('image2'):
            out.append(f'<figure><img src="{imgbase}{p["image2"]}-800.webp" srcset="{srcset(imgbase, p["image2"])}" sizes="(min-width:760px) 700px, 92vw" width="1536" height="1024" alt="{esc(p["image2Alt"])}" loading="lazy" decoding="async"><figcaption class="cap">{esc(p.get("image2Cap", p["image2Alt"]))}</figcaption></figure>')
    return '\n'.join(out), toc


POST_JS = r"""<script>
(function(){
var slug=document.body.dataset.slug,$=function(s){return document.querySelector(s)};
// reading progress + table of contents highlight
var pr=$('#prog'),art=$('.article'),links=[].slice.call(document.querySelectorAll('.toc a'));
addEventListener('scroll',function(){var r=art.getBoundingClientRect(),h=r.height-innerHeight;pr.style.width=Math.max(0,Math.min(100,(-r.top)/(h>0?h:1)*100))+'%';
var cur=null;links.forEach(function(a){var t=document.getElementById(a.hash.slice(1));if(t&&t.getBoundingClientRect().top<140)cur=a});links.forEach(function(a){a.classList.toggle('on',a===cur)})},{passive:true});
// rating
var stars=[].slice.call(document.querySelectorAll('.stars button')),key='tsi-rate-'+slug,mine=0;try{mine=+localStorage.getItem(key)||0}catch(e){}
function paint(n,cls){stars.forEach(function(b,i){b.classList.toggle(cls,i<n)})}
paint(mine,'on');if(mine)$('#rateMsg').textContent='Thank you, you rated this '+mine+' / 5';
stars.forEach(function(b,i){b.onmouseenter=function(){paint(i+1,'hov')};b.onmouseleave=function(){paint(0,'hov')};
b.onclick=function(){if(mine)return;mine=i+1;try{localStorage.setItem(key,mine)}catch(e){}paint(mine,'on');track('blog_rating',{value:mine,post_slug:slug});$('#rateMsg').textContent='Thank you, you rated this '+mine+' / 5'}});
fetch('INSIGHTS',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(d){var x=((d.blog||{})[slug]);if(x&&x.count){$('#rateAvg').textContent='★ '+x.avg.toFixed(1)+' average from '+x.count+(x.count>1?' ratings':' rating')}}).catch(function(){});
// comment form (sent by email; the daily journal run publishes real comments and replies)
var rp=$('#replying');document.querySelectorAll('.cm-r').forEach(function(x){x.onclick=function(){var f=$('#cform');f.replyto.value=x.dataset.cid+' ('+x.dataset.name+')';$('#replyingTo').textContent='Replying to '+x.dataset.name;rp.hidden=false;f.querySelector('button[type=submit]').textContent='Post reply';f.scrollIntoView({behavior:'smooth',block:'center'});f.comment.focus({preventScroll:true})}});
var rc=$('#replyCancel');if(rc)rc.onclick=function(){var f=$('#cform');f.replyto.value='';rp.hidden=true;f.querySelector('button[type=submit]').textContent='Post comment'};
var f=$('#cform');if(f)f.onsubmit=function(e){e.preventDefault();if(f.company.value)return;var b=f.querySelector('button[type=submit]');b.disabled=true;b.textContent='Sending…';
fetch('FORM',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({_subject:'New blog comment: '+document.title,_template:'table',_captcha:'false',Article:location.href,'Reply to':f.replyto.value||'-',Name:f.name.value,Email:f.email.value,Comment:f.comment.value})})
.then(function(r){if(!r.ok)throw 0;var isR=!!f.replyto.value;f.innerHTML='<p class="ok">Thank you! Your '+(isR?'reply':'comment')+' was sent and will appear here within a day.</p>';track('blog_comment',{post_slug:slug,reply:isR})})
.catch(function(){b.disabled=false;b.textContent=f.replyto.value?'Post reply':'Post comment';$('#cErr').textContent='Sorry, it could not be sent. Please try again or message us on WhatsApp.'})};
// share
var cp=$('#copyLink');if(cp)cp.onclick=function(){(navigator.clipboard?navigator.clipboard.writeText(location.href):Promise.reject()).then(function(){cp.textContent='Link copied'}).catch(function(){prompt('Copy this link',location.href)})};
document.querySelectorAll('.share a').forEach(function(a){a.addEventListener('click',function(){track('share',{method:a.dataset.m,content_type:'article',item_id:slug})})});
if(navigator.share){var ns=$('#nativeShare');ns.hidden=false;ns.onclick=function(){navigator.share({title:document.title,url:location.href}).catch(function(){})}}
})();
</script>""".replace('INSIGHTS', INSIGHTS).replace('FORM', FORM)


def post_page(p, posts, SITE):
    url = f'{SITE}blog/{p["slug"]}/'
    imgbase = '/blog/img/'
    og = f'{SITE}blog/img/{p["image"]}-og.jpg'
    body, toc = body_html(p, imgbase)
    idx = posts.index(p)
    newer = posts[idx - 1] if idx > 0 else None
    older = posts[idx + 1] if idx + 1 < len(posts) else None
    tags = set(p.get('tags', []))
    rel = sorted([q for q in posts if q is not p], key=lambda q: (-len(tags & set(q.get('tags', []))), -q['dt'].toordinal()))[:3]
    rel_html = ''.join(card(q) for q in rel) + ''.join(soon_card(s) for s in [s for s in QUEUE if s not in {q['style'] for q in posts}][:3 - len(rel)])
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'BlogPosting', '@id': url + '#article', 'headline': p['title'], 'description': p['metaDesc'], 'url': url, 'mainEntityOfPage': url,
         'image': [f'{SITE}blog/img/{p["image"]}-1536.webp', og] + ([f'{SITE}blog/img/{p["image2"]}-1536.webp'] if p.get('image2') else []),
         'datePublished': p['date'], 'dateModified': p.get('updated', p['date']), 'author': AUTHOR, 'publisher': PUBLISHER,
         'articleSection': 'Interior styles', 'keywords': p['keywords'], 'wordCount': p['words'], 'inLanguage': 'en',
         'isPartOf': {'@type': 'Blog', '@id': SITE + 'blog/#blog', 'name': 'Style Journal'}, 'about': {'@type': 'Thing', 'name': p['style'] + ' interior design'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE},
            {'@type': 'ListItem', 'position': 2, 'name': 'Style Journal', 'item': SITE + 'blog/'},
            {'@type': 'ListItem', 'position': 3, 'name': p['title'], 'item': url}]}]
        + ([{'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': f['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in p['faq']]}] if p.get('faq') else [])}
    extra = (f'<meta property="og:type" content="article"><meta property="article:published_time" content="{p["date"]}T08:00:00+04:00">'
             f'<meta property="article:modified_time" content="{p.get("updated", p["date"])}T08:00:00+04:00"><meta property="article:author" content="Farnaz Sadeghian">'
             f'<meta property="article:section" content="Interior styles">' + ''.join(f'<meta property="article:tag" content="{esc(t)}">' for t in p.get('tags', []))
             + f'<link rel="preload" as="image" href="{imgbase}{p["image"]}-800.webp" imagesrcset="{srcset(imgbase, p["image"])}" imagesizes="(min-width:1200px) 1180px, 100vw">')
    comments = p.get('comments', [])
    fz = lambda c: f'<div class="cm fz"><b>Farnaz</b><p>{esc(c["reply"])}</p></div>' if c.get('reply') else ''
    def one(c, cid):
        subs = ''.join(f'<div class="cm"><b>{esc(r["name"])}</b><time datetime="{r["date"]}">{r["date"]}</time><p>{esc(r["text"])}</p>{fz(r)}</div>' for r in c.get('replies', []))
        return (f'<div class="cm" id="{cid}"><b>{esc(c["name"])}</b><time datetime="{c["date"]}">{c["date"]}</time><p>{esc(c["text"])}</p>{fz(c)}{subs}'
                f'<button type="button" class="cm-r" data-cid="{cid}" data-name="{esc(c["name"])}">Reply</button></div>')
    cm_html = ''.join(one(c, f'c{i}') for i, c in enumerate(comments, 1))
    n_comments = len(comments) + sum(len(c.get('replies', [])) for c in comments)
    enc = lambda s: re.sub(r'[^A-Za-z0-9._~-]', lambda m: ''.join('%%%02X' % b for b in m.group(0).encode()), s)
    faq = ('<section class="faq" aria-labelledby="faqh"><h2 id="faqh">Questions about ' + esc(p['style']) + ' style</h2>'
           + ''.join(f'<details{" open" if i == 0 else ""}><summary>{esc(f["q"])}</summary><p>{esc(f["a"])}</p></details>' for i, f in enumerate(p['faq'])) + '</section>') if p.get('faq') else ''
    refs = ('<section class="refs box"><h2>Further reading</h2><ul>' + ''.join(f'<li><a href="{esc(r["u"])}" target="_blank" rel="noopener">{esc(r["t"])}</a></li>' for r in p['related_links']) + '</ul></section>') if p.get('related_links') else ''
    return head(f'{p["seoTitle"]} | Third Skin Interiors', p['metaDesc'], url, og, extra, ld, p['keywords']).replace('<body>', f'<body data-slug="{p["slug"]}">') + TOPBAR + f'''
<main>
<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/blog/">Style Journal</a> › <span>{esc(p["style"])} style</span></nav>
<header class="post-head">
<p class="eyebrow">{esc(p["style"])} style · Style Journal</p>
<h1>{esc(p["title"])}</h1>
<p class="dek">{esc(p["excerpt"])}</p>
<p class="byline"><img src="/img/farnaz-portrait.jpg" alt="Farnaz Sadeghian" width="42" height="42"><span>By <b>Farnaz Sadeghian</b>, certified interior decorator · <time datetime="{p["date"]}">{p["nice"]}</time> · {p["mins"]} min read</span></p>
</header>
<figure class="hero-img"><img src="{imgbase}{p["image"]}-800.webp" srcset="{srcset(imgbase, p["image"])}" sizes="(min-width:1200px) 1180px, 100vw" width="1536" height="1024" alt="{esc(p["imageAlt"])}" fetchpriority="high" decoding="async"></figure>
<div class="layout">
<aside class="toc"><nav aria-label="In this article"><b>In this article</b>{''.join(f'<a href="#{i}">{esc(t)}</a>' for i, t in toc)}</nav></aside>
<div>
<article class="article">
{body}
</article>
{faq}
{refs}
<div class="share" aria-label="Share this article"><span>Share:</span>
<a data-m="whatsapp" href="https://wa.me/?text={enc(p["title"] + " " + url)}" target="_blank" rel="noopener">WhatsApp</a>
<a data-m="pinterest" href="https://pinterest.com/pin/create/button/?url={enc(url)}&media={enc(og)}&description={enc(p["title"])}" target="_blank" rel="noopener">Pinterest</a>
<a data-m="facebook" href="https://www.facebook.com/sharer/sharer.php?u={enc(url)}" target="_blank" rel="noopener">Facebook</a>
<a data-m="x" href="https://x.com/intent/post?url={enc(url)}&text={enc(p["title"])}" target="_blank" rel="noopener">X</a>
<button type="button" id="copyLink">Copy link</button><button type="button" id="nativeShare" hidden>More…</button></div>
<section class="rate box" aria-labelledby="rateh"><h2 id="rateh">Did you enjoy this article?</h2><small id="rateAvg">Be the first to rate it</small>
<div class="stars" role="group" aria-label="Rate this article from 1 to 5">{''.join(f'<button type="button" aria-label="{i} star{"s" if i > 1 else ""}">★</button>' for i in range(1, 6))}</div><small id="rateMsg">Tap a star to rate</small></section>
<section class="comments" aria-labelledby="cmh"><h2 id="cmh">Comments{f" ({n_comments})" if comments else ""}</h2>
{cm_html or '<p class="note">No comments yet. Be the first to share your thoughts or ask Farnaz a question.</p>'}
<form class="cform" id="cform" novalidate><p class="replying" id="replying" hidden><span id="replyingTo"></span><button type="button" id="replyCancel">Cancel</button></p><input type="hidden" name="replyto" value=""><div class="row2"><input name="name" required maxlength="60" placeholder="Your name" autocomplete="name" aria-label="Your name"><input name="email" type="email" required placeholder="Email (not published)" autocomplete="email" aria-label="Email, not published"></div>
<textarea name="comment" required maxlength="2000" placeholder="Your comment or question…" aria-label="Your comment"></textarea><input class="hp" name="company" tabindex="-1" autocomplete="off" aria-hidden="true">
<div><button class="btn btn-solid" type="submit">Post comment</button></div><p class="note">Comments and replies appear here within a day. Your email is never shown. <a href="/privacy/">Privacy policy</a>.</p><p class="note" id="cErr" role="alert"></p></form></section>
<div class="author box"><img src="/img/farnaz-portrait.jpg" alt="Farnaz Sadeghian" width="84" height="84" loading="lazy"><div><h3>Farnaz Sadeghian</h3><p>Certified interior decorator (TAFE, Australia) based in Dubai, founder of Third Skin Interiors and creator of Decor with Farnaz, followed by about 390,000 people. Author of the upcoming book <em>Soul of the Room</em>.</p></div></div>
<div class="cta-box"><h2>Want this look in your home?</h2><p>Book an interior design consultation in Dubai or online.</p><a class="btn" href="/#contact">Book a consultation</a></div>
<nav class="pn" aria-label="More articles">{f'<a class="box" href="/blog/{older["slug"]}/" rel="prev"><small>← Previous</small><span>{esc(older["title"])}</span></a>' if older else '<span></span>'}{f'<a class="box" href="/blog/{newer["slug"]}/" rel="next" style="text-align:right"><small>Next →</small><span>{esc(newer["title"])}</span></a>' if newer else ''}</nav>
</div></div></div>
<section class="related" aria-labelledby="relh"><div class="wrap"><h2 id="relh">Related styles</h2><div class="jr-grid">{rel_html}</div>
<p style="text-align:center;margin:30px 0 0"><a class="btn" href="/blog/">All articles</a></p></div></section>
</main>
{FOOTER}
{POST_JS}
</body></html>
'''


def archive_page(posts, SITE):
    url = SITE + 'blog/'
    styles = sorted({p['style'] for p in posts})
    items = ''.join(card(p, lazy=i > 2).replace('<article class="jr-card">', f'<article class="jr-card" data-style="{esc(p["style"])}" data-q="{esc((p["title"] + " " + p["excerpt"] + " " + " ".join(p.get("tags", []))).lower())}">') for i, p in enumerate(posts))
    items += ''.join(soon_card(s) for s in [s for s in QUEUE if s not in styles][:max(0, 3 - len(posts))])
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Blog', '@id': url + '#blog', 'name': 'Style Journal by Farnaz Sadeghian', 'url': url, 'description': 'A new interior style every day, explained by Dubai interior decorator Farnaz Sadeghian.',
         'publisher': PUBLISHER, 'author': AUTHOR, 'inLanguage': 'en',
         'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'], 'url': f'{SITE}blog/{p["slug"]}/', 'datePublished': p['date'], 'image': f'{SITE}blog/img/{p["image"]}-og.jpg'} for p in posts[:20]]},
        {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}, {'@type': 'ListItem', 'position': 2, 'name': 'Style Journal', 'item': url}]}]}
    og = f'{SITE}blog/img/{posts[0]["image"]}-og.jpg' if posts else SITE + 'img/og-image.jpg'
    return head('Style Journal: Interior Design Styles Explained | Farnaz Sadeghian', 'A new interior style every day: Persian, Scandinavian, Japandi, French and more, explained with ideas for real homes by Dubai interior decorator Farnaz Sadeghian.', url, og, '<meta property="og:type" content="website">', ld,
                'interior design styles, home decor styles, interior style guide, Dubai interior decorator blog') + TOPBAR + f'''
<main class="arch"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <span>Style Journal</span></nav>
<p class="eyebrow" style="margin-top:26px">Style Journal</p>
<h1>Interior styles, <em>one a day</em></h1>
<p class="lead">Every day Farnaz Sadeghian, a certified interior decorator in Dubai, explains one interior style: where it comes from, what defines it, and how to bring it into a real home.</p>
<input class="search" id="q" type="search" placeholder="Search articles…" aria-label="Search articles">
<div class="filters" id="filters"><button type="button" aria-pressed="true" data-s="">All</button>{''.join(f'<button type="button" aria-pressed="false" data-s="{esc(s)}">{esc(s)}</button>' for s in styles)}</div>
<div class="jr-grid" id="grid">{items}</div>
<p class="note" id="none" hidden>No articles match your search yet.</p>
</div></main>
{FOOTER}
<script>(function(){{var s='',q='',cards=[].slice.call(document.querySelectorAll('#grid .jr-card[data-style]'));
function f(){{var n=0;cards.forEach(function(c){{var ok=(!s||c.dataset.style===s)&&(!q||c.dataset.q.indexOf(q)>-1);c.hidden=!ok;if(ok)n++}});document.getElementById('none').hidden=n>0;document.querySelectorAll('.jr-soon').forEach(function(c){{c.hidden=!!(s||q)}})}}
document.getElementById('filters').onclick=function(e){{var b=e.target.closest('button');if(!b)return;s=b.dataset.s;this.querySelectorAll('button').forEach(function(x){{x.setAttribute('aria-pressed',x===b)}});f()}};
document.getElementById('q').oninput=function(){{q=this.value.trim().toLowerCase();f()}}}})();</script>
</body></html>
'''


def rss(posts, SITE):
    items = ''.join(f'''<item><title>{esc(p["title"])}</title><link>{SITE}blog/{p["slug"]}/</link><guid isPermaLink="true">{SITE}blog/{p["slug"]}/</guid>
<pubDate>{p["dt"].strftime("%a, %d %b %Y")} 08:00:00 +0400</pubDate><dc:creator>Farnaz Sadeghian</dc:creator><category>{esc(p["style"])}</category>
<description>{esc(p["excerpt"])}</description><enclosure url="{SITE}blog/img/{p["image"]}-og.jpg" type="image/jpeg" length="0"/></item>''' for p in posts[:30])
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom"><channel>
<title>Style Journal by Farnaz Sadeghian</title><link>{SITE}blog/</link><atom:link href="{SITE}blog/feed.xml" rel="self" type="application/rss+xml"/>
<description>A new interior style every day, by Dubai interior decorator Farnaz Sadeghian.</description><language>en</language>{items}
</channel></rss>
'''


def build(SITE, I18N=None):
    global FONTS
    FONTS = fonts_css()
    posts = load_posts()
    shutil.rmtree('dist/blog', ignore_errors=True)
    os.makedirs('dist/blog/img', exist_ok=True)
    for f in glob.glob('blog/img/*'):
        shutil.copy(f, 'dist/blog/img/')
    for p in posts:
        os.makedirs(f'dist/blog/{p["slug"]}', exist_ok=True)
        open(f'dist/blog/{p["slug"]}/index.html', 'w').write(post_page(p, posts, SITE))
    open('dist/blog/index.html', 'w').write(archive_page(posts, SITE))
    open('dist/blog/feed.xml', 'w').write(rss(posts, SITE))
    # homepage cards: latest 3 (+ "coming next" placeholders while there are fewer than 3)
    home = ''.join(card(p, base='blog/', imgbase='blog/img/', read='@@READ@@') for p in posts[:3])
    home += ''.join(soon_card(s) for s in [s for s in QUEUE if s not in {p['style'] for p in posts}][:max(0, 3 - len(posts))])
    sm = f'\n  <url><loc>{SITE}blog/</loc><lastmod>{posts[0]["date"] if posts else ""}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>'
    for p in posts:
        sm += (f'\n  <url><loc>{SITE}blog/{p["slug"]}/</loc><lastmod>{p.get("updated", p["date"])}</lastmod><priority>0.7</priority>'
               f'\n    <image:image><image:loc>{SITE}blog/img/{p["image"]}-1536.webp</image:loc><image:title>{esc(p["imageAlt"])}</image:title></image:image>'
               + (f'\n    <image:image><image:loc>{SITE}blog/img/{p["image2"]}-1536.webp</image:loc><image:title>{esc(p["image2Alt"])}</image:title></image:image>' if p.get('image2') else '')
               + '\n  </url>')
    print(f'blog: {len(posts)} posts')
    return home, sm, posts
