# Site source (do not edit the generated files directly)

The live site (index.html, the 10 language folders, app.js, sitemap.xml, robots.txt,
llms.txt, sw.js, manifest) is GENERATED from this folder by `build2.py`.
If you hand-edit index.html only, the next build overwrites it.

| File | What it is |
|---|---|
| head.part | `<head>` CSS (and placeholders for meta + fonts) |
| body.part | page markup; visible text uses `data-i18n` keys |
| app.part | all JavaScript (CONFIG at the top: WhatsApp, form, stats, gaId, clarityId) |
| scenes.part | inline SVG scenes |
| i18n.js | every text in 10 languages (`I18N.en`, `I18N.fa` …). SEO meta (metaTitle, metaDesc, metaKeywords) and image alt texts are near the end |
| seo_alts.py | generator for the alt-text / meta block in i18n.js |
| build2.py | builds everything into dist/ (SITE = https://thirdskin.online/) |
| fonts.css | @font-face list used by the font loader |

Build: `npm i -g esbuild` once, then `bash _src/build.sh` from the repo root.
Then commit `_src/` and the regenerated files together.
