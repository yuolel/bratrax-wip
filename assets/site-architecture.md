# Bratrax Site Architecture

**Last updated:** August 11, 2026
**Owner:** Yuliya
**Status:** Post-launch (Bratrax Lite launched June 2026 via the $1-trial offer; founding window closed, now invite-only)

This document captures the agreed site architecture for bratrax.com, the URL conventions for comparison pages, and the rules for when standalone About and FAQ pages are worth building versus keeping their content on the landing page.

---

## Table of contents

- [Domain strategy](#domain-strategy)
- [Proposed site architecture](#proposed-site-architecture)
- [URL conventions](#url-conventions)
- [Comparison pages: /vs/ and /alternatives/](#comparison-pages)
- [Changelog / product updates](#changelog)
- [Integrations: hub and per-tool pages](#integrations)
- [FAQ: landing page section vs separate page](#faq-guidelines)
- [About: landing page section vs separate page](#about-guidelines)
- [Internal linking strategy](#internal-linking)
- [Launch-day checklist](#launch-checklist)
- [Future: Bratrax Clear Vision](#clear-vision)

---

<a id="domain-strategy"></a>
## Domain strategy

**Decision: consolidate everything on `bratrax.com`. No subdomain for marketing.**

The earlier `bratrax.com` → `light.bratrax.com` redirect goes away on launch. The Bratrax Lite landing page lives at `bratrax.com/`. All marketing content — comparison pages, blog, about, FAQ — lives on the same domain.

### Why one domain, not a subdomain split

Google treats subdomains as separate sites for ranking purposes. SEO authority built on one does not automatically pass to the other. Splitting marketing across `bratrax.com` and `lite.bratrax.com` would have meant building authority twice and losing the reinforcing effect of every backlink, citation, and newsletter mention compounding into the same domain.

Bratrax Clear Vision, when it eventually launches, will be a custom-built consultative product — not a SaaS with comparison-friendly positioning. It does not need an umbrella domain to support it. A `/clear-vision` section or a single "talk to us about a custom build" page is sufficient.

### Where the app lives

If a separate subdomain is needed for the actual product interface (post-signup), use `app.bratrax.com`. This is the conventional split: marketing on the root domain, app on a subdomain. Do not use `lite.bratrax.com` for the app — the product name "Bratrax Lite" lives at the root, and the subdomain naming should match its function (`app`), not its product tier.

### Launch-day SEO consolidation

The launch-day work that actually consolidates SEO is:

1. Stop the `bratrax.com` → `lite.bratrax.com` redirect; instead serve the waitlist/product content directly at `bratrax.com/`.
2. Add `301 redirects` going the opposite direction: `lite.bratrax.com/*` → `bratrax.com/*` (or → `bratrax.com/` for the root). This passes any link equity already accumulated on `lite.bratrax.com` to the new home.
3. Update all canonicals to `https://bratrax.com/`.
4. Update `og:url` to match.
5. Update the sitemap to list `bratrax.com/` only.

Verify `bratrax.com` in Google Search Console as a property after the cutover so you can monitor indexation, submit the sitemap, and watch for crawl errors.

---

<a id="proposed-site-architecture"></a>
## Proposed site architecture

```
bratrax.com/                            # Bratrax Lite landing page (homepage)
├── /vs/triple-whale                    # Comparison page (rename from current file)
├── /vs/hyros                           # Comparison page (rename from current file)
├── /vs/northbeam                       # Next priority — major incumbent
├── /vs/polar                           # Next priority — closest architectural analog (also ships MCP)
├── /vs/thoughtmetric                   # Next priority — closest philosophical analog (BYOK AI)
├── /vs/                                # Comparison hub (BUILD ONCE 5+ children exist; see comparison-pages section)
├── /alternatives/triple-whale          # "Best Triple Whale alternatives" — multi-tool roundup (later)
├── /alternatives/hyros
├── /alternatives/northbeam
├── /blog/                              # The Dashboard newsletter archive
│   ├── /blog/attribution-is-arithmetic
│   └── /blog/[other newsletter pieces]
├── /changelog                          # LIVE — product-updates feed (editorialized from the prod digest)
│   └── /changelog/[release]            # Notable release — own URL when rank-worthy
├── /integrations                       # Integrations hub — all connectors
│   └── /integrations/[tool]            # shopify, woocommerce, meta, google-ads, tiktok, bing,
│                                       #   taboola, outbrain, klaviyo, bloomreach, claude, slack
├── /slack                              # LIVE — Slack Marketplace landing page; 301s to
│                                       #   /integrations/slack once the hub ships
├── /clear-vision                       # Single page, "talk to us" CTA — when ready
├── /pricing                            # Planned — dedicated page (see note)
└── /faq                                # LIVE — built; triggers were met

(future)
app.bratrax.com/                        # Product interface, post-signup — only if technically needed
```

### Notes on each section

**Homepage (`/`).** The Bratrax Lite product page itself. Hero, pricing in the H1, MCP/BYOK explanation, proof band (Inceptly $950M+, VidTao 100K+ marketers), feature band, "How we compare" section linking to `/vs/X` pages, FAQ section (with `FAQPage` schema), small About credibility band, primary CTA. This is the conversion-tuned page.

**`/vs/[competitor]`.** Individual comparison pages. Each page targets a specific "bratrax vs [competitor]" search query and lives as a child of the homepage in the IA. These pages cross-link to each other and link up to the homepage's "How we compare" section.

**`/vs/` (hub).** Defer building until 5+ comparison pages exist. See [Comparison pages](#comparison-pages) for what goes on it.

**`/alternatives/[competitor]`.** Different intent than `/vs/`: targets "best [competitor] alternatives" queries. Builds for users who don't know Bratrax yet but are leaving a specific incumbent. Build later, after the `/vs/` set is established.

**`/blog/`.** The Dashboard newsletter archive. Each piece is a child of `/blog/`. No category sub-routes at launch; add only if the archive becomes large enough to warrant browsing by topic.

**`/clear-vision`.** Single page when ready. Brief positioning, "for brands at $20M+ GMV" qualifier, "talk to us" CTA. Probably builds 3-6 months post-launch.

**`/pricing`.** Planned as a dedicated page. The June position was that $99 flat is simple enough to live on the homepage; that has since been overtaken — a standalone page is wanted, and the guidance below on avoiding duplication with the homepage's pricing section still applies. Live price is **$99/mo** (the $79 founding rate is closed; earlier drafts of this doc said "$79/$99").

**`/faq`.** **Built and live.** The June guidance was to defer it; the triggers were met. Keep the homepage FAQ section and `/faq` differentiated per [FAQ guidelines](#faq-guidelines) — the homepage carries conversion questions, `/faq` carries the comprehensive set.

**`/slack`.** Live. Built as the Installation landing page required by the Slack Marketplace submission. Moves to `/integrations/slack` with a 301 once the hub ships — see [Integrations](#integrations).

---

<a id="url-conventions"></a>
## URL conventions

| Pattern | Use case | Example |
|---|---|---|
| `/vs/[slug]` | 1-vs-1 comparison pages | `/vs/triple-whale` |
| `/alternatives/[slug]` | Multi-tool alternative roundups | `/alternatives/triple-whale` |
| `/blog/[slug]` | Newsletter pieces and articles | `/blog/attribution-is-arithmetic` |
| `/changelog/[slug]` | Individual product-update entries | `/changelog/commerce-profile-graph` |
| `/integrations/[slug]` | Per-connector integration pages | `/integrations/klaviyo` |
| `/[single-word]` | Top-level marketing pages | `/pricing`, `/about`, `/faq` |
| `/[multi-word-with-hyphens]` | Top-level marketing pages | `/clear-vision`, `/free-trial` |

### Slugging rules

- Lowercase always. `/About` redirects to `/about`.
- Hyphens, never underscores. `/clear-vision` not `/clear_vision`.
- No dates in URLs. `/blog/seo-guide` not `/blog/2026/05/seo-guide`.
- No product tier in slugs. `/vs/triple-whale` not `/bratrax-lite-vs-triple-whale`. The brand is implicit on `bratrax.com`; product tier is a position the page can shift on without a URL change.
- No trailing slash on leaf pages. Pick one policy site-wide and enforce with redirects.
- Short and descriptive. The URL is brand surface area — treat it like H1 territory.

### Why `/vs/[competitor]` over `/bratrax-lite-vs-[competitor]`

Three reasons:

1. **Search query match.** People search "bratrax vs triple whale," not "bratrax lite vs triple whale." The URL should target the actual high-volume query.
2. **Future-proofing.** When Clear Vision launches, the same URL can host the canonical Bratrax-vs-X comparison without a migration.
3. **Industry norm.** Linear, Notion, Asana, Stripe, Webflow all use `/vs/` or `/compare/`. Following the pattern means competitor research tools cluster the pages correctly and AI search engines parse them more reliably.

---

<a id="comparison-pages"></a>
## Comparison pages: /vs/ and /alternatives/

These are two different page types serving two different searcher intents. Build both, but at different times.

### `/vs/[competitor]` — head-to-head comparison

For someone who already knows Bratrax and is comparing it to a specific competitor. Direct, structured, opinionated. Already drafted: `/vs/triple-whale` and `/vs/hyros`. Next priority: Northbeam, Polar, ThoughtMetric, Wicked Reports.

### `/alternatives/[competitor]` — multi-tool roundup

For someone leaving a specific incumbent who doesn't yet know Bratrax. Targets "best [competitor] alternatives" queries. Format: a roundup of 5-8 alternatives with Bratrax positioned first, brief comparison of each, links to the relevant `/vs/[competitor]` page for the full head-to-head. Build these 60-90 days after launch, once the `/vs/` set has expanded.

### When to build the `/vs/` hub page

A `/vs/` hub page is a real piece of content, not a router or directory listing. It should rank for category-level queries like `bratrax alternatives`, `attribution tool comparison`, `best attribution software`. It is worth building only when there is enough underneath it to make it substantive.

**Build trigger:** 5+ individual `/vs/X` pages published.

**Until then:** the homepage's "How we compare" section serves as the lightweight hub. Each `/vs/X` page cross-links to the others in a sidebar or end-of-page block.

**What goes on the `/vs/` hub when built:**
- 200-300 word intro framing the category and Bratrax's positioning
- Master comparison table: rows = Bratrax + every competitor, columns = pricing model, contract terms, AI architecture, target buyer, key weakness
- Card per `/vs/X` page with one-sentence takeaway and link in
- "Anti-positioning" section: who Bratrax is *not* for (filters bad-fit traffic, builds trust)
- Pricing-at-a-glance band
- Aggregated FAQ pulling from the most-asked questions across individual pages
- Schema: `CollectionPage` plus `BreadcrumbList`

**What does NOT go on the hub:**
- Just a list of links (this is a router, not a hub — Google penalizes thin content)
- Duplicate copy from individual `/vs/X` pages (creates internal cannibalization)

---

<a id="changelog"></a>
## Changelog / product updates: `/changelog`

A reverse-chronological feed of what's shipped to production, written for customers and prospects — not developers. Fed from the existing weekly production digest, but through an editorial pass, never raw.

> **Implementation brief:** the full rubric, entry template, digest→entry transform prompt, weekly process, and build checklist live in `changelog-implementation-brief.md` (delegation-ready).

### Placement & URLs
- **`/changelog`** — the index/feed. Industry norm (Linear, Stripe, Notion), so AI search and competitor-research tools parse it correctly.
- **`/changelog/[slug]`** — an individual entry for any *notable* release (e.g. `/changelog/commerce-profile-graph`), giving a meaningful feature its own rankable, linkable URL. Minor/bundled changes stay inline on the index; only releases worth ranking for get their own page.

### The pipeline (digest → entry)
The weekly production digest is the **raw input**, not the output:
1. Weekly digest of what merged to production (already running).
2. **Editorial pass** — translate dev changes into customer-benefit entries: *what shipped, who it's for, why it matters.* An LLM can draft from the digest; a human approves. Never pipe commit messages straight to the page.
3. Publish to `/changelog`; promote notable items to their own `/changelog/[slug]`.

**Cadence:** match the digest (weekly, or as releases warrant). Skip empty weeks rather than pad.

### Entry format
- Benefit-framed title ("Trace any order end to end," not "Add order-drilldown view"), date, and a New / Improved / Fixed tag.
- 1–3 short paragraphs: what it is, why you'd care, how to use it. Optional screenshot/GIF.
- Link out to the relevant `/integrations/[tool]` or dashboard where useful.

### Why it earns a place
- **Freshness + rankings** — regular publishing lifts crawl frequency; entries rank for "Bratrax [feature]" / "what's new in Bratrax" and feed AI-search answers.
- **Retention asset** — the natural source for the dormant re-engagement email and the founding-onboarding "we build what early customers ask for" line; those emails link *to* it.
- **Sales proof** — a public, fast-moving changelog signals momentum to prospects.

### Schema
Index: `CollectionPage`. Individual entries: `Article` / `TechArticle` with `datePublished`.

---

<a id="integrations"></a>
## Integrations: `/integrations` hub + `/integrations/[tool]` spokes

Hub-and-spoke programmatic SEO — the same playbook as `/vs/`, applied to connectors. Explains how each supported integration works so customers and prospects see the full supported stack at a glance.

> **Implementation brief:** the full spoke template, per-platform content checklist, slug list, depth-tiering, schema, and build checklist live in `integrations-implementation-brief.md` (delegation-ready).

**Make-or-break:** structurally similar spokes (the ad platforms especially) go thin/duplicate if they're just the template with the name swapped. Each spoke's unique core is the **reconciliation angle** — how *that* platform's self-reported numbers differ from the real order record and what Bratrax does about it (Meta view-through, Google last-click, TikTok lag, Klaviyo email-assist). Same thesis as the `d18_objection` email; no competitor can write it.

**Two spokes are exempt** because they aren't data sources: `/integrations/claude` and `/integrations/slack` are *surfaces* — ways to reach your data, not sources of it — so there's no self-reported number to reconcile. They clear the anti-thin bar on their own uniqueness instead. The exemption stops there; every data connector carries its reconciliation angle or doesn't ship.

### Placement & URLs
- **`/integrations`** — hub. Every connector with logo, one-line description, link to its page. Ranks for "Bratrax integrations."
- **`/integrations/[tool]`** — one page per connector: `shopify`, `woocommerce`, `meta`, `google-ads`, `klaviyo`, `tiktok`, `bing`, `taboola`, `outbrain`, `bloomreach`, plus the two surfaces `claude` and `slack`. Targets "connect [tool] to Bratrax," "[tool] attribution," "Bratrax [tool] integration." **One canonical URL per query** — `/integrations/meta` targets both "Meta" and "Facebook ads" in-copy (no separate `/facebook` page — cannibalization); `google-ads`, not `google`.
- **`/slack` → `/integrations/slack`.** A standalone `/slack` page already exists — built as the Installation landing page the Slack Marketplace submission requires. End state: `/integrations/slack` canonical, `/slack` kept as a 301. **Sequencing:** `/slack` stays put until the hub exists; don't point a live page at an unbuilt section, and don't hold the Marketplace submission for it.

### Scales with the product — ship by depth tier
Each new connector wired = a new page, no rethink. But ship by **tier**, not all at once (better 5 strong pages than 8 with thin ones dragging the cluster):
- **Tier 1 (full, rich, indexable first):** Shopify, Meta, Google Ads, TikTok, Klaviyo.
- **Tier 2 (thinner story):** Bing, Taboola, Outbrain — make genuinely unique, or `noindex`/hold until they have substance.
- **Flagship:** `/integrations/claude` — the BYO-AI connection is a differentiator nobody else can write. **One** canonical URL with feature-depth (Claude + MCP + BYO-AI terms); don't split into a separate `/mcp` page.
- **Roadmap (Pinterest, Amazon, Recharge, Bold, Skio):** **hub-listed only** — no individual indexable page until the connector ships (avoids thin/doorway pages). The ship becomes a changelog entry.

### Per-page template (`/integrations/[tool]`)
- What it is / what it's for.
- **What Bratrax pulls from it** (the data, plainly).
- **How to connect it** — setup steps (`HowTo` schema candidate).
- **What it powers** — which dashboards/insights light up once connected.
- Screenshot, a short FAQ (2–4 Qs, `FAQPage` schema), CTA → connect in-app.

### SEO + internal linking
- Hub: `CollectionPage` + `BreadcrumbList`. Spokes: `SoftwareApplication` or `HowTo` where setup-led.
- Each spoke links to the hub, the homepage, and any `/vs/` page where that connector is a differentiator. The changelog links to the relevant integration page when a connector ships or improves.

### Relationship to the product
These are *marketing/docs* pages, distinct from the in-app **Connectors** tab. They can deep-link into the app's connector flow, and pair naturally with the connector auth-error lifecycle email.

---

<a id="faq-guidelines"></a>
## FAQ: landing page section vs separate page

### Default at launch: FAQ section on the landing page, no `/faq` page

The landing page carries the FAQ. Build a dedicated `/faq` page only when triggers below are met. Premature `/faq` pages tend to be thin, duplicate landing page content, and split SEO authority across two competing URLs.

### How to organize the landing page FAQ section for maximum SEO clout

**Placement.** After the main conversion content (hero, features, proof, comparison) but before the final CTA. The FAQ should not interrupt the conversion narrative; it should reinforce it for the skeptical reader who scrolled past the first CTA without converting.

**Question count.** 8-12 questions. Fewer than 6 looks thin. More than 14 starts pushing the final CTA below useful scroll depth and dilutes the signal.

**Question phrasing.** Phrase each question as users would actually search it. `How does Bratrax compare to Triple Whale?` not `Comparison with competitors`. Use Search Console queries (post-launch) and tools like AlsoAsked or AnswerThePublic (pre-launch) to find real query language.

**Answer length.** 50-150 words per answer. Long enough to be substantive and capture long-tail terms; short enough to not bury the page or make the section unscannable.

**Anchor links.** Each question gets a stable anchor (`#how-does-it-work`). Useful for direct sharing, sales-team linking, and "On this page" navigation if added.

**Schema markup.** Wrap the FAQ section in `FAQPage` JSON-LD schema. This is the single highest-leverage SEO move on the FAQ section — Google still rewards it with FAQ rich snippets in some SERPs (expandable Q&A blocks beneath the title).

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "How much does Bratrax Lite cost?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Bratrax Lite is $99/month flat — no GMV scaling, no annual contract, no demo call. (The $79 founding rate is locked for life for the first 100 members but that window has closed.) Month-to-month, cancel anytime."
    }
  }]
}
</script>
```

**Question mix.** Cover the major objection categories from the brief:
- Pricing reality ("Is $79 real or a bait tier?")
- Setup / non-technical install ("Can a non-developer install this?")
- AI architecture ("What is MCP and why should I care?")
- Trust ("Who is behind Bratrax?")
- Comparison ("How is this different from Triple Whale / Hyros / Northbeam?")
- Capability ("Can I use this if I'm running TikTok ads / Klaviyo / a non-Shopify stack?")
- Migration ("How do I switch from my current tool?")

**Update cadence.** Refresh quarterly based on actual customer questions from support, demo calls, and Reddit/Twitter mentions. The FAQ is a living asset — questions that nobody actually asks are dead weight.

### Triggers to break the FAQ out into a standalone `/faq` page

Build `/faq` when **any one** of these is true:

1. **The landing page FAQ section exceeds ~15 questions** and is pushing the final CTA below useful scroll depth.
2. **Search Console shows recurring informational queries** that the landing page can't address well — e.g., `what is MCP attribution`, `is bratrax SOC2 compliant`, `does bratrax work with klaviyo` — and you want a dedicated page that ranks for them.
3. **You have technical/setup questions** that need 200+ word answers and don't belong in the conversion narrative. (Bonus: most of these probably belong in `/docs` rather than `/faq`.)
4. **Customer support is repeatedly answering the same 5+ questions** that aren't on the landing page and would make better self-serve content than ticket replies.
5. **Press, partners, or affiliates need a stable URL** to point to for "common questions about Bratrax."

### What goes on a standalone `/faq` page when built

- All landing page FAQ questions, plus the additional questions that triggered the breakout.
- Categorized sections (Pricing, Setup, AI/MCP, Comparison, Migration, Security/Compliance, Billing).
- `FAQPage` schema across the page.
- Search/filter for the FAQ if length warrants it.
- Internal links from each answer to relevant blog posts, docs, comparison pages.
- Canonical tag pointing at `/faq` itself (not the homepage section) to avoid duplicate-content issues.

### Avoiding cannibalization

If both the landing page FAQ section and a standalone `/faq` page exist, keep them differentiated:

- Landing page section: 8-12 conversion-relevant questions, focused on the buying decision.
- `/faq` page: comprehensive set including post-purchase, technical, edge-case, and trust questions.

The landing page FAQ should not be a copy-paste of the `/faq` page's first section. Both pages should have unique value. If they end up duplicative, drop the landing page section in favor of a "Have a question? See our FAQ →" link.

---

<a id="about-guidelines"></a>
## About: landing page section vs separate page

### Default at launch: About content lives on the landing page as a small credibility band

A dedicated `/about` page at launch is almost always thinner than the landing page version it would replace. Skip it. Use a credibility band on the homepage instead.

### How to organize the landing page About section for maximum SEO clout

**Placement.** Two viable spots: (a) immediately below the hero as a proof band, or (b) near the bottom before the final CTA as a trust-closing element. For Bratrax Lite, the Inceptly $950M+ / VidTao 100K+ pedigree is a strong objection-killer for the "who are you" skepticism trigger, so placing it as a hero proof band is probably stronger than relegating it to the footer.

**Content recipe.** A small credibility band should include:

- One headline-style line: "Built by Brat Vukovich and the team behind Inceptly ($950M+ in D2C revenue) and VidTao (100K+ marketers)."
- A 2-3 sentence founder note in authentic founder voice. Not corporate. Why Bratrax exists, in Brat's words.
- Optional: photo of founder if it adds trust and is on-brand.
- Outbound link to founder LinkedIn or X profile.
- Optional: 2-3 logos of companies that already use or have endorsed Bratrax / Inceptly.

**Anchor link.** `#about` so it can be linked to directly.

**Schema markup.** Add `Organization` and `Person` JSON-LD on the page. This helps Google build the knowledge panel and links the founder identity to the company.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Bratrax",
  "url": "https://bratrax.com",
  "founder": {
    "@type": "Person",
    "name": "Brat Vukovich",
    "sameAs": [
      "https://www.linkedin.com/in/...",
      "https://x.com/..."
    ]
  }
}
</script>
```

**What NOT to put in the landing page About section:**
- Long brand philosophy or manifesto content (this deserves its own page when written).
- Full team roster (if relevant later, build `/team`).
- Press mentions list (build `/press` later if it accumulates).
- Detailed origin story (save for a `/manifesto` essay).

### Triggers to break About out into a standalone `/about` (or `/manifesto`) page

Build a separate page when **any one** of these is true:

1. **Search Console shows founder-name or brand-origin queries** — `who is brat vukovich`, `bratrax founder`, `who built bratrax`, `is bratrax legit`. You want a page that ranks specifically for these.
2. **You have substantive philosophical or manifesto content** worth publishing at length — 1500+ words. The `Bratrax Philosophical Foundation.pdf` and 37signals philosophy research already in the workspace are exactly this kind of asset. When that content gets written for the web, it earns its own URL.
3. **Press or journalists need a stable URL** to link to as "the official Bratrax about page."
4. **The credibility story expands beyond what fits in a homepage band** — e.g., the team grows, multiple co-founders earn their own bios, customer credibility logos accumulate, press mentions need a home.

### What goes on a standalone `/about` page when built

- Full founder story (Brat's path, why Bratrax exists, the Inceptly/VidTao backstory).
- Brand philosophy / manifesto (if long-form, consider splitting into `/manifesto` or `/why`).
- Team page or section (with photos and brief bios).
- Customer credibility — selected logos, named customers, testimonials.
- Press mentions, podcast appearances, conference talks.
- Outbound links to founder social profiles, Inceptly, VidTao.
- Schema: `AboutPage` plus full `Organization` and `Person` markup.

### The /manifesto angle worth flagging

There is brand philosophy content sitting in the workspace already (`Bratrax Philosophical Foundation.pdf`, `37signals-philosophy-research.md`). That content does not belong on a generic `/about` page. It deserves its own home — likely `/manifesto`, `/why`, or `/principles`.

This is a competitive moat opportunity: nobody writes 2000-word philosophical pieces about Triple Whale. Distinctive long-form positioning content is exactly the kind of asset that compounds — it gets cited, quoted, screenshotted, and linked to. Plan to publish a manifesto page within the first 6 months post-launch.

---

<a id="internal-linking"></a>
## Internal linking strategy

The architecture only pays off if internal linking actually wires the pages together. The biggest comparison-page mistake teams make is publishing them as orphans with no inbound links — Google reads "no inbound links" as "not important."

### Linking rules

**Every `/vs/[competitor]` page links to:**
- All other `/vs/X` pages (sidebar or end-of-page block: "Also comparing: [Northbeam, Hyros, Polar...]").
- The homepage (header logo, primary CTA).
- The matching `/alternatives/[competitor]` page once that exists.
- Any blog post that references that competitor.

**Every blog post that mentions a competitor links to** that competitor's `/vs/X` page contextually. The existing `competitor-teardown-hyros-v5.md` content should link to `/vs/hyros`, and `/vs/hyros` should link back to the teardown.

**The homepage links to** the `/vs/X` set via a "How we compare" section. The homepage is the most-linked page on the site, so a homepage link to a comparison page passes more authority than any other internal link.

### Top navigation — two items, deliberately

**Integrations · Pricing** — plus Log in and the primary CTA. Nothing else.

A nav link appears on every page, which makes it the strongest internal link on the site. Spend it on what you most want to rank (Integrations, the whole programmatic play) and what buyers click (Pricing, highest commercial intent). Everything else — Changelog, FAQ, Newsletter, the `/vs/` set — is reachable from the footer and earns its rankings through content and cadence, not nav position.

**Blocked on content.** `/integrations` and `/pricing` are currently `noindex` placeholders with a single heading each. Do not put them in the nav until they carry real content; two headline nav items leading to empty pages is worse than no nav change.

### Footer — five columns over the legal bar

The legal links keep the separate bottom row added in August 2026. The columns sit above it.

```
PRODUCT        INTEGRATIONS                          COMPARE            COMPANY
Integrations   Shopify           Taboola             vs Triple Whale    Newsletter
Pricing        WooCommerce       Outbrain            vs Hyros           Contact
Changelog      Meta              Klaviyo             …                  Log in
FAQ            Google Ads        Bloomreach          All comparisons →
               TikTok            Claude
               Bing              Slack
                                 All integrations →
───────────────────────────────────────────────────────────────────────────────
© 2026 Bratrax                                    Privacy Policy · Terms of Service
```

**Integrations spans two columns, grouped by category.** Left is where you sell and where you spend (two store platforms, then the four ad platforms); right is native, email/SMS, and the two AI surfaces. Six and six, and the break lands on a real seam rather than an arbitrary midpoint. **The second column carries no visible heading** — the eye reads it as a continuation of the first.

**Accessibility:** that second column still needs a heading in the markup, visually hidden. Without one a screen reader announces six orphan links with no context.

**All twelve spokes are listed, not a Tier 1 subset.** Two columns buys the room, and a site-wide footer link means every spoke satisfies the no-orphan rule the day it ships. `All integrations →` carries anyone who wants the hub.

**Stacking:** on narrow screens the five columns collapse to one and the two integration columns merge under a single heading — which is why the category order matters. Stacked, it reads stores → ads → native → email → AI.

**If five columns feels wide** at the 1080px max-width, Compare and Company can share one column stacked vertically, taking it to four.

**Sequencing.** The Integrations column ships when the spokes do — dead links in a site-wide footer are worse than no column. Product, Compare and Company can be built now.

**Implementation.** The footer exists in eleven places: `partials/footer.html` (fetched at runtime from GitHub raw) plus an inline fallback on ten pages. Both must carry the same structure, or the site changes shape whenever the fetch fails. One mechanical pass.

**No orphan pages.** Every published page must have at least one inbound internal link from a navigational or contextual context. Audit quarterly.

**Anchor text.** Descriptive, not generic. `See how Bratrax compares to Triple Whale →` not `click here`. The anchor text is a ranking signal.

---

<a id="launch-checklist"></a>
## Launch-day checklist

Before publishing the comparison pages and the live `bratrax.com/`:

**Domain consolidation (the SEO-critical block):**

- [ ] Stop the `bratrax.com` → `lite.bratrax.com` redirect; serve waitlist/product content directly at `bratrax.com/`.
- [ ] Add 301 redirects from `lite.bratrax.com/*` → `bratrax.com/*` (or → `bratrax.com/` for the root) so any link equity already on the subdomain passes through.
- [ ] Update all canonical tags to `https://bratrax.com/` (and matching paths for inner pages).
- [ ] Update `og:url` and `twitter:url` to match the canonical.
- [ ] Update the sitemap to list `bratrax.com/` URLs only — no `lite.bratrax.com` entries.
- [ ] Verify `bratrax.com` in Google Search Console as a property after the cutover.
- [ ] Submit the updated sitemap (homepage, `/vs/*`, `/blog/*`) to Search Console.

**Page-level structured data and content:**

- [ ] Rename comparison page files to match URL pattern: `bratrax-lite-vs-triple-whale.html` → `triple-whale.html` in a `/vs/` directory.
- [ ] Add `FAQPage` JSON-LD schema to landing page FAQ section.
- [ ] Add `Organization` + `Person` JSON-LD schema for About content.
- [ ] Add `Product` + `Offer` JSON-LD schema with the $79/$99 founding pricing.
- [ ] Add `BreadcrumbList` schema to comparison pages.
- [ ] Add OG / Twitter card meta on every page (social sharing).

**Crawl, index, and quality checks:**

- [ ] Test all internal links (no 404s, no redirects in internal nav).
- [ ] Add `robots.txt` and confirm `bratrax.com/robots.txt` is reachable.
- [ ] Set up analytics (GA4 or Plausible) and conversion tracking on the signup CTA.

---

<a id="clear-vision"></a>
## Future: Bratrax Clear Vision

Bratrax Clear Vision is a custom-built consultative product (~$5K/mo, dedicated human analyst). It is not a SaaS with apples-to-apples comparison content. Architectural plan:

**Single page at `/clear-vision`** when ready. Brief positioning, target audience qualifier ("for D2C brands at $20M+ GMV with active media buying teams"), case study or two, "talk to us" CTA. Probably 800-1500 words total. No pricing surface.

**No subdomain.** Same logic as Bratrax Lite — there's no upside to splitting authority.

**No `/vs/` pages for Clear Vision.** It does not compete on the same axes as Northbeam or Triple Whale; comparison content would feel forced. If a Clear Vision prospect needs to evaluate alternatives, that conversation happens on the sales call, not on the marketing site.

**Light cross-linking from the Lite homepage.** A small "For brands at $20M+ GMV, see Bratrax Clear Vision →" callout in the pricing section or footer. Discoverable but not prominent enough to confuse the Lite conversion narrative.

**Optional `/clear-vision/case-studies/[customer]` URLs** if/when customer case studies are published. These can rank for branded enterprise queries and serve as sales enablement.

---

## Appendix: decision log

| Decision | Date | Rationale |
|---|---|---|
| Consolidate on `bratrax.com`, drop subdomain | 2026-05-01 | Clear Vision is custom-build, not comparison-friendly. No upside to splitting authority. |
| `/vs/[competitor]` URL pattern | 2026-05-01 | Captures higher-volume "bratrax vs X" search; future-proof against Clear Vision; matches industry norm. |
| Defer `/vs/` hub page until 5+ comparisons | 2026-05-01 | A hub page with 2 cards looks like SEO bloat; 5+ makes it a category asset. |
| FAQ stays on landing page at launch | 2026-05-01 | A standalone `/faq` page at launch would duplicate landing page content; build only when triggers met. |
| About stays on landing page at launch | 2026-05-01 | Generic `/about` adds little; reserve a separate page for substantive manifesto/founder content. |
| Plan to publish 1 new `/vs/X` per month | 2026-05-01 | Builds toward the `/vs/` hub trigger and grows topical authority steadily. |
| Add `/changelog` (+ per-release URLs) | 2026-06-24 | Editorialized product-updates feed from the prod digest — SEO freshness, AI-search "what's new," and a retention/sales asset. |
| Add `/integrations` hub + `/integrations/[tool]` | 2026-06-24 | Programmatic SEO for connector queries; scales as connectors are wired. |
| Integrations SEO arrangement | 2026-06-24 | Per-platform reconciliation angle as the unique core (anti-thin); one canonical URL per query (meta not facebook, google-ads); Claude as one flagship page; roadmap hub-listed only; depth-tiered build. See `integrations-implementation-brief.md`. |
| Slack lives under `/integrations`, not the top level | 2026-08-11 | Slack is a *surface*, not a data source — same class as Claude, which the brief already treats as a special non-connector spoke. Gets `/integrations/slack` with `/slack` as a 301 once the hub ships; needs no menu item of its own. |
| WooCommerce and Bloomreach added to the connector set | 2026-08-11 | Both were missing from the June brief. WooCommerce is a `primary` connector co-equal with Shopify, so "the foundation" is two store platforms and spoke copy can't say "reconciles to Shopify orders." Verified against `connectors/platforms.ts`, the customer-facing list — not `_SUPPORTED_INTEGRATIONS`, which is scoped to the super-admin CRM card and omits live connectors. |
| Top nav = Integrations + Pricing only | 2026-08-11 | A nav link fires on every page, so it's the strongest internal link available — spend it on the page we most want to rank and the page buyers click. Everything else lives in the footer. Blocked until both pages carry real content; they are `noindex` placeholders today. |
| Footer = five columns over the legal bar | 2026-08-11 | Integrations spans two category-grouped columns (6/6, second column unheaded but with a visually-hidden heading for screen readers) so all twelve spokes get a site-wide inbound link and satisfy the no-orphan rule on ship day. Compare and Company can merge into one column if five reads too wide. Integrations column waits for the spokes. |
| Refresh doc to post-launch | 2026-06-24 | $1-trial launch shipped June 2026; founding window closed, $99 standard, 30-day money-back dropped. |
