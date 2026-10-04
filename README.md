# Third Skin Interiors — website (by Farnaz Sadeghian)

One-page responsive site in 9 languages (EN default, FA, AR, ES, IT, ZH, JA, DE, FR), installable as a web app.

## Before going live
Open `index.html`, find `const CONFIG` and set:
- `whatsapp` / `whatsappDisplay` — already set to +971 52 123 5012
- `email` — set to decorwithfarnaz@gmail.com (change later to a domain email)
- `formEndpoint` (optional) — a free Formspree form URL so inquiries also arrive by email
- `stats` — update follower numbers from the dashboards now and then; the live counter projects from them

## Publish free on GitHub Pages
1. Create a new public repository, e.g. `thirdskininteriors`.
2. Upload everything in this folder (keep the `img` folder).
3. Settings → Pages → Source: "Deploy from a branch", Branch: `main`, folder `/ (root)` → Save.
4. The site goes live at `https://<username>.github.io/decorwithfarnaz/` within a minute or two.
5. Later, add a custom domain in Settings → Pages → Custom domain.

Language: chosen automatically from the visitor's browser language, then their region (time zone). Visitors can switch with the flag menu; links like `…/#fa` open a specific language.
