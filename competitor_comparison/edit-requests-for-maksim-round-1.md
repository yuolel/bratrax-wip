# Edit Requests — Comparison Pages Round 1

**From:** Yuliya
**To:** Maksim
**Date:** 2026-04-29
**Pages:** `bratrax-lite-vs-hyros.md` + `.html`, `bratrax-lite-vs-triple-whale.md` + `.html`

---

## Read this first

Structurally, both pages are in good shape. All 9 framework sections are present, voice is on-brand, the integrity sections ("When [Competitor] is the right choice") are honest, and the receipts pattern is strong. The MD verification logs are exactly the dated artifact the framework asks for — keep that habit on every future page.

This round is **16 edits across four priorities.** Work through them in order — Priority 1 blocks publish; Priorities 2 and 3 are the substantial content work; Priority 4 is polish. You're doing the content edits; the SEO + publish-prep work is in a separate doc on my side, so you don't need to track it.

Within each priority, items are roughly sequenced top-of-page-down so you're not bouncing around the file.

---

## Priority 1 — Publish-blocking edits

These five items must be resolved first. They're a mix of factual / integrity fixes (1.1–1.3) and product decisions on pricing and CTA destination (1.4–1.5) that block publish.

### 1.1 Triple Whale $5M GMV price disagrees with itself

The number is inconsistent across the MD and HTML versions of the Triple Whale page:

- **MD says `$1,290/mo`** in subhead, TL;DR, At-a-Glance table, Pricing head-to-head, Receipts, and verification log.
- **HTML says `$1,129/mo`** in subhead, TL;DR, At-a-Glance table, Pricing head-to-head, and Receipts.

Both can't be right. Per the framework's claims-verification protocol (*"Every pricing figure is checked within 24 hours of publish"*), this is exactly the bug the framework was written to prevent.

**Action:**
- Re-verify against `triplewhale.com/pricing` today.
- Pick the correct number.
- Propagate to every location in both files.
- Update the verification log with today's verification date.

### 1.2 Restore live source URLs in the HTML

The framework's clearest non-negotiable: *"Link every competitor claim to its live source."* In the MDs, every cited claim is a working hyperlink. In the HTML, those have been collapsed into static attribution text (e.g., `Hyros pricing page · April 2026`) — readable, but no longer one-click verifiable. Outbound links to authoritative sources are also positive E-E-A-T signals for SEO, so this matters on two fronts.

**Action:** In both HTML files, restore live `<a href="...">` links wherever the MD has them:

- Every `quote-source` attribution under a pull quote.
- Every cell in the At-a-Glance table that references a Hyros / Triple Whale claim.
- Every URL inside a body paragraph in the head-to-head sections.

The mono-style attribution lines can stay, but the URL needs to be a live link, not just text. What you deliver should be publish-ready HTML.

### 1.3 Add date stamps to dollar figures in HTML

Framework rule: *"Don't name specific dollar pricing without a date and URL."* The MD includes `(URL, April 2026)` inline; the HTML often dropped the date.

**Action:** Every dollar figure in the HTML — tables, body paragraphs, TL;DRs, subheads — needs an `as of April 2026` (or equivalent) date stamp visible to the reader, plus the live URL per 1.2.

### 1.4 Lock all Bratrax Lite pricing to $99/mo; remove founding-member language from comparison pages

The comparison pages currently lead with `$79/mo` (the founding-member promo) and treat it as the headline price across subheads, TL;DRs, At-a-Glance tables, head-to-head sections, and CTAs. Going forward, **comparison pages should reference $99/mo only.** The founding-member $79/mo offer becomes a reveal on the Bratrax Lite landing page itself, not a feature of the comparison pages.

**Why:** $99 is the regular published price; $79 is a promo capped at 100 seats. Leading with the promo on comparison pages is a small bait-and-switch and makes the pages go stale once founding seats sell out. The price gap with competitors stays decisive at $99 — still ~13x cheaper than Triple Whale at $5M GMV, still ~2.3x cheaper than Hyros's entry tier. The discovery of the founding offer becomes a conversion-lift moment on the Bratrax Lite landing page, not the comparison page.

**Action:** Find every $79 reference and every founding-member mention across both pages (MD + HTML) and update:

