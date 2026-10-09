"""Production build: one fast, pre-translated page per language + SEO files.
   python3 build2.py   ->  dist/ (GitHub Pages)  and  artifact.html (claude.ai preview)
"""
import json, re, os, shutil, subprocess, html, datetime

SITE = 'https://thirdskin.online/'
LANGS = ['en', 'fa', 'ar', 'ru', 'es', 'it', 'zh', 'ja', 'de', 'fr']
OG_LOCALE = {'en': 'en_US', 'fa': 'fa_IR', 'ar': 'ar_AE', 'ru': 'ru_RU', 'es': 'es_ES', 'it': 'it_IT', 'zh': 'zh_CN', 'ja': 'ja_JP', 'de': 'de_DE', 'fr': 'fr_FR'}
CACHE = 'tsi-v39'
TODAY = datetime.date.today().isoformat()

# ---------- sources ----------
head = open('head.part').read()
body = open('body.part').read()
import blog
BLOG_HOME, BLOG_SM, BLOG_POSTS = blog.build(SITE)
body = body.replace('@@BLOGCARDS@@', BLOG_HOME)
app = open('app.part').read().replace('SCENES_HERE', open('scenes.part').read())
i18n_src = open('i18n.js').read()
subprocess.run(['node', '-e', """
const vm=require('vm'),fs=require('fs');const c={};vm.createContext(c);
vm.runInContext(fs.readFileSync('i18n.js','utf8')+';this.I18N=I18N',c);
fs.writeFileSync('/tmp/i18n.json',JSON.stringify(c.I18N));"""], check=True)
I18N = json.load(open('/tmp/i18n.json'))
cfg = re.search(r'whatsapp: "(\d+)".*?email: "([^"]+)"', app, re.S)
PHONE, EMAIL = '+' + cfg.group(1), cfg.group(2)

def t(lang, k):
    return I18N.get(lang, {}).get(k) or I18N['en'].get(k) or ''

