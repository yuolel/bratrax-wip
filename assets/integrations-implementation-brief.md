# Bratrax Integrations Pages — Implementation Brief

**For:** whoever builds the integrations pages (content + dev)
**Owner:** Yuliya
**Related:** `site-architecture.md` (Integrations section — IA placement, URL conventions)
**Status:** Specced, not yet built. Connector set + Slack placement updated 2026-08-11.

---

## What we're building

A programmatic-SEO **integrations section** on `bratrax.com`: a category-grouped **`/integrations` hub** plus a **`/integrations/[tool]` page per connector**. Goal: rank for "connect [tool] to Bratrax," "[tool] attribution," "Bratrax [tool] integration," and "does Bratrax integrate with [tool]" — organic + AI-search — and show prospects the full supported stack.

**The make-or-break (read this first):** structurally similar pages (especially the ad platforms) read as thin/duplicate to Google and cannibalize each other if they're just a template with the name swapped. Every spoke must carry **proprietary, platform-specific** content. Bratrax's defensible edge is the *reconciliation angle* — see below. Without it, don't ship the page.

---

## The unique core of every spoke: the reconciliation angle

The one thing no competitor or aggregator can write, and what makes each page non-thin: **how that platform's self-reported numbers differ from what actually sold, and what Bratrax does about it.**

- **Meta** over-reports view-through conversions.
- **Google** leans last-click.
- **TikTok** has reporting lag.
- **Klaviyo** claims email-assisted revenue.

Each spoke explains *that platform's specific discrepancy* and how Bratrax reconciles it to the real order record — Shopify or WooCommerce, whichever the merchant runs. (This is on-brand and the same thesis as the `d18_objection` email.) Make this the heart of each page.

### The exception: surface pages

Two pages in this section are **not data sources**. Nothing flows in from them; they are ways to *reach* your data rather than sources *of* it — so there is no self-reported number to reconcile and the angle above does not apply.

- **`/integrations/claude`** — point your own AI at your data via MCP.
- **`/integrations/slack`** — ask your numbers in a Slack channel.

These are exempt from the reconciliation requirement because they clear the anti-thin bar a different way: neither is a template with a name swapped, and no competitor can write either one. **The exemption is limited to these two.** Any future page that is a data connector must carry its reconciliation angle or not ship.

---

## Hub (`/integrations`) — grouped by category

| Category | Connectors | Slug |
|---|---|---|
| Your store (the foundation) | Shopify, WooCommerce | `/integrations/shopify`, `/woocommerce` |
| Ad platforms | Meta, Google Ads, TikTok, Bing | `/integrations/meta`, `/google-ads`, `/tiktok`, `/bing` |
| Native advertising | Taboola, Outbrain | `/integrations/taboola`, `/outbrain` |
| Email & SMS | Klaviyo, Bloomreach | `/integrations/klaviyo`, `/bloomreach` |
| Ask your data (surfaces, not sources) | Claude (BYO-AI / MCP), Slack | `/integrations/claude`, `/slack` |
| Coming soon (hub-listed only) | Pinterest, Amazon, Recharge, Bold, Skio | — no page until shipped |

Hub content: short intro, the category groups above with logo + one-liner + link per live connector, the "coming soon" list, a CTA. Not just a link list — it should rank for "Bratrax integrations" on its own.

**Verify the connector list before building.** The categories above were reconciled against the product on 2026-08-11. The customer-facing source of truth is
`rill/web-local/src/lib/bratrax/connectors/platforms.ts` — the list a customer actually sees in **Settings → Connectors**. Do **not** verify against `_SUPPORTED_INTEGRATIONS` in `server/onboarding.py`; that registry is scoped to the super-admin CRM card and omits live connectors.

### Slug / canonicalization rules
- **One canonical URL per query — no cannibalization.**
- **Meta:** single page at `/integrations/meta`; target *both* "Meta" and "Facebook ads" in the title/H1/body. **Do not** make a separate `/facebook` page.
- **Google:** `/integrations/google-ads` (matches the real query; avoids ambiguity with "Google").
- Lowercase, hyphens not underscores, no trailing slash.

### `/slack` → `/integrations/slack` — sequencing matters

A standalone **`/slack`** page already exists. It was built as the Installation landing page Slack's Marketplace submission form requires, and it is the URL going into that form.

The end state is `/integrations/slack` as the canonical, with **`/slack` kept as a 301 redirect** — convention-compliant URL that inherits hub link equity, short URL preserved for the Marketplace listing, the in-app link, and saying out loud. A redirect is not a competing page, so there's no cannibalization.

**Do not move it before the hub exists.** Never point a live page at a URL under an unbuilt section, and don't hold the Marketplace submission for it. Order of operations:

1. `/slack` stays as-is and goes into the Slack submission form. *(now)*
2. `/integrations` hub ships.
3. Page moves to `/integrations/slack`; `/slack` becomes a 301.
4. Update the Marketplace listing's landing-page field to the new URL — or leave it, since the redirect resolves. Prefer updating it: reviewers check that the field's URL loads directly.

---

## Spoke page template (`/integrations/[tool]`)

Each spoke needs these **platform-specific** sections (not generic boilerplate):

