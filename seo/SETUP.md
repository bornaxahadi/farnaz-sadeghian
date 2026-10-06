# Setup status (owner: update this file when a step is done)

The agent can only report what it can see. Each tool below needs a one-time
setup by the owner. Tick the box when done and add any IDs.

## 1. Google Search Console  [ ] not done
Shows which searches bring people, and your ranking.
1. https://search.google.com/search-console -> Add property -> Domain
   -> thirdskin.online (verify via a DNS TXT record at your domain provider).
2. Submit https://thirdskin.online/sitemap.xml
3. Each week: Performance -> Export -> save CSV into seo/data/ (no personal data).
Also do Bing Webmaster Tools (can import from Search Console).

## 2. Visitor analytics  [ ] not done
Pick ONE. Recommended: Plausible or Cloudflare Web Analytics (simple, no
cookie banner needed). Or Google Analytics 4 (free, needs cookie consent for
EU visitors).
- Tool chosen: ________   Site ID: ________
- Agent will ask your approval before adding the script to all 10 pages.
- Export a weekly CSV into seo/data/ (or share dashboard numbers).

## 3. Email list  [ ] not done
Recommended: Brevo, MailerLite or Buttondown (free tiers, hosted form
endpoint, handle unsubscribe + legal). The existing contact form
(formEndpoint in index.html) is NOT a newsletter list.
- Service chosen: ________   Form URL: ________
- Signup form must include: consent checkbox, privacy link, all 10 languages
- A privacy page is needed (what you collect, why, how to unsubscribe).
  Visitors from the EU (GDPR) and UAE (PDPL) are covered by this.
- Idea for more signups: free PDF, e.g. "5 mistakes that make a room look
  smaller" or a chapter of "Soul of the Room".

## 4. Google Business Profile  [ ] not done
Biggest local-SEO win for "interior designer Dubai". Same name, phone, city
as the website.

## 5. Auto-merge  [ ] OFF
Default: the agent opens a pull request daily and the owner merges it.
Change to ON only if you trust it to publish safe fixes automatically.