def plain(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

# ---------- pre-render translations into the HTML ----------
VOID = {'img', 'input', 'br', 'hr', 'meta', 'link', 'source'}
def prerender(src, lang):
    out = src
    # attribute translations
    for attr, target in (('data-i18n-ph', 'placeholder'), ('data-i18n-alt', 'alt'), ('data-i18n-aria', 'aria-label')):
        def rep(m):
            tag = m.group(0); key = re.search(attr + r'="([^"]+)"', tag).group(1)
            val = html.escape(plain(t(lang, key)), quote=True)
            if re.search(r'\s' + target + r'="', tag):
                return re.sub(r'(\s' + target + r'=")[^"]*(")', lambda mm: mm.group(1) + val + mm.group(2), tag, count=1)
            return tag.replace(' ' + attr, f' {target}="{val}" {attr}', 1)
        out = re.sub(r'<[a-zA-Z][^>]*\s' + attr + r'="[^"]+"[^>]*>', rep, out)
    # element content translations (process from the end so offsets stay valid)
    hits = [m for m in re.finditer(r'<([a-zA-Z][a-zA-Z0-9]*)\b[^>]*\sdata-i18n="([^"]+)"[^>]*>', out)]
    for m in reversed(hits):
        name, key = m.group(1).lower(), m.group(2)
        if name in VOID: continue
        start = m.end(); depth = 1; pos = start
        tagre = re.compile(r'<(/?)' + name + r'\b[^>]*?(/?)>', re.I)
        while depth:
            mm = tagre.search(out, pos)
            if not mm: break
            if mm.group(1): depth -= 1
            elif not mm.group(2): depth += 1
            pos = mm.end()
        if depth: continue
        close_start = mm.start()
        out = out[:start] + t(lang, key) + out[close_start:]
    return out

# ---------- structured data ----------
def jsonld(lang):
    url = SITE if lang == 'en' else SITE + lang + '/'
    person = {
        '@type': 'Person', '@id': SITE + '#farnaz', 'name': 'Farnaz Sadeghian',
        'alternateName': ['Decor with Farnaz', 'فرناز صادقیان'],
        'jobTitle': 'Interior Decorator and Interior Designer',
        'description': 'Certified interior decorator in Dubai (TAFE Australia), home stager and decor educator with about 390,000 followers on Instagram and Facebook.',
        'image': SITE + 'img/farnaz-hero.webp', 'url': SITE,
        'worksFor': {'@id': SITE + '#business'},
        'homeLocation': {'@type': 'Place', 'name': 'Dubai, United Arab Emirates'},
        'hasCredential': {'@type': 'EducationalOccupationalCredential', 'credentialCategory': 'Certificate', 'name': 'Interior Decoration', 'recognizedBy': {'@type': 'Organization', 'name': 'TAFE (Australia)'}},
        'knowsAbout': ['Interior design', 'Interior decoration', 'Home staging', '3D interior design', 'Space planning', 'Lighting design', 'Colour schemes', 'Japandi', 'Wabi-sabi', 'Mid-century modern', 'Art Deco', 'Persian carpets'],
        'knowsLanguage': ['en', 'fa'],
        'sameAs': ['https://www.instagram.com/decor.with.farnaz/', 'https://www.facebook.com/817038121486364', 'https://www.instagram.com/decor_farnaz/'],
    }
    services = [('Interior design consultation', 's1d'), ('3D interior design and visualisation', 's2d'), ('Full interior design projects', 's3d'),
                ('Home staging', None), ('Sponsored reels for home brands', 'o1d'), ('Brand ambassador partnerships', 'o2d'), ('Showroom and launch visits', 'o3d')]
    business = {
        '@type': ['ProfessionalService', 'LocalBusiness'], '@id': SITE + '#business',
        'name': 'Third Skin Interiors', 'alternateName': 'Third Skin Interiors by Farnaz Sadeghian',
        'description': 'Interior design studio of Farnaz Sadeghian in Dubai: interior design consultations, 3D design and visualisation, full interior projects and home staging for apartments, villas and show homes, plus content partnerships for home brands.',
        'url': SITE, 'logo': SITE + 'img/icon-512.png', 'image': [SITE + 'img/og-image.jpg', SITE + 'img/farnaz-carpet.webp'],
        'telephone': PHONE, 'email': EMAIL, 'founder': {'@id': SITE + '#farnaz'},
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Dubai', 'addressRegion': 'Dubai', 'addressCountry': 'AE'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': 25.2048, 'longitude': 55.2708},
        'areaServed': [{'@type': 'City', 'name': 'Dubai'}, {'@type': 'Country', 'name': 'United Arab Emirates'}],
        'knowsLanguage': ['en', 'fa'],
        'sameAs': person['sameAs'],
        'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Interior design services in Dubai', 'itemListElement': [
            {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n, 'areaServed': 'Dubai, UAE', 'provider': {'@id': SITE + '#business'},
                                                 **({'description': plain(t('en', d))} if d else {})}} for n, d in services]},
    }
    book = {'@type': 'Book', '@id': SITE + '#book', 'name': 'Soul of the Room', 'alternativeHeadline': 'A Journey Through Interior Styles',
            'author': {'@id': SITE + '#farnaz'}, 'inLanguage': 'en', 'genre': 'Interior design', 'image': SITE + 'img/book-closed.webp',
            'description': plain(t('en', 'bookP2')), 'about': ['Interior styles', 'Japandi', 'Art Deco', 'Home decoration']}
    website = {'@type': 'WebSite', '@id': SITE + '#website', 'url': SITE, 'name': 'Third Skin Interiors', 'publisher': {'@id': SITE + '#business'}, 'inLanguage': LANGS}
    page = {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': plain(t(lang, 'metaTitle')), 'description': plain(t(lang, 'metaDesc')),
            'inLanguage': lang, 'isPartOf': {'@id': SITE + '#website'}, 'about': {'@id': SITE + '#business'}, 'primaryImageOfPage': SITE + 'img/og-image.jpg', 'dateModified': TODAY}
    faq = {'@type': 'FAQPage', '@id': url + '#faq', 'inLanguage': lang, 'mainEntity': [
        {'@type': 'Question', 'name': plain(t(lang, f'q{i}')), 'acceptedAnswer': {'@type': 'Answer', 'text': plain(t(lang, f'a{i}'))}} for i in range(1, 7)]}
    return json.dumps({'@context': 'https://schema.org', '@graph': [website, page, business, person, book, faq]}, ensure_ascii=False, separators=(',', ':'))

