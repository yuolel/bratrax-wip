# Slack submission — every field, every value

One page. Copy from here into Slack's forms.

Two places to fill things in:
- **App config** — <https://api.slack.com/apps> → Bratrax. Mostly already set from `slack/manifest.yaml`.
- **Marketplace submission** — the separate listing flow, launched from that app.

Slack reshuffles these forms periodically, so field names may not match exactly.
Match on meaning.

**Connector claims: check the Connections screen, not the code.** Two lists in the codebase
look authoritative and are not. `_SUPPORTED_INTEGRATIONS` in `server/onboarding.py` is
scoped to the super-admin CRM card and omits live connectors. `connectors/platforms.ts`
defines cards that include entries not yet deployed — as of 2026-08-19 it lists Stripe,
GoHighLevel, ClickFunnels and Google Analytics, none of which render for customers. The
only reliable source is **Settings → Connections** in the running app. Both mistakes were
made in this document before this note existed.

---

## 1. App config — already set from the manifest

Verify rather than retype. Source of truth is `slack/manifest.yaml` in `VidTao/bratrax`.

| Field | Value |
|---|---|
| App name | `bratrax` |
| Bot display name | `bratrax` |
| Always show as online | On |
| OAuth redirect URL | `https://api.bratrax.com/slack/oauth_redirect` |
| Event subscriptions request URL | `https://api.bratrax.com/slack/events` |
| Interactivity request URL | `https://api.bratrax.com/slack/interactive` |
| Bot events | `app_mention`, `app_uninstalled`, `app_context_changed`, `app_home_opened`, `message.im`, `tokens_revoked` |
| Org-wide deploy | Off |
| Socket mode | Off |
| Token rotation | Off |

**Background colour:** `#0A0A0A`. ✅ Fixed in the app config. Confirm `slack/manifest.yaml`
matches — it carried `#0b0b0b`, one step lighter, which reads as a seam against any
screenshot pulled from bratrax.com.

**Agents migration:** the manifest moved from `assistant_view` to `agent_view` in
`a95a62220`. Clicking **Update Now** on Features → Agents is still outstanding, is
one-way per app, and rewrites the manifest server-side. See `slack-dev-handover.md`.

### Bot scopes (16) — verify the list matches

`links:read` and `links:write` were removed in `a95a62220`; nothing used them and Slack
rejects scopes held for untestable future functionality.

```
app_mentions:read      assistant:write        channels:history
channels:read          chat:write             files:write
files:read             groups:history         groups:read
groups:write           im:history             im:read
im:write               reactions:write        users:read
users:read.email
```

Every scope needs a written reason via **Manage Reasons**, minimum 75 characters. The rule
is to explain *how the app uses it*, not what the scope does — a reason that describes the
scope, or defers to another entry ("as channels:read, for private channels"), gets bounced.

Three that reviewers question, with the answer:

| Scope | Justification |
|---|---|
| `channels:history`, `groups:history` | Thread context is rebuilt from Slack history on each question. The service is stateless and stores no conversation. |
| `groups:write` | Creates the private `#ext-<slug>` channel in the shared Bratrax community workspace. |
| `users:read.email` | Matches a Slack user to their Bratrax account in the community workspace, so a DM resolves to the right store. |

---

## 2. Listing fields

### App name
```
Bratrax
```

### Short description — 10 words, 73 characters

**LIVE in the listing as of 2026-08-19.**

```
Shopify and WooCommerce attribution that adds up, where decisions happen.
```

"Adds up" replaced "reconciled": same meaning, no accounting vocabulary. Avoid bare superiority adjectives here — "precise", "accurate", "honest" assert quality without saying why, and there is nothing behind them a buyer or reviewer can check. Mechanism words work; character words do not.

### Long description — 2,329 characters

**LIVE in the listing as of 2026-08-19.** Written against Slack's four stated criteria and modelled on their own Hiretron example: one opening that says what the service is, one line on what it connects to, then bullets that are all things the reader *does in Slack*. No headings, no bold — the earlier heading-and-CAPS versions were a product page, not an app listing.

