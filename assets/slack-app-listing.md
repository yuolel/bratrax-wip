# Bratrax — Slack app listing copy

Copy for the Slack app config + Marketplace submission fields.
Voice: blunt, math-forward, anti-BI-tool. Show the math, don't sell certainty.

**Verified against the implementation** (`VidTao/bratrax` → `slack/`,
`server/routes/slack_settings.py`, `server/onboarding.py`) on 2026-07-30. The
first draft was written from the marketing site alone; every product claim below
has now been checked against code. Corrections are marked `[FIXED]` and the
reasoning is in `slack-app-verification.md`, which also records the claims that
held.

The implementation reference is `docs/SLACK_ASSISTANT.md` in the product repo —
read that before changing any claim here.

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
> Ask your Shopify or WooCommerce numbers anything — spend, revenue, ROAS, and attribution, in Slack.

(99 characters)

**Alt A — leads with the category:**
> Shopify and WooCommerce attribution in Slack. Ask where revenue came from — spend, ROAS, new-customer CPA.

(106 characters)

**Alt B — platform-agnostic, if both names feel crowded:**
> Ask your store data anything — spend, revenue, ROAS, attribution. Numbers that reconcile, answered in Slack.

(108 characters)

Note on the current draft ("Ask your Bratrax store data anything…"): "Bratrax
store data" reads as though Bratrax is the store. Drop the brand from the
sentence — the app name is already directly above it in the listing — and spend
those characters on the platform names instead.

Both **Shopify** and **WooCommerce** are worth the characters. They're the words
an operator scans for, and WooCommerce especially: nobody expects a DTC
attribution tool to support it, so a Woo store owner who doesn't see the word
assumes the answer is no and never opens the listing. Alt B is the fallback if
the two names make the line feel like a spec sheet, but it gives up that filter.

---

## Long description

Renders with bold and lists on the App Detail page.

---

**Shopify and WooCommerce attribution that reconciles — answerable in the channel where the decision gets made.**

Bratrax combines a first-party pixel with your full order record, so revenue stops landing in a bucket labeled "Direct." Ask for the number in plain English and get it back in Slack, with the math you can audit.

**Ask things like**

- "NC ROAS by source for the last 30 days — allocate spend by new-customer order share, not total."
- "Why did blended ROAS drop last week?"
- "Funnel dropoff by step, last 7 days."
- "Top 10 SKUs by net revenue this month, with returns."

**What's behind the answers**

- A first-party tracking pixel served from your own domain, so adblockers can't kill it.
- Your full order record as the canonical attribution unit — when the pixel misses a touch (UTM stripped, session expired, iOS dropped it), the order fills the gap.
- 5 attribution models — first-touch, last-touch, linear, time-decay, position-based — recalculated at query time.
- Numbers that reconcile to your store and to your ad platform reports. Read the config yourself; there is no proprietary math to take on faith.

**Connects to**

Stores: Shopify (including Shopify-native subscriptions) and WooCommerce, plus external landing pages and Funnelish funnels via the pixel.
Ads: Meta, Google Ads, TikTok Ads, Microsoft/Bing Ads, Pinterest Ads, Taboola, Outbrain.
Email, SMS and CRM: Klaviyo, Bloomreach.

**Setup**

Connect your Bratrax account first, then add Slack from **Settings → Slack** — one click, and the bot is in your workspace. Mention `@bratrax` in any channel or DM it directly. On Shopify, tracking sets itself up; no manual pixel install. On WooCommerce, you authorize the store API and install our WordPress plugin, and onboarding walks you through both. Either way, a full year of store history backfills in the background.

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

## Installing Your App — settled: **Install from your landing page**

Slack offers two options. This one is **not a preference — it is the only option
the code supports.** `[FIXED: was an open question]`

The install is initiated from inside Bratrax, never from Slack. `POST
/settings/slack/install` (`server/routes/slack_settings.py`) requires an
authenticated admin session, and it mints a **single-use OAuth `state` row, bound
to the caller's `client_id`, with a 10-minute TTL**. The callback
(`slack/oauth.py`) does nothing but consume that row:

```python
state_row = await stores.consume_oauth_state(state)
if not state_row:
    return _error_page("This install link has expired or was already used. "
                       "Generate a new one from Bratrax → Settings → Slack.")
```

A Slack Marketplace **Direct install URL** sends the user to Slack's consent
screen with Slack's own `state`, so it arrives at the callback with no matching
row. Every direct install would fail on that error page. `client_id` is resolved
*only* from the state row — there is no fallback path that could infer the tenant
after the fact.

So: **Install from your landing page**, pointed at `https://bratrax.com/slack`.
This also removes the Direct install URL requirement entirely.

The product reasons point the same way, and are worth keeping in mind if anyone
revisits this: the app is useless without a Bratrax account with connected store
data (a direct install is a bot that can answer nothing — exactly what a reviewer
would test), and enrollment is waitlist-only.

