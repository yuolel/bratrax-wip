# Slack listing copy — verification against the implementation

Every product claim in `slack-app-listing.md` checked against `VidTao/bratrax`
on 2026-07-30. The listing was originally drafted from bratrax.com alone; this
is the reconciliation pass.

Primary sources: `slack/manifest.yaml`, `slack/oauth.py`, `slack/config.py`,
`slack/brain/mcp.py`, `slack/stores.py`, `server/routes/slack_settings.py`,
`server/onboarding.py`, `server/migrations.py`,
`ontology/compiler/generators/clickhouse_attribution.py`,
`meltano/meltano_project/dags/_client_dag_factory.py`, `docs/SLACK_ASSISTANT.md`.

---

## Corrections applied

### 1. Setup order was backwards — the most consequential error

**Was:** "Install to your workspace, connect your Bratrax account, pick a channel."

You cannot install to your workspace first. The install is initiated *from inside
Bratrax*: `POST /settings/slack/install` requires an authenticated admin session
and mints a single-use, 10-minute, `client_id`-bound OAuth state row. The Slack
callback consumes that row and fails closed without it.

This mattered beyond wording — it is what settles the Marketplace "Installing Your
App" question. See the listing's *Installing Your App* section.

**Now:** "Connect your Bratrax account first, then add Slack from Settings → Slack."

"Pick a channel" was also wrong for the common case. In a client's own workspace
the whole workspace binds to one client, so the bot works in any channel it's
invited to — no channel picking. Channel *linking* exists only in the shared
Bratrax community workspace, where the channel is the trust boundary because
answers are visible to everyone in it. Replaced with "Mention `@bratrax` in any
channel or DM it directly."

### 2. Bloomreach — flagged, then reinstated (my error)

I briefly cut Bloomreach from the connector list on the grounds that it was
half-wired. That was wrong, and the claim stands as originally written.

The mistake was reading `_SUPPORTED_INTEGRATIONS` in `server/onboarding.py` as
the canonical connector registry. Its own docstring says otherwise — it backs the
**super-admin CRM Connections card**, not the customer-facing connector list. I
compounded it with a stale `# (when wired)` comment at `onboarding.py:4486`.

Bloomreach is a live connector:

- Customer-facing entry in `rill/web-local/src/lib/bratrax/connectors/platforms.ts`
  with a dedicated `BloomreachCredentialModal.svelte`
- Documented in the in-app help (`content/admin/02-connecting-platforms.md`)
- Extractors exist: `scripts/direct_extract/extract_bloomreach.py`,
  `bloomreach_backfill.py`, `scripts/discover_schemas/bloomreach.py`

**The trap for anyone auditing this again:** `server/routes/sync_status.py:110`
lists bloomreach among platforms with "no live recurring pipeline". That comment
is about how the **Last sync** timestamp is displayed — those platforms fall back
to backfill/connected time instead of `extract_run_metrics`. It is not a
statement that the connector is inert. The same list includes **woocommerce,
taboola, outbrain and pinterest**, all of which are unambiguously supported. Do
not read that line as a support matrix.

**Lesson for future connector claims:** verify against
`rill/web-local/src/lib/bratrax/connectors/platforms.ts` — the list the customer
actually sees — not a server-side registry scoped to one admin screen.

### 3. No digest / proactive-alert line added

The handover flagged a scheduled-digest feature as "a strong listing line that's
currently missing." It's missing because it doesn't exist. There is no scheduler
in `slack/`; `docs/SLACK_ASSISTANT.md` lists scheduled snapshots under known
limitations as a phase-2 idea. The app is strictly reactive — it answers when
mentioned or DM'd and never initiates.

Worth building: the doc notes the Block Kit composer already does most of the
work. Until then it cannot go in the listing, and it would be an obvious miss if
a reviewer tested for it.

---

## Claims that held

| Claim | Verdict | Evidence |
|---|---|---|
| Read-only Q&A | ✅ | 7-tool read-only MCP allowlist; `query_sql` + `workshop_write_knowledge` excluded (`brain/mcp.py`) |
| Shopify + WooCommerce | ✅ | Both in `_SUPPORTED_INTEGRATIONS`, category `primary`; Woo has its own plugin route + stack template |
| Meta, Google, TikTok, Bing, Pinterest, Taboola, Outbrain | ✅ | All in `_SUPPORTED_INTEGRATIONS` |
| Klaviyo | ✅ | In registry, category `optional` |
| External landing pages / Funnelish | ✅ | `external_pages` in registry; `shopify-funnelish-paid-media` stack |
| 5 attribution models (first-touch, last-touch, linear, time-decay, position-based) | ✅ | `clickhouse_attribution.py:24` names exactly these five |
| "A full year of store history backfills" | ✅ | `SHOPIFY_BACKFILL_HISTORY_DAYS = 365`. Precise as written — *store* history is 365d; ad platforms default to 60d, so don't generalise this to "a year of everything" |
| $99/mo flat, Clear Vision $5K/mo | ✅ | Matches faq/index.html. (`docs/lite/CLAUDE.md` says $49 — that file is stale, the site is right) |
| Answers in the channel, charts and tables | ✅ | Native Block Kit `data_visualization` + `data_table`, matplotlib PNG fallback past 20 points |
| Deep link to the matching dashboard | ✅ | `list_canvases` MCP tool returns a pre-built `open_url` |

Not checkable from this repo, unchanged, and inherited from existing site copy:
the first-party-pixel-on-your-own-domain claim, "adblockers can't kill it",
"under 10 minutes" signup-to-dashboards, and the reconciliation claims. These
live in the pixel/ingest path rather than the Slack surface. Flagged only so
nobody assumes this pass validated them.

---

## Naming collision worth knowing

The site already says "Slack access to the data team" — twice in the FAQ and
once on the homepage. That is the **Clear Vision** $5K/mo tier's human support
channel, not this app. Two different things called Slack, on the same site, one
of which is now a Marketplace listing.

The new FAQ section and `/slack` page are written to make the app unmistakable,
but if the Clear Vision copy is ever revised, "direct Slack channel with your
analyst" would remove the ambiguity for good.
