# Setup status (owner: update this file when a step is done)

The agent can only report what it can see. Each tool below needs a one-time
setup by the owner. Tick the box when done and add any IDs.

## 1. Google Search Console  [x] done (6 Oct 2026)
- URL-prefix property https://thirdskin.online/ verified with google963066ade0abd581.html (keep that file forever).
- sitemap.xml submitted; indexing requested for the homepage.
- Each week (owner): Performance -> Export -> save CSV into seo/data/ (no personal data).
- Bing Webmaster Tools: [ ] owner must sign in once at bing.com/webmasters, then import from Search Console.
- IndexNow: [x] key file 1498d818f79a545bad7ebe2081055ab2.txt is live; all URLs submitted 6 Oct 2026 (Bing, Yandex accepted).

## 2. Visitor analytics  [x] done (6 Oct 2026)
- Tool chosen: Google Analytics 4   Property: "Third Skin Interiors - thirdskin.online" (557594788)   Measurement ID: G-MZWRKFNXNN
- Loads after the first scroll/tap or 5 s (no speed cost). Google Consent Mode v2: Europe-timezone visitors see a small Accept/Decline banner; others are measured without ad cookies.
- Events: generate_lead (inquiry sent), sign_up (book list), whatsapp_click, instagram_click, facebook_click, media_kit_download, email_click, language_switch.
- Microsoft Clarity (heatmaps): [ ] owner must sign in once at clarity.microsoft.com; then put the project id in _src/app.part CONFIG.clarityId and rebuild.
- Export a weekly CSV into seo/data/ (or share dashboard numbers).

## 3. Email list  [ ] not done
Recommended: Brevo, MailerLite or Buttondown (free tiers, hosted form
endpoint, handle unsubscribe + legal). The existing contact form
(formEndpoint in index.html) is NOT a newsletter list.
- Service chosen: ________   Form URL: ________
- Signup form must include: consent checkbox, privacy link, English page
- A privacy page is needed (what you collect, why, how to unsubscribe).
  Visitors from the EU (GDPR) and UAE (PDPL) are covered by this.
- Idea for more signups: free PDF, e.g. "5 mistakes that make a room look
  smaller" or a chapter of "Soul of the Room".

## 4. Google Business Profile  [ ] not done
Biggest local-SEO win for "interior designer Dubai". Same name, phone, city
as the website.

## 5. Auto-publish  [x] ON
The agent commits and pushes directly to main every day without asking.
To stop it: delete the daily routine, or tell Claude "pause the SEO agent".
