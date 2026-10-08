# Setup status (owner: update this file when a step is done)

The agent can only report what it can see. Each tool below needs a one-time
setup by the owner. Tick the box when done and add any IDs.

## 1. Google Search Console  [x] done (6 Oct 2026)
- URL-prefix property https://thirdskin.online/ verified with google963066ade0abd581.html (keep that file forever).
- sitemap.xml submitted; indexing requested for the homepage.
- Each week (owner): Performance -> Export -> save CSV into seo/data/ (no personal data).
- Bing Webmaster Tools: [x] verified (msvalidate.01 meta + BingSiteAuth.xml, keep both), sitemap submitted 6 Oct 2026. Also feeds ChatGPT search / Copilot.
- Google Analytics <-> Search Console: [x] linked 6 Oct 2026.
- IndexNow: [x] key file 1498d818f79a545bad7ebe2081055ab2.txt is live; all URLs submitted 6 Oct 2026 (Bing, Yandex accepted).

## 2. Visitor analytics  [x] done (6 Oct 2026)
- Tool chosen: Google Analytics 4   Property: "Third Skin Interiors - thirdskin.online" (557594788)   Measurement ID: G-MZWRKFNXNN
- Loads after the first scroll/tap or 5 s (no speed cost). Google Consent Mode v2: Europe-timezone visitors see a small Accept/Decline banner; others are measured without ad cookies.
- Events: generate_lead (inquiry sent), sign_up (book list), whatsapp_click, instagram_click, facebook_click, media_kit_download, email_click, language_switch.
- Microsoft Clarity (heatmaps/recordings): [x] project yteq8bnfw0 (CONFIG.clarityId), consent-aware.
- Export a weekly CSV into seo/data/ (or share dashboard numbers).

## 3. Email list  [~] working, upgrade optional
- Now: the "Join the launch list" form on every language page collects name + email with a REQUIRED consent checkbox
  (records "opted in on <date> (<language>)") and a link to the privacy page https://thirdskin.online/privacy/.
  Sign-ups arrive in Farnaz's inbox through FormSubmit (same service as the inquiry form). FormSubmit must be
  activated for thirdskin.online once (click "Activate Form" in its email). GA4 event: sign_up.
- Upgrade later (owner signs up once, free): MailerLite or Brevo for a real newsletter with unsubscribe links.
  When a form/endpoint URL exists, write it here; the agent then points the launch form at it.
- Service chosen: FormSubmit (interim)   Form URL: https://formsubmit.co/ajax/2b4ca41127912ca3bbac2accd0ee54b0
- Privacy page: [x] https://thirdskin.online/privacy/ (English; source in _src/build2.py, PRIVACY)
- Lead-magnet idea: free PDF, e.g. "5 mistakes that make a room look smaller" or a chapter of "Soul of the Room".

## 4. Google Business Profile  [~] created, NOT verified yet
- Created 6 Oct 2026: "Third Skin Interiors", category Interior designer, service-area business (Dubai, UAE), phone +971 52 123 5012, website https://thirdskin.online/.
- Owner must finish verification at business.google.com (private mailing address, then phone/video check by Google). Until verified it does not show on Maps.
- After verification: add photos, opening hours, services, and ask happy clients for honest reviews.

## 5. Auto-publish  [x] ON
The agent commits and pushes directly to main every day without asking.
To stop it: delete the daily routine, or tell Claude "pause the SEO agent".

## 6. Live follower counts (Instagram + Facebook)
Two things keep the numbers on the site current:
- A daily Claude routine (10:20 Dubai) reads the public Instagram count through
  vidIQ (5 vidIQ credits a day) and runs `.github/scripts/followers.py --ig <count> --source vidiq`.
  This works today without any Meta setup.
- The "Live follower counts" GitHub Action runs every 6 hours. Instagram and
  Facebook block GitHub's servers from public pages most of the time, so it
  only becomes reliable (and Facebook only updates at all) once the Meta token below is added.
Between checks the counter grows by the real measured daily growth
(seo/data/followers-readings.csv), so it keeps moving.
For exact numbers on both platforms use Meta's official API (free):
1. Instagram must be a Business/Creator account linked to the Facebook page.
2. developers.facebook.com -> create an app -> get a long-lived access token
   with instagram_basic + pages_read_engagement.
3. In GitHub: repo Settings -> Secrets and variables -> Actions -> add
   META_ACCESS_TOKEN, IG_USER_ID (Instagram business account id),
   FB_PAGE_ID (817038121486364).
The Action uses the API automatically once those secrets exist.
