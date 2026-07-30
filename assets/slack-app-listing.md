# Bratrax — Slack app listing copy

Copy for the Slack app config + Marketplace submission fields.
Source of truth for product claims: `index.html` (bratrax.com homepage).
Voice: blunt, math-forward, anti-BI-tool. Show the math, don't sell certainty.

---

## App name

**Bratrax**

Alternate: `bratrax` (lowercase, matches the wordmark)

Slack renders the name as a proper noun next to the grey `APP` badge and in
`@mentions`, so title case reads correctly there. The lowercase wordmark still
carries the brand in the icon. Do not append "AI", "Bot", or "App" — Slack's
review guidelines push back on those.

---

## Short description

Limit is ~140 characters. Slack reviewers want functional clarity, not superlatives.

**Primary:**
> Ask your Shopify numbers anything — spend, revenue, ROAS, and attribution, right in Slack.

(90 characters)

**Alt A — leads with the category:**
> Shopify attribution in Slack. Ask where revenue came from — spend, ROAS, new-customer CPA — and get numbers that reconcile.

(123 characters)

**Alt B — closest to the current draft, minus the self-reference:**
> Ask your store data anything — spend, revenue, ROAS, attribution. Shopify numbers that reconcile, answered in Slack.

(116 characters)

Note on the current draft ("Ask your Bratrax store data anything…"): "Bratrax
store data" reads as though Bratrax is the store. Drop the brand from the
sentence — the app name is already directly above it in the listing — and spend
those characters on the word **Shopify**, which is what a browsing operator
filters for.

---

## Long description

Renders with bold and lists on the App Detail page.

---

**Shopify attribution that reconciles — answerable in the channel where the decision gets made.**

Bratrax combines a first-party pixel with the full Shopify order record, so revenue stops landing in a bucket labeled "Direct." Ask for the number in plain English and get it back in Slack, with the math you can audit.

**Ask things like**

- "NC ROAS by source for the last 30 days — allocate spend by new-customer order share, not total."
- "Why did blended ROAS drop last week?"
- "Funnel dropoff by step, last 7 days."
- "Top 10 SKUs by net revenue this month, with returns."

**What's behind the answers**

- A first-party tracking pixel served from your own domain, so adblockers can't kill it.
- The full Shopify order record as the canonical attribution unit — when the pixel misses a touch (UTM stripped, session expired, iOS dropped it), the order fills the gap.
- 5 attribution models — first-touch, last-touch, linear, time-decay, position-based — recalculated at query time.
- Numbers that reconcile to Shopify and to your ad platform reports. Read the config yourself; there is no proprietary math to take on faith.

**Connects to**

Shopify, Meta Ads, Google Ads, TikTok Ads, Bing Ads, Taboola, Outbrain, Klaviyo.

**Setup**

Install to your workspace, connect your Bratrax account, pick a channel. Most stores go from signup to live dashboards in under 10 minutes, with full historical backfill from day one — every order, customer, and SKU since you opened the store.

**Pricing**

Requires a Bratrax account. Bratrax Lite is $99/mo flat — the same bill at $500K GMV or $20M. No contract, no GMV scaling, no token markup.

---

## Background color

**`#0A0A0A`** — not `#0b0b0b`.

`#0A0A0A` is `--color-bg` in the design system and the actual page background on
bratrax.com. `#0b0b0b` is one step lighter and will read as a seam against any
screenshot or OG image pulled from the site. The difference is invisible alone
and visible side by side.

---

## Slack Marketplace categories

Pick up to 3, from Slack's fixed dropdown:

1. **Analytics** — primary. This is the shelf operators browse.
2. **Marketing** — attribution, ad spend, ROAS.
3. **Bots** — it answers questions conversationally.

Swap **Bots** for **Finance** if the intended reader is the CFO/founder rather
than the media buyer. Do not pick **Developer Tools** — the MCP endpoint is a
Bratrax feature, not what this Slack app is.

---

## Installation landing page

**`https://bratrax.com/slack`** — does not exist yet. Needs building.

Slack requires a URL where a user can learn about and install the app. Pointing
it at the homepage works but converts worse: the homepage sells the $1 waitlist
offer, not the Slack surface. A `/slack` page should carry the Slack-specific
demo (a channel screenshot with a real answer), the connect-and-go steps, and
the same waitlist CTA.

---

## Privacy policy URL

**`https://bratrax.com/privacy-policy`**

Before submission, confirm the policy covers Slack-specific data handling —
what the app reads from the workspace, what it stores, and retention. Slack's
reviewers check for this explicitly and reject on its absence.

---

## Support URL

**`https://bratrax.com/faq`**

Slack wants a page, not a `mailto:`. The FAQ is the honest answer today.
`support@bratrax.com` (already in the site footer) should be visible on that
page as the escalation path.

---

## YouTube video (optional)

Skip for v1. A weak demo video costs more than no video. If one gets made, the
strongest 45 seconds is the Monday-morning workflow from the homepage:
the CSV-export-into-ChatGPT ritual, then the same question asked once in Slack.

---

## App images (optional, up to 6 · 1600×1000)

Shot list, in priority order:

1. A Slack channel thread: operator asks "Why did blended ROAS drop last week?", Bratrax answers with the CPC-doubling breakdown.
2. The same thread on the NC ROAS-by-source table — the channel/spend/ROAS rows.
3. The Attribution dashboard, channel → campaign → ad set → ad drilldown (`dashboards/02-attribution-top.png`).
4. Store Performance, the CFO screen (`dashboards/01-store-performance-top.png`).
5. Before/after Direct bucket: 20% unattributed → 5%, the two Exhibit blocks side by side.
6. The connector row — Shopify, Meta, Google, TikTok, Klaviyo.

Render on `#0A0A0A` with the graph-paper canvas texture. Per the design system,
graph paper stays on the page canvas only — never on the cards or data surfaces
inside the shot.