**If direct Marketplace install is ever wanted**, the work is a second,
Slack-initiated OAuth path: accept a callback with no state row, persist the
installation as unclaimed, and have the bot DM a "connect your Bratrax account"
link that binds `team_id → client_id` on completion. That is a real feature with
a real tenancy-safety surface (an unclaimed installation must resolve to *no*
tenant until claimed), not a config toggle. Not v1.

### The landing page

**`https://bratrax.com/slack`** — built in this branch (`slack/index.html`).

It carries the Slack-specific demo, both store paths, the corrected connect-and-go
steps, and the waitlist CTA. Pointing the field at the homepage instead converts
worse for two reasons: the homepage sells the $1 waitlist offer rather than the
Slack surface, and it never mentions WooCommerce — so a Woo operator arriving from
the Slack listing hits a page that looks like it isn't for them.

---

## What the app actually does — reviewer-facing facts

Slack reviewers test the running app, so the listing must not promise more than
this. All verified in code.

**Read-only conversational Q&A. Nothing else.** It answers when mentioned or DM'd.
It never initiates. There are no proactive alerts, no scheduled digests, no
"post last week's overview every Monday" — that is listed as phase-2 in
`docs/SLACK_ASSISTANT.md` and there is no scheduler in the service.
`[FIXED: the handover asked whether a digest line could be added — it can't, yet]`

**Answers come from Claude** (Anthropic), running server-side in the
`bratrax-slack` container. Key resolution is first-non-empty: per-client BYOK
(`rill_clients.anthropic_api_key`) → `SLACK_ANTHROPIC_API_KEY` →
`ANTHROPIC_API_KEY`. **The default is Bratrax's key**, so in the default
configuration Bratrax is the party calling the LLM. This is what forces the
privacy-policy change — see below.

**Data reach is a 7-tool read-only MCP allowlist**: `list_metrics_views`,
`get_metrics_view`, `list_canvases`, `get_canvas`, `query_metrics_view_summary`,
`query_metrics_view`, `workshop_read_knowledge`. `query_sql` and
`workshop_write_knowledge` are deliberately excluded, so a hostile Slack message
cannot run free-text SQL or write tenant knowledge. Good line to have ready if a
reviewer asks about prompt injection.

**18 bot scopes**, from `slack/manifest.yaml` (kept in sync with
`SLACK_BOT_SCOPES` in `slack_settings.py`):

`app_mentions:read`, `assistant:write`, `channels:history`, `channels:read`,
`chat:write`, `files:write`, `files:read`, `groups:history`, `groups:read`,
`groups:write`, `im:history`, `im:read`, `im:write`, `links:read`,
`links:write`, `reactions:write`, `users:read`, `users:read.email`

Three of those need a justification ready, because they are the ones a reviewer
questions:

| Scope | Why |
|---|---|
| `channels:history` / `groups:history` | Thread context is rebuilt from Slack history on every question — the service is stateless and stores no conversation |
| `groups:write` | Creates the private `#ext-<slug>` channel in the shared Bratrax community workspace |
| `users:read.email` | Maps a Slack user to their Bratrax account in the community workspace, so a DM resolves to the right tenant |

**What is stored**: four Postgres tables — `slack_installations` (team_id,
enterprise_id, team_name, bot token, bot_user_id, scopes, installer, timestamps),
`slack_oauth_states`, `slack_channel_links`, and the hub flag. **No message
content is persisted.** Verified: the only writes in `slack/stores.py` are to
installations and channel links.

---

## Privacy policy URL

**`https://bratrax.com/privacy-policy`**

⚠️ **The policy as written today contradicts this app and must be amended before
submission.** It states "Bratrax does not route your data through any LLM" and
"We do not send your data to any LLM unless you initiate the connection." Both
become false the moment the Slack app answers a question on Bratrax's Anthropic
key. It also never names Slack — not as a connection, not as a subprocessor.

Paste-ready amendment, with exact anchors: **`slack-privacy-amendment.md`**.

Slack's reviewers check the privacy policy for platform-specific data handling
and reject on its absence, so this is a submission blocker rather than a
tidy-up.

---

## Support URL

**`https://bratrax.com/faq`**

Slack wants a page, not a `mailto:`. Reusing the main support URL is fine — Slack
wants a working help resource, not a Slack-dedicated one — but a reviewer who
clicks through and finds nothing about Slack may leave a comment.

A **Slack section (07)** has been added to the FAQ in this branch covering how to
install, what the app can see, and how to disconnect. `support@bratrax.com`
(already in the site footer) is the escalation path.

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
6. The connector row — Shopify **and WooCommerce**, Meta, Google, TikTok, Klaviyo. This is the only image that carries the Woo signal, so it earns its slot.

Render on `#0A0A0A` with the graph-paper canvas texture. Per the design system,
graph paper stays on the page canvas only — never on the cards or data surfaces
inside the shot.
