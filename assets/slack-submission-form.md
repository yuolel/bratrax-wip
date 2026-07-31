# Slack submission — every field, every value

One page. Copy from here into Slack's forms.

Two places to fill things in:
- **App config** — <https://api.slack.com/apps> → Bratrax. Mostly already set from `slack/manifest.yaml`.
- **Marketplace submission** — the separate listing flow, launched from that app.

Slack reshuffles these forms periodically, so field names may not match exactly.
Match on meaning.

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
| Bot events | `app_mention`, `app_uninstalled`, `assistant_thread_started`, `assistant_thread_context_changed`, `link_shared`, `message.im`, `tokens_revoked` |
| Org-wide deploy | Off |
| Socket mode | Off |
| Token rotation | Off |

**One change to make.** The manifest carries `background_color: "#0b0b0b"`. It should be
`#0A0A0A` — the actual page background on bratrax.com. One step darker; invisible alone,
visible against a screenshot. Fix it in both the app config and `slack/manifest.yaml`.

### Bot scopes (18) — verify the list matches

```
app_mentions:read      assistant:write        channels:history
channels:read          chat:write             files:write
files:read             groups:history         groups:read
groups:write           im:history             im:read
im:write               links:read             links:write
reactions:write        users:read             users:read.email
```

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

### Short description — 99 characters
```
Ask your Shopify or WooCommerce numbers anything — spend, revenue, ROAS, and attribution, in Slack.
```

### Long description

Plain text, spaced so it survives Slack's editor (see note below).

```
Shopify and WooCommerce attribution that reconciles — answerable in the channel where the decision gets made.

Bratrax combines a first-party pixel with your full order record, so revenue stops landing in a bucket labeled "Direct." Ask for the number in plain English and get it back in Slack, with the math you can audit.

ASK THINGS LIKE

• "NC ROAS by source for the last 30 days — allocate spend by new-customer order share, not total."

• "Why did blended ROAS drop last week?"

• "Funnel dropoff by step, last 7 days."

• "Top 10 SKUs by net revenue this month, with returns."

WHAT'S BEHIND THE ANSWERS

• A first-party tracking pixel served from your own domain, so adblockers can't kill it.

• Your full order record as the canonical attribution unit — when the pixel misses a touch (UTM stripped, session expired, iOS dropped it), the order fills the gap.

• 5 attribution models — first-touch, last-touch, linear, time-decay, position-based — recalculated at query time.

• Numbers that reconcile to your store and to your ad platform reports. Read the config yourself; there is no proprietary math to take on faith.

CONNECTS TO

Stores: Shopify (including Shopify-native subscriptions) and WooCommerce, plus external landing pages and Funnelish funnels via the pixel.

Ads: Meta, Google Ads, TikTok Ads, Microsoft/Bing Ads, Pinterest Ads, Taboola, Outbrain.

Email, SMS and CRM: Klaviyo, Bloomreach.

SETUP

Connect your Bratrax account first, then add Slack from Settings → Slack — one click, and the bot is in your workspace. Mention @bratrax in any channel or DM it directly.

On Shopify, tracking sets itself up; no manual pixel install. On WooCommerce, you authorize the store API and install our WordPress plugin, and onboarding walks you through both. Either way, a full year of store history backfills in the background.

PRICING

Requires a Bratrax account. Bratrax Lite is $99/mo flat — the same bill at $500K GMV or $20M. No contract, no GMV scaling, no token markup.
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