def headmeta(lang, prefix):
    url = SITE if lang == 'en' else SITE + lang + '/'
    title, desc = html.escape(plain(t(lang, 'metaTitle'))), html.escape(plain(t(lang, 'metaDesc')))
    alts = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{SITE if l == "en" else SITE + l + "/"}">' for l in LANGS)
    ogalts = '\n'.join(f'<meta property="og:locale:alternate" content="{OG_LOCALE[l]}">' for l in LANGS if l != lang)
    geo = ("<script>(function(){try{if(location.hash||localStorage.getItem('dwf-lang'))return;"
           "if(Intl.DateTimeFormat().resolvedOptions().timeZone==='Asia/Tehran')location.replace('fa/'+location.search)}catch(e){}})()</script>\n") if lang == 'en' else ''
    return geo + f'''<meta name="msvalidate.01" content="1018AD3EBC6FFB01FED16CB0AD633B59">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Farnaz Sadeghian">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="keywords" content="{html.escape(plain(t(lang, 'metaKeywords')))}">
<meta name="geo.region" content="AE-DU"><meta name="geo.placename" content="Dubai">
<link rel="canonical" href="{url}">
{alts}
<link rel="alternate" hreflang="x-default" href="{SITE}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Third Skin Interiors">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}img/og-image.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Farnaz Sadeghian, interior designer in Dubai, Third Skin Interiors">
<meta property="og:locale" content="{OG_LOCALE[lang]}">
{ogalts}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}img/og-image.jpg">
<link rel="manifest" href="{prefix}manifest.webmanifest">
<link rel="icon" href="{prefix}img/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefix}img/icon-192.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<link rel="alternate" type="text/plain" href="{prefix}llms.txt" title="Summary for AI assistants">
<script type="application/ld+json">{jsonld(lang)}</script>'''

# ---------- minify ----------
def esbuild(code, loader):
    r = subprocess.run(['esbuild', '--minify', f'--loader={loader}', '--target=es2020', '--log-level=error'], input=code.encode(), capture_output=True, check=True)
    return r.stdout.decode()
def minify_head(h):
    return re.sub(r'<style>(.*?)</style>', lambda m: '<style>' + esbuild(m.group(1), 'css').strip() + '</style>', h, flags=re.S)
def minify_html(s):
    s = re.sub(r'<!--(?!HEADMETA).*?-->', '', s, flags=re.S)
    return re.sub(r'>\s*\n\s*<', '>\n<', s)

FACES = []
for blk in re.findall(r'@font-face\{([^}]*)\}', open('fonts/fonts.css').read()):
    g = lambda k: (re.search(k + r':\s*([^;]+);', blk) or [None, None])[1]
    url = re.search(r'url\(([^)]+)\)', blk).group(1)
    FACES.append({'f': g('font-family').strip("'\""), 's': 'url(' + url + ')', 'st': g('font-style'), 'w': g('font-weight'), 'u': g('unicode-range'), 'sub': url.rsplit('-', 1)[1].replace('.woff2', '')})