1. **What it is / what it's for** — framed for this platform.
2. **What Bratrax pulls from [platform]** — the actual data/fields, plainly.
3. **How [platform]'s numbers differ from reality** — the reconciliation angle above. *This is the unique core.*
4. **How to connect it** — platform-specific setup + quirks (Meta token expiry / CAPI, Google campaign-naming, TikTok reporting lag, etc.).
5. **What it powers** — which dashboards/insights light up once connected.
6. **FAQ** — 2–4 platform-specific questions (`FAQPage` schema).
7. **CTA** → connect in-app.

Plus a screenshot. Voice: plain, honest, confident — the Bratrax/Brat site voice.

### Four special pages
- **`/integrations/shopify` and `/integrations/woocommerce` (foundation, not peers).** Frame each as *required* — the source of truth everything reconciles to, and the full historical backfill source (a year of store history). Not "one connector among many." A merchant runs one or the other, so these two never compete for the same reader: Shopify targets the default D2C case, WooCommerce targets a searcher who assumes the answer is no. Nobody expects a D2C attribution tool to support Woo, which makes that page unusually high-intent for its volume.
- **`/integrations/claude` (flagship).** Not a data connector — it's "point your own AI at your data." Write it with feature-page depth, targeting Claude + MCP + BYO-AI terms on this **one** URL. Don't split into a separate `/mcp` or `/byo-ai` page (cannibalization); revisit only if MCP-specific search volume grows.
- **`/integrations/slack` (flagship, shipped).** The @bratrax assistant: ask your numbers in a channel and get back tables, charts, and a link into the dashboard. Also a data-flow story worth telling plainly — read-only, answers only when mentioned, one workspace per store.

**Claude and Slack are the two AI surfaces and must not blur into each other.** The distinction is *whose* AI account runs it, and it is the same split now drawn in privacy policy §4.2:

| | Whose AI account | How it's reached |
|---|---|---|
| Claude / MCP | The customer's own Anthropic account | Any MCP client |
| Slack | Bratrax's — no AI account needed on the customer's side | The Slack app |

Each page states its own case and links to the other as the alternative. Do not let either page claim to be "the way to use AI with Bratrax."

---

## Build order & depth-tiering

Better 5 strong pages than 8 with thin ones dragging the cluster down.

- **Tier 1 — build first, full + rich + indexable:** Shopify, Meta, Google Ads, TikTok, Klaviyo. (Highest intent + strongest reconciliation stories.)
- **Tier 1b — WooCommerce.** Same depth as Tier 1, sequenced just behind it. Lower volume than Shopify, but the intent is unusually high: a Woo operator who assumes a D2C attribution tool won't support them converts hard when they find out it does. The setup story is also genuinely different (store API authorization plus the WordPress plugin), so the page writes itself without touching the Shopify page's territory.
- **Tier 2 — thinner story:** Bing, Taboola, Outbrain, Bloomreach. Either invest to make them genuinely unique, or **hold them as hub listings / `noindex` until they have real substance.** Don't ship thin indexable pages.
- **Flagships:** Claude and Slack (build alongside Tier 1 — both are differentiators). **Slack's page already exists** at `/slack` and moves in when the hub ships; it needs a content pass against the spoke template, not a rebuild.
- **Roadmap (Pinterest, Amazon, Recharge, Bold, Skio):** hub-listed only. Build the page when the connector ships — and make that ship a changelog entry.

---

## Schema, linking, indexation

- **Schema:** hub = `CollectionPage` + `BreadcrumbList`; spokes = `SoftwareApplication` (or `HowTo` where setup-led) + `BreadcrumbList` + `FAQPage` for the FAQ block.
- **Internal linking:** hub → every live spoke; each spoke → hub + homepage + the relevant `/vs/[competitor]` page (where that platform is a differentiator) + its changelog entries when the connector ships/improves. Breadcrumbs on every page.
- **Sitemap:** a separate `/integrations/` sitemap; all on the `bratrax.com` subfolder (never a subdomain — consolidates authority).
- **AI-search:** keep the hub a clean entity list and make each spoke answer "does Bratrax work with [tool]?" directly and factually — that's what gets cited by LLMs.

---

## Build checklist

- [ ] Re-verify the connector list against `connectors/platforms.ts` before writing
- [ ] `/integrations` hub (category-grouped, live connectors + "coming soon" list)
- [ ] Tier 1 spokes: shopify, meta, google-ads, tiktok, klaviyo — each with all 7 sections + the reconciliation core
- [ ] Tier 1b: woocommerce (same depth; store-API + WordPress-plugin setup story)
- [ ] Flagship: claude (feature-depth)
- [ ] Flagship: slack — move `/slack` in, 301 the old URL, pass it against the spoke template
- [ ] Update the Slack Marketplace listing's landing-page field to the new URL
- [ ] Tier 2 (bing, taboola, outbrain, bloomreach): build unique or `noindex`/hold
- [ ] Sweep every spoke for "Shopify orders" where it should read "your order record" — two store platforms now
- [ ] Schema on hub + spokes; per-page meta titles/descriptions targeting the real queries
- [ ] Internal links (hub↔spokes, spokes→homepage/`/vs/`/changelog) + breadcrumbs; claude↔slack cross-link
- [ ] Separate `/integrations/` sitemap; footer/nav link to the hub *(placement TBD — nav and footer structure is an open decision)*
- [ ] Ongoing: every new connector shipped = a new spoke + a changelog entry