- **Subheads:** "Flat $79/mo vs..." → **"Flat $99/mo vs..."**
- **TL;DRs:** "$79–$99/mo" or "$79/mo flat" → **"$99/mo flat"**
- **At-a-Glance table cells:** "$79/mo (founding), $99/mo regular" → **"$99/mo flat"**
- **Pricing head-to-head paragraphs:** rewrite to reflect $99/mo as the single price; drop founding-member language entirely (no "first 100 seats," no "locked for life")
- **CTA section:** drop "Flat $79/mo" framing; remove the "Founding member pricing ($79/mo, locked for life) is available for the first 100 seats." line entirely
- **Verification log:** competitor pricing entries stay as sourced (those are Hyros / Triple Whale numbers); only update internal Bratrax pricing references

This change also propagates into item 4.3 (gap-multiple math) — recompute the multiplier with $99/mo as the base.

### 1.5 Point all CTAs to `lite.bratrax.com`; update CTA copy

Both pages currently link CTAs to `../index.html#waitlist`, with button text reading "Join the Bratrax Lite waitlist →" / "Join the waitlist."

Going forward, comparison-page CTAs should point to **`https://lite.bratrax.com`** — the dedicated Bratrax Lite product URL. Pre-launch, that subdomain redirects to one of two waitlist pages (we're running an A/B test on waitlist copy). On launch day, that subdomain resolves to the proper Bratrax Lite landing page. Pointing comparison pages there from day one means no comparison-page edits at launch — the redirect handles the pre-launch phase, and the proper landing page takes over post-launch.

The redirect logic is on our side; you don't need to do anything other than use the right URL.

**Action:**

- **Change every CTA `href`** from `../index.html#waitlist` to `https://lite.bratrax.com`. This includes the hero/Fast-read aside CTA, the bottom-of-page CTA, and any "Join the waitlist" links inside body copy.
- **Change CTA button text** from "Join the waitlist →" / "Join the Bratrax Lite waitlist →" to **"Get Bratrax Lite →"**. This phrasing works pre-launch (lands on the redirect-to-waitlist page) and post-launch (lands on the proper product page) — no further edits needed at launch.
- **Update the trust-signal copy** under the CTA button: drop "$79/mo" references (per 1.4), keep "No demo call. No annual lock-in. 30-day money-back guarantee."
- **Drop the founding-member sentence** at the bottom of the CTA section entirely.

Both CTAs should land at this structure post-edit:

> **Get Bratrax Lite →**
>
> Flat $99/mo. No demo call. No annual lock-in. 30-day money-back guarantee.
>
> Built by the team behind Inceptly ($950M+ in D2C revenue driven) and VidTao (100K+ marketers). Same attribution engine we use for custom analytics clients — productized for Shopify D2C.

---

## Priority 2 — New content to add

Six items that aren't on the page yet. Listed roughly in order from top of page to bottom.

### 2.1 Add a 1-sentence definition of Bratrax Lite at the very top of each page

The TL;DR has 3–4 bullets but no clean lead-in defining what Bratrax Lite *is*. Both AI systems and skim readers prefer a single declarative sentence as the answer to "What is Bratrax Lite?" Without it, the pages don't surface in that broader query class at all.

**Action:** Add one declarative sentence at the top of each page, above or as the lead-in to the TL;DR. The same definition can repeat verbatim on both pages. Example:

> *"Bratrax Lite is a flat-priced ($79–$99/mo) attribution tool built for Shopify D2C brands that want portable data and the ability to bring their own Claude or ChatGPT."*

It should be stable, declarative, and self-contained — readable without surrounding context.

### 2.2 Add a 1-sentence definition of the competitor near the top

The pages explain *who Hyros / Triple Whale is for* but never define *what they are* in a single extractable sentence. Adding one makes the page citable for the broader "What is Hyros?" / "What is Triple Whale?" queries — which are higher-volume than the narrow vs queries.

**Action:** Add one declarative sentence defining the competitor, near the top of each page (in or near the TL;DR). Examples:

For the Hyros page:
> *"Hyros is a tracked-revenue-priced attribution platform with a proprietary AI agent (AIR) and 1-to-1 analyst onboarding, targeting large multi-channel ad operations."*

For the Triple Whale page:
> *"Triple Whale is a GMV-priced ecommerce intelligence platform combining attribution, AI agents (Moby), creative analytics, MMM, and forecasting under one roof."*

Keep it neutral and factual — same Wikipedia-style register you'd use to describe any tool. The integrity-section work and the receipts do the comparative framing later.

### 2.3 Add a first-hand experience anchor in the lede

The Inceptly/VidTao pedigree currently sits only in the CTA at the bottom. Moving a short experience anchor into the lede places the operator perspective where it does work earlier on the page — both for human credibility and for E-E-A-T extractability.

**Action:** Add one sentence near the top (subhead, lede, or first body paragraph). Example phrasings:

- *"Built by the team that's run paid attribution for D2C brands at Inceptly for eight years."*
- *"From the team behind Inceptly's eight-year track record running paid attribution for D2C brands."*
- *"Same attribution engine we've used for D2C brands at Inceptly since 2018, productized for Shopify."*

Keep the full Inceptly + VidTao pedigree in the CTA — this is just adding an early-page anchor, not relocating the existing one.

### 2.4 Add a visible "Last updated: May 1, 2026" line near the H1

Undated content systematically loses to dated content in search and AI ranking — freshness is heavily weighted. Inline mentions of "April 2026" don't carry the same signal as a structured top-of-page date callout.

**Action:** Add a visible `Last updated: May 1, 2026` line near the H1 or directly below the subhead, in a clearly distinct UI treatment (small mono label is fine, similar to the existing eyebrow style).

`May 1, 2026` is the planned publish date — bake that in. The same date will be set as `dateModified: 2026-05-01` in the Article schema during publish prep; the visible UI element and the structured data should match.

When the page is refreshed quarterly (per the framework's verification cadence), update both the visible date and the schema field together.

### 2.5 Add a "Who Bratrax Lite is for" section, parallel to "When [Competitor] is the right choice"

Right now the integrity section names who should pick the competitor, but there's no equivalent structural block for who should pick Bratrax. Bratrax fit is mentioned in the TL;DR and the CTA, but it doesn't get the same visual weight.

**Action:** Add a new section directly above (or symmetrically paired with) "When [Competitor] is the right choice." Same bullet structure — 3–4 bullets naming who Bratrax Lite is built for, in concrete terms (GMV band, channel mix, team shape, decision criteria). Closes the asymmetry and gives every reader a clear "this is for me" or "this isn't" read.

### 2.6 Add a dedicated "Service & Support" head-to-head dimension

Currently "service" is folded into "Onboarding," which only contrasts setup speed. Hyros's 1-to-1 analyst and Triple Whale's CSM/Implementation Specialist are real ongoing service-level differentiators that deserve their own dimension — not just a footnote on speed.

**Action:** Add a 6th head-to-head dimension titled "Service & Support: Self-serve vs. analyst-supported" (or similar). Cover analyst availability, support channels, documentation quality, and ongoing CSM tier. Confront Bratrax Lite's "self-serve, no analyst" position directly — it's a real tradeoff, not a hidden weakness. Same structure as the other dimensions: Bratrax block + competitor block + "Why it matters" note.

---

## Priority 3 — Restructure existing content

Six items where the content is there but needs reshaping for skim, SEO, and AI extractability.

### 3.1 Reshape the H1 to lead with the target keyword

Both HTML pages currently use **"The honest comparison"** as the H1, with `Bratrax Lite vs Hyros` / `Bratrax Lite vs Triple Whale` pushed into a small mono eyebrow above. Google weighs the H1 heavily for keyword relevance, and "The honest comparison" carries zero query-matching value. The eyebrow lives in a `<span>`, which Google sees but discounts.

**Action:** Update the H1 on each page to lead with the target keyword (`Bratrax Lite vs [Competitor]`). The mono eyebrow above the H1 can be removed once the keyword sits in the H1, or repurposed for a different label.

Viable SEO-friendly options:

For the **Hyros** page (target keyword: *Bratrax Lite vs Hyros*):

1. *"Bratrax Lite vs Hyros: The Honest Comparison"* — mirrors the `<title>` tag, on-brand, lowest-risk
2. *"Bratrax Lite vs Hyros: Flat $79/mo vs Tracked-Revenue Tiers"* — leads with the sharpest contrast
3. *"Bratrax Lite vs Hyros: Lean Shopify Tool or Full-Service Platform?"* — frames the buyer's actual decision
4. *"Bratrax Lite vs Hyros, Side by Side"* — short, conversational, still keyword-leading

For the **Triple Whale** page (target keyword: *Bratrax Lite vs Triple Whale*):

1. *"Bratrax Lite vs Triple Whale: The Honest Comparison"* — mirrors the `<title>`, lowest-risk
2. *"Bratrax Lite vs Triple Whale: Flat $79/mo vs GMV-Scaled Pricing"* — leads with the price-model contrast
3. *"Bratrax Lite vs Triple Whale: Focused Attribution or Full Intelligence Platform?"* — frames the scope decision
4. *"Bratrax Lite vs Triple Whale, Side by Side"* — short, conversational variant

**My recommendation:** option 1 on both pages. It mirrors the `<title>` tag we already know works, keeps the on-brand "honest" framing, and consistency between H1 and `<title>` is itself a small SEO positive. Pick whichever phrasing fits the page best — they're all keyword-leading. If you have a fifth option that's better, even better.

**One constraint:** if you drop "honest" from the H1 (options 2–4), it has to land somewhere on the page — subhead or first-section lede — since it's part of how Bratrax differentiates.

### 3.2 Reshape 2–3 H2s per page to include target keyword variations

Right now zero H2s on either page contain "Hyros" / "Triple Whale" / "alternative" / "comparison" / "vs" — all are creative ("Most buyers can decide from this table alone," "Head-to-head, without the theater," etc.). The framework's SEO checklist says *"H2s include variations of the keyword."*

**Action:** Reshape 2–3 H2s on each page to fold the target keyword in naturally. Keep the creative voice — don't force it into every H2.

Examples for the Hyros page:
- *"Most buyers can decide from this Bratrax Lite vs Hyros table alone."*
- *"Bratrax Lite vs Hyros, head-to-head, without the theater."*
- *"When Hyros is the right choice over Bratrax Lite."*

Same pattern for Triple Whale.

### 3.3 Group the At-a-Glance table by category

Currently the table is a flat list — pricing rows, attribution-model rows, AI rows, and onboarding rows are all interleaved.

**Action:** Re-group the table into 4 categorized blocks with subheaders:

- **Pricing & contracts** — Starting price, Price at $5M GMV, Pricing model, Contract terms, Free trial
- **Product scope** — Attribution models, Platform scope, Target buyer
- **AI & integrations** — AI integration, Data portability
- **Service & support** — Onboarding (and the new Service & Support content from 2.6)

Same data, scannable structure.

### 3.4 Compress At-a-Glance cells to facts

The framework says: *"The most important section on the page. Reader should be able to decide from this table alone."* Right now every cell is a full sentence with embedded quoted phrases — there's no visual hierarchy a buyer can scan in 15 seconds.

**Action:**
- Move long quoted phrases (`"We require a quick call to set you up"`, `"Most brands are up and running in 15 minutes…"`) out of the cells into the head-to-head sections.
- Compress every cell to one short phrase or `Yes / No / N/A` where possible.

Example, Hyros "Onboarding" row:
- Currently: `"We require a quick call to set you up"`
- Should be: `Demo call required` (the quote stays in the head-to-head section)

### 3.5 Compress head-to-head paragraphs to ≤60 words

Several Bratrax/competitor blocks in the head-to-head sections are 80–120 words. AI extraction works best on 40–60 word passages; longer paragraphs distribute meaning, making it harder for AI to lift a clean snippet — and harder for human readers to skim.

**Action:** For each Bratrax block and each competitor block inside the head-to-head dimensions, target ≤60 words. The "Why it matters" callout below can stay longer — that's a different content shape and AI handles it differently. Push supporting detail into the "Why it matters" note.

This stacks naturally with the density rework.

### 3.6 Add a table of contents / sticky in-page nav

Both pages run 2,000+ words across 7+ sections, with no intra-page navigation beyond a single "See the table" anchor link. A jumplinks TOC near the top (or a sticky in-page nav on scroll) lifts scroll depth and time-on-page, and gives buyers a way to find the section they care about most.

**Action:** Add either:

- A TOC block right after the TL;DR, with anchor links: At-a-glance comparison, Head-to-head, Receipts, Who Bratrax Lite is for / When [Competitor] is right, Migration, FAQ
- OR a sticky in-page nav that highlights the current section as the user scrolls

Either works — pick whichever fits the visual treatment best. Make sure each major section has a stable anchor ID (`#comparison-table`, `#head-to-head`, `#receipts`, `#who-bratrax`, `#when-competitor`, `#migration`, `#faq`) so cross-linking can target them cleanly later.

---

## Priority 4 — Polish

Smaller cleanups.

### 4.1 Hyros MD: ambiguous "20K"

The Hyros MD's At-a-Glance table and TL;DR reference `20K tracked monthly revenue`. No dollar sign — ambiguous (20K what? customers? leads? dollars?). The HTML correctly says `$20k`.

**Action:** Sync the MD to `$20K` (or `$20,000`) everywhere it appears. Same fix for any other bare-number references.

### 4.2 Vendor name casing consistency

Framework rule: *"Hyros not HYROS in body text, though their own branding varies."* Both pages mostly comply, but spot-check the receipts where you've quoted Hyros directly — keep their casing inside the quote, but normalize to `Hyros` in your own surrounding prose.

### 4.3 Triple Whale MD: gap-multiple math

After 1.1 (correct Triple Whale price) and 1.4 (Bratrax Lite locked at $99/mo), recompute the multiplier. The Bratrax base is now $99/mo (not $79). New math:

- If Triple Whale at $5M GMV is $1,290/mo → ~13x difference ($1,290 / $99)
- If Triple Whale at $5M GMV is $1,129/mo → ~11x difference ($1,129 / $99)

Update every reference to the multiplier — subhead, pricing head-to-head paragraph, and any other location that names the gap. MD currently says "16x"; HTML says "15x." Both are wrong now and need to land on the new number.

### 4.4 Verification log placement (note, not action)

The MD verification log is excellent — keep it as-is. **Don't add it to the HTML.** It's an internal verification artifact, not part of the published page. Just make sure every claim in the verification log corresponds to a live link in the published HTML (per 1.2).

---

## What's working — keep doing this

So this isn't all red ink:

- **9-section structure** is fully present on both pages. Don't change the underlying scaffolding.
- **TL;DRs** lead with who-should-pick-which in plain language. That's the right pattern.
- **"Why it matters" note boxes** after each head-to-head dimension are doing the so-what work the framework calls for.
- **Receipts** follow the 3-quote shape (homepage / vendor self-admission / customer review) and properly contextualize the Trustpilot/G2 aggregates rather than cherry-picking. The Hyros "Set up in seconds" vs. "We require a quick call" contradiction across two of their own pages is the strongest receipt either page has — that's the level we want.
- **Inceptly pedigree anchor** is reproduced verbatim in both CTAs.
- **Voice** stays grounded — no dupe-seat framing, no Becker/Orbach jokes, no "stop wasting money," no buzzwords. No peer DTC practitioner citations. All compliant.
- **MD verification log** is excellent. Keep building these on every future page.
- **Integrity sections** ("When Hyros / Triple Whale is the right choice") name the competitor's real strengths without hedging. Trust-builder.

---

## What's NOT in scope for this round

Visual density rework, sticky CTAs, mobile pass, receipts visual treatment — those come in the next round once Priority 1–4 above are in. Don't pre-optimize.

The full SEO + publish-prep pass (canonical tags, schema markup, social meta, internal linking, machine-readable files, etc.) is mine and lives in a separate doc — you don't need to track it.

---

## Delivery checklist

When you send the next version back, please confirm:

**Priority 1**

- [ ] 1.1 — Triple Whale $5M GMV price re-verified, single correct number used everywhere in both MD and HTML
- [ ] 1.2 — All HTML source attributions are live `<a href>` links (table cells, body, receipts)
- [ ] 1.3 — Every dollar figure in HTML carries a date stamp
- [ ] 1.4 — All Bratrax Lite pricing locked to $99/mo across both pages (MD + HTML); founding-member language removed entirely
- [ ] 1.5 — All CTAs point to `https://lite.bratrax.com`; CTA copy reads "Get Bratrax Lite →"; trust-signal copy updated

**Priority 2**

- [ ] 2.1 — 1-sentence Bratrax Lite definition added at top of each page
- [ ] 2.2 — 1-sentence competitor definition added near top of each page
- [ ] 2.3 — First-hand experience anchor (Inceptly pedigree) added to lede or first body paragraph
- [ ] 2.4 — Visible "Last updated: May 1, 2026" line added near the H1 on each page
- [ ] 2.5 — "Who Bratrax Lite is for" section added, parallel to "When [Competitor] is the right choice"
- [ ] 2.6 — "Service & Support" added as a dedicated 6th head-to-head dimension

**Priority 3**

- [ ] 3.1 — H1 reshaped to lead with target keyword on both pages
- [ ] 3.2 — 2–3 H2s per page reshaped to include target keyword variations (kept the creative voice)
- [ ] 3.3 — At-a-Glance table re-grouped into 4 categorized blocks
- [ ] 3.4 — At-a-Glance cells compressed to facts (long quotes moved to head-to-head sections)
- [ ] 3.5 — Head-to-head paragraphs compressed to ≤60 words; supporting detail moved into "Why it matters" notes
- [ ] 3.6 — Table of contents / sticky in-page nav added; every major section has a stable anchor ID

**Priority 4**

- [ ] 4.1 — Hyros MD: `20K` → `$20K` sync
- [ ] 4.2 — Vendor name casing spot-checked
- [ ] 4.3 — Triple Whale MD: gap-multiple math reconciled to whichever price is correct
- [ ] 4.4 — Verification log kept in MD only (not added to HTML)

---

*Reviewer: Yuliya | Approval after Yuliya pass: Brat | Framework: BRATRAX - Competitor Teardowns.md*