def font_loader(lang):
    subs = {'latin'} | ({'cyrillic'} if lang == 'ru' else set()) | ({'arabic'} if lang in ('fa', 'ar') else set()) | ({'latin-ext'} if lang in ('de', 'fr', 'es', 'it') else set())
    fams = None if lang in ('fa', 'ar') else lambda f: f['f'] != 'Vazirmatn'
    faces = [f for f in FACES if f['sub'] in subs and (fams is None or fams(f))]
    data = json.dumps([[f['f'], f['s'], f['st'], f['w'], f['u']] for f in faces], separators=(',', ':'))
    # all fonts are fetched after the page has loaded and switched on together, so the page lays out only once more
    return ('<script>(function(){var F=' + data + ';function go(){if(!window.FontFace)return;Promise.all(F.map(function(a){return new FontFace(a[0],a[1],{style:a[2],weight:a[3],unicodeRange:a[4],display:"swap"}).load().catch(function(){return null})})).then(function(l){l.forEach(function(f){f&&document.fonts.add(f)});try{sessionStorage.setItem("tsi-f","1")}catch(e){}})}'
            'var seen=0;try{seen=sessionStorage.getItem("tsi-f")}catch(e){}var later=function(){requestAnimationFrame(function(){setTimeout(go,80)})};if(seen)go();else if(document.readyState==="complete")later();else addEventListener("load",later,{once:true})})()</script>')
head_min = minify_head(head)
body_min = minify_html(body)
sw_reg = "\nif('serviceWorker'in navigator&&location.protocol==='https:'){addEventListener('load',()=>navigator.serviceWorker.register('ROOTsw.js').catch(()=>{}))}"

def i18n_for(lang):
    sub = {'en': I18N['en']}
    for l in LANGS:
        if l != 'en': sub[l] = I18N[l] if l == lang else {'_name': I18N[l]['_name'], '_dir': I18N[l]['_dir']}
    return 'var I18N=' + json.dumps(sub, ensure_ascii=False, separators=(',', ':')) + ';'

def relink(s, prefix):
    if not prefix: return s
    s = re.sub(r'''(["'(])(img|fonts)/''', r'\1' + prefix + r'\2/', s)
    s = s.replace('href="media-kit.pdf"', 'href="' + prefix + 'media-kit.pdf"')
    s = s.replace('href="privacy/"', 'href="' + prefix + 'privacy/"')
    s = re.sub(r'''(["' ])blog/''', r'\1' + prefix + 'blog/', s)
    return s

os.makedirs('dist', exist_ok=True)
import hashlib
APP_JS = esbuild(app, 'js') + sw_reg.replace("'ROOTsw.js'", "(document.documentElement.dataset.pageLang==='en'?'':'../')+'sw.js'")
APPV = hashlib.md5(APP_JS.encode()).hexdigest()[:8]
open('dist/app.js', 'w').write(APP_JS)
for lang in LANGS:
    prefix = '' if lang == 'en' else '../'
    d = I18N[lang]['_dir']
    js = esbuild(i18n_for(lang), 'js').strip()
    page = ('<!doctype html>\n<html lang="' + lang + '" dir="' + d + '" data-page-lang="' + lang + '">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">\n'
            + head_min.replace('<!--HEADMETA-->', headmeta(lang, prefix)).replace('<!--FONTS-->', font_loader(lang)) + '</head>\n<body>\n'
            + prerender(body_min, lang) + '\n<script>' + js + '</script>\n<script>(function(){var go=function(){var s=document.createElement("script");s.src="' + prefix + 'app.js?v=' + APPV + '";document.body.appendChild(s)};var later=function(){requestAnimationFrame(function(){setTimeout(go,60)})};if(document.readyState==="complete")later();else addEventListener("load",later,{once:true})})()</script>\n</body>\n</html>\n')
    page = relink(page.replace('@@READ@@', t(lang, 'blogRead')), prefix)
    out = 'dist/index.html' if lang == 'en' else f'dist/{lang}/index.html'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(page)
    print(f'{out:24s} {len(page)//1024} KB')

# ---------- preview copy for claude.ai (single page, switches language in place) ----------
art_head = head.replace('<!--HEADMETA-->', '<title>Third Skin Interiors</title>\n<script>document.documentElement.dataset.noRoute="1"</script>').replace('<!--FONTS-->', '<style>' + open('fonts/fonts.css').read() + '</style>')
open('artifact.html', 'w').write(art_head + body + '\n<script>\n' + i18n_src + '\n' + app + '\n</script>\n')