```
Bratrax is an attribution platform for Shopify and WooCommerce brands: rather than trusting what each ad platform claims it drove, it joins your ad spend to your actual order record. That precision comes from recovering the touches most tools quietly drop (a stripped UTM, an expired session, a conversion iOS never reported), so far less of your revenue ends up stranded in a bucket labeled "Direct" — and you can see exactly which channels and campaigns are driving your sales.

This app puts those numbers in Slack. Ask in the channel where the decision is being made, get the answer there, and keep moving — without anyone opening the app.

• Ask the way you'd ask a colleague. Mention @bratrax in a channel, or send it a direct message: "Why did blended ROAS drop last week?" or "Top 10 SKUs by net revenue this month, with returns."

• Get an answer, not a dashboard link. The number, a short explanation of what moved, and charts and tables that are as readable on your phone as on your laptop.

• Ask the obvious follow-up. "And just for Facebook?" works — it remembers what you were talking about. Swap the window to 7, 30 or 90 days with a button, or open the full dashboard when you want to go deeper.

• Answer once, for everyone. The question and the number land in the same place, so nobody has to relay a screenshot or repeat themselves in three places.

• It stays quiet. It speaks when you mention it or message it directly, and it only sees the channels you invite it to.

Bratrax connects to:

Stores — Shopify, WooCommerce, Amazon Seller Central
Advertising — Meta, Google Ads, TikTok, Microsoft Bing, Pinterest, Amazon Ads, Taboola, Outbrain
Email and SMS — Klaviyo, Bloomreach
Landing pages — external page builders, including Funnelish

More are added regularly.

To set up: create a Bratrax account and connect your store, then open Settings → Slack and authorize the app. The bot is in your workspace a few clicks later.

Requires a Bratrax account ($99/mo flat, no GMV scaling). Answers are generated by a large language model and can be wrong — every answer links back to the dashboard it came from, so you can check the number before you act on it. Slack's split-view assistant panel requires a paid Slack plan; on a free plan you can still mention @bratrax in any channel or send it a direct message.
```

### The rest

| Field | Value |
|---|---|
| Background color | `#0A0A0A` |
| Categories (max 3) | Analytics · Marketing — plus Finance if offered. **Bots is not in the dropdown**; it was an App Directory category and didn't survive into the Marketplace. Two is fine. |
| Installing your app | **Install from your landing page** |
| Installation landing page | `https://bratrax.com/slack` |
| Direct install URL | Leave blank — not applicable with the landing-page option |
| Privacy policy URL | `https://bratrax.com/privacy-policy` |
| Support URL | `https://bratrax.com/faq` |
| Support email | `support@bratrax.com` |
| Supported languages | English (U.S.) |
| YouTube video | Skip |
| Pricing model | Paid — requires a Bratrax subscription. Bratrax Lite, $99/mo. No free tier for the Slack app on its own. |

**Why landing page, not direct install:** the install is initiated from inside Bratrax.
`POST /settings/slack/install` mints a single-use OAuth state bound to the customer's
account, and the callback rejects anything without it. A direct install from the
Marketplace would arrive with Slack's own state and fail every time.

---

## 3. Reviewer testing

The field asking how reviewers should test. Suggested text — **swap in real credentials
before submitting**:

```
Bratrax is a paid analytics product, so the assistant needs an account with
connected store data to answer anything. We've set up a test account on our
demo workspace, which contains synthetic data.

Sign in:  https://bratrax.com/login
Email:    [FILL IN]
Password: [FILL IN]

To connect the app:
1. Sign in at the link above.
2. Go to Settings → Slack and click "Connect Slack."
3. Approve the consent screen. You'll be returned to Bratrax.
4. In your Slack workspace, invite @bratrax to any channel, or DM it.

Questions that will return data:
- "What was my spend today vs yesterday?"
- "Top 5 campaigns by ROAS this week"
- "Chart revenue by channel for the last 14 days"
- "What dashboards do I have?"

Notes:
- The assistant is read-only. It answers when mentioned or messaged directly
  and never posts on its own.
- Setup begins inside Bratrax rather than in Slack, because the connection has
  to be bound to a specific store account.
- Answers are generated with Anthropic's Claude. This is disclosed in our
  privacy policy at https://bratrax.com/privacy-policy (sections 2.3 and 4.2).
```

---

## 4. Assets still to produce

The only outstanding work besides credentials.

**App icon** — square, 512×512 minimum, PNG. `assets/bratrax-icon.png` is the starting
point; check it meets the size floor. Slack renders it small and on both light and dark,
so verify legibility at 32px.

**App images** — up to 6, 1600×1000. In priority order:

1. A Slack thread: "Why did blended ROAS drop last week?" and the answer breaking down the CPC move
2. The same thread on an NC-ROAS-by-source table — channel, spend, ROAS rows
3. Attribution dashboard, channel → campaign → ad set → ad drilldown (`dashboards/02-attribution-top.png`)
4. Store Performance, the CFO screen (`dashboards/01-store-performance-top.png`)
5. Before/after the Direct bucket: 20% unattributed → 5%
6. The connector row — Shopify **and WooCommerce**, Meta, Google, TikTok, Klaviyo

Shots 1 and 2 should be **real screenshots from the working bot**, not mockups. They are
the images reviewers study hardest, and a real one also demonstrates the app functions.

Render on `#0A0A0A` with the graph-paper canvas texture. Per the design system, graph
paper stays on the page canvas only — never on cards or data surfaces inside the shot.

---

## Pre-submit checklist

- [ ] `background_color` changed to `#0A0A0A` in the app config **and** `slack/manifest.yaml`
- [ ] `https://bratrax.com/slack` is live (currently on branch `claude/bratrax-slack-marketplace-dqmbbf`)
- [ ] Updated privacy policy is live — the old text contradicted the app
- [ ] FAQ Slack section is live at `https://bratrax.com/faq#slack`
- [ ] Reviewer credentials created and tested end to end by someone who isn't you
- [ ] App icon and at least 3 app images uploaded
- [ ] Events request URL shows "Verified" in the app config