# ---------- assets: only what pages use ----------
used = set()
for root, _, files in os.walk('dist'):
    for f in files:
        if f.endswith('.html'):
            used |= set(re.findall(r'img/([A-Za-z0-9._-]+)', open(os.path.join(root, f)).read()))
used |= {'icon-192.png', 'icon-512.png', 'icon.svg', 'og-image.jpg'}
used |= {f'ba-{r}-{s}.webp' for r in ['bedroom', 'dining', 'entry', 'kids', 'kitchen', 'living'] for s in ['before', 'after']}
shutil.rmtree('dist/img', ignore_errors=True); os.makedirs('dist/img')
for f in sorted(used):
    src = 'img/' + f if os.path.exists('img/' + f) else 'img-src/' + f
    if os.path.exists(src): shutil.copy(src, 'dist/img/' + f)
    elif not os.path.exists('blog/img/' + f): print('missing image', f)
shutil.rmtree('dist/fonts', ignore_errors=True); shutil.copytree('fonts', 'dist/fonts', ignore=shutil.ignore_patterns('*.css'))

# ---------- manifest, service worker ----------
json.dump({'name': 'Third Skin Interiors', 'short_name': 'Third Skin', 'description': 'Third Skin Interiors by Farnaz Sadeghian, certified interior decorator in Dubai.',
           'start_url': './', 'scope': './', 'display': 'standalone', 'background_color': '#F5EDE2', 'theme_color': '#561C24', 'lang': 'en',
           'icons': [{'src': 'img/icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'img/icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'}]},
          open('dist/manifest.webmanifest', 'w'), indent=1)
open('dist/sw.js', 'w').write(f"""const CACHE='{CACHE}';
self.addEventListener('install',e=>{{self.skipWaiting()}});
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{{
  const r=e.request,u=new URL(r.url);
  if(r.method!=='GET'||u.origin!==location.origin)return;
  if(/\\/(img|fonts)\\//.test(u.pathname)){{   // images & fonts: instant from cache, refreshed in the background
    e.respondWith(caches.open(CACHE).then(c=>c.match(r).then(hit=>{{const net=fetch(r).then(res=>{{if(res.ok)c.put(r,res.clone());return res}}).catch(()=>hit);return hit||net}})));return;
  }}
  e.respondWith(fetch(r,{{cache:'no-cache'}}).then(res=>{{const copy=res.clone();caches.open(CACHE).then(c=>c.put(r,copy));return res}}).catch(()=>caches.match(r)));   // pages: always fresh, cache only for offline
}});
""")

# ---------- sitemap, robots, llms.txt ----------
SITEMAP_IMGS = [('farnaz-cut.webp', 'altHeroImg'), ('farnaz-carpet.webp', None), ('ba-living-after.webp', 'altBaA_living'), ('ba-bedroom-after.webp', 'altBaA_bedroom'),
    ('ba-kitchen-after.webp', 'altBaA_kitchen'), ('ba-dining-after.webp', 'altBaA_dining'), ('ba-entry-after.webp', 'altBaA_entry'), ('ba-kids-after.webp', 'altBaA_kids'),
    ('feed-wallart.webp', 'altF_wallart'), ('feed-corner.webp', 'altF_corner'), ('feed-bathroom.webp', 'altF_bathroom'), ('book-open.webp', None)]
def img_entries(l):
    out = ''
    for f, k in SITEMAP_IMGS:
        if not os.path.exists('dist/img/' + f): continue
        out += f'\n    <image:image><image:loc>{SITE}img/{f}</image:loc></image:image>'
    return out
def alt_links():
    return ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE if l == "en" else SITE + l + "/"}"/>' for l in LANGS) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}"/>'
urls = ''.join(f'''
  <url>
    <loc>{SITE if l == "en" else SITE + l + "/"}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if l == "en" else "0.8"}</priority>{alt_links()}
    <image:image><image:loc>{SITE}img/og-image.jpg</image:loc></image:image>{img_entries(l)}
  </url>''' for l in LANGS)
urls += f'''
  <url>
    <loc>{SITE}privacy/</loc>
    <lastmod>2026-10-06</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>'''
open('dist/sitemap.xml', 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">{urls}{BLOG_SM}\n</urlset>\n')
open('dist/robots.txt', 'w').write(f"""# Everyone is welcome, search engines and AI assistants alike
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bingbot
Allow: /

Sitemap: {SITE}sitemap.xml
""")
journal_list = '\n'.join(f"- [{p['title']}]({SITE}blog/{p['slug']}/): {p['excerpt']}" for p in BLOG_POSTS[:30])
faq_en = '\n'.join(f"### {plain(t('en', f'q{i}'))}\n{plain(t('en', f'a{i}'))}\n" for i in range(1, 7))
open('dist/llms.txt', 'w').write(f"""# Third Skin Interiors · Farnaz Sadeghian

> Farnaz Sadeghian is a certified interior decorator (TAFE, Australia) and interior designer based in Dubai, UAE. Through her studio Third Skin Interiors she offers interior design consultations, 3D design and visualisation, full interior projects and home staging for apartments, villas and show homes in Dubai and across the UAE. As "Decor with Farnaz" she teaches practical home styling to about 390,000 followers on Instagram and Facebook, and she is the author of the upcoming book "Soul of the Room: A Journey Through Interior Styles" (50 interior styles).

## Key facts
- Name: Farnaz Sadeghian (Persian: فرناز صادقیان)
- Business: Third Skin Interiors (social media name: Decor with Farnaz)
- Location: Dubai, United Arab Emirates; works in person in Dubai/UAE and online
- Credentials: certified interior decorator through TAFE, Australia; six years of professional practice; 50+ homes staged, each planned in 3D first
- Audience: about 323,000 Instagram followers (@decor.with.farnaz) and 70,000 Facebook followers; roughly 31% Iran and Central Asia, 28% UAE, 25% United States, 10% Europe
- Reach: about 36 million people reached in a month; most-watched reel 9.5 million views
- Languages: English and Persian (website available in 10 languages)
- Contact: WhatsApp {PHONE}, email {EMAIL}, Instagram collaborations @decor_farnaz

## Services for homeowners
- Interior design consultation (in person in Dubai or online): layout, colour, lighting and what to buy, with a written plan
- 3D interior design and visualisation: see the room in realistic 3D before buying
- Full interior projects: design, sourcing, styling and staging for apartments, villas and show homes

## Services for brands
- Sponsored reels (Instagram and Facebook), brand ambassadorships, showroom and launch visits, product edits, real estate and developer content

## Book
- Soul of the Room: A Journey Through Interior Styles, by Farnaz Sadeghian (coming soon). 50 interior styles from Japandi to Art Deco: origins, defining features and how to bring each into a real home.

## FAQ
{faq_en}
## Pages
- [English]({SITE})
- [فارسی]({SITE}fa/)
- [العربية]({SITE}ar/)
- [Русский]({SITE}ru/)
- [Español]({SITE}es/)
- [Italiano]({SITE}it/)
- [中文]({SITE}zh/)
- [日本語]({SITE}ja/)
- [Deutsch]({SITE}de/)
- [Français]({SITE}fr/)

## Style Journal
- [Style Journal: a new interior style guide by Farnaz every day]({SITE}blog/)
- [RSS feed]({SITE}blog/feed.xml)
{journal_list}
""")
open('dist/.nojekyll', 'w').write('')
print('done', len(used), 'images')
open('dist/CNAME','w').write('thirdskin.online\n')
open('dist/google963066ade0abd581.html','w').write('google-site-verification: google963066ade0abd581.html')
open('dist/1498d818f79a545bad7ebe2081055ab2.txt','w').write('1498d818f79a545bad7ebe2081055ab2')

# ---------- privacy page (English) ----------
PRIVACY = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Privacy policy | Third Skin Interiors</title>
<meta name="description" content="How thirdskin.online (Farnaz Sadeghian, Third Skin Interiors, Dubai) handles contact messages, email sign-ups, analytics and cookies.">
<link rel="canonical" href="https://thirdskin.online/privacy/"><meta name="robots" content="index, follow">
<link rel="icon" href="../img/icon.svg" type="image/svg+xml">
<style>
:root{--cream:#F5EDE2;--ink:#2B1517;--muted:#6B5A57;--wine:#6D2932;--line:#E3D5C6}
body{margin:0;background:var(--cream);color:var(--ink);font:400 17px/1.7 "Avenir Next","Segoe UI",system-ui,sans-serif}
main{max-width:720px;margin:0 auto;padding:48px 20px 80px}
a{color:var(--wine)} h1{font:500 40px/1.15 Georgia,serif;margin:0 0 6px} h2{font:500 22px/1.3 Georgia,serif;margin:34px 0 8px}
.meta{color:var(--muted);font-size:14px;margin-bottom:28px} .back{display:inline-block;margin-bottom:28px;text-decoration:none;font-size:14px}
ul{padding-inline-start:22px} li{margin:4px 0}
</style></head><body><main>
<a class="back" href="../">&larr; thirdskin.online</a>
<h1>Privacy policy</h1>
<p class="meta">Third Skin Interiors by Farnaz Sadeghian · Dubai, UAE · Last updated 6 October 2026</p>
<p>This page explains what information this website collects, why, and what you can do about it. We keep it simple: we only collect what we need to answer you and to understand how the site is used. We never sell your data.</p>
<h2>Who we are</h2>
<p>This website is run by Farnaz Sadeghian (Third Skin Interiors, Decor with Farnaz), Dubai, United Arab Emirates. Contact: <a href="mailto:decorwithfarnaz@gmail.com">decorwithfarnaz@gmail.com</a>.</p>
<h2>Messages you send us</h2>
<p>When you use the inquiry form, we receive your name, email and message, and the company and phone number if you add them. The form is delivered to our email inbox by the FormSubmit service. We use these details only to reply to you and to work on your request. If the form cannot be sent, the site lets you send the same text by WhatsApp or copy it; WhatsApp is run by Meta under its own privacy policy.</p>
<h2>Book launch list</h2>
<p>If you join the <em>Soul of the Room</em> launch list, we receive your name and email, and we record that you ticked the consent box and when. We use it only to tell you about the book and Farnaz's news. Every email lets you unsubscribe, or you can write to us and we will remove you.</p>
<h2>Journal comments</h2>
<p>If you comment on an article in our Style Journal, we receive your name, email and comment by email through FormSubmit. Comments are checked before they appear. Only your first name, the date and your comment are published, with our reply; your email is never shown or published. To have a comment removed, write to us.</p>
<h2>Analytics and cookies</h2>
<ul>
<li><b>Google Analytics 4</b> helps us see how many people visit, from which countries, and which parts of the site they use (for example page views, clicks on WhatsApp or the media kit, and forms sent). It uses cookies. We do not use advertising or ad-personalisation cookies.</li>
<li>Visitors in Europe are asked first: analytics cookies are only used if you press <b>Accept</b>. You can change your choice by clearing this site's data in your browser.</li>
<li>We may also use <b>Microsoft Clarity</b> to see anonymous heatmaps of where people tap and scroll, under the same consent rules.</li>
<li>The site stores small settings in your browser (your language choice and your cookie choice). These are not shared with anyone.</li>
</ul>
<h2>Hosting</h2>
<p>The site is hosted on GitHub Pages, which may keep technical logs (such as IP addresses) for security, under GitHub's privacy statement.</p>
<h2>Your choices</h2>
<p>You can ask us what information we hold about you, ask us to correct or delete it, or unsubscribe at any time by emailing <a href="mailto:decorwithfarnaz@gmail.com">decorwithfarnaz@gmail.com</a>.</p>
</main></body></html>
'''
os.makedirs('dist/privacy', exist_ok=True)
open('dist/privacy/index.html', 'w').write(PRIVACY)

open('dist/BingSiteAuth.xml','w').write('<?xml version="1.0"?>\n<users>\n\t<user>1018AD3EBC6FFB01FED16CB0AD633B59</user>\n</users>')
