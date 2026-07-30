# Handover — Bratrax Slack app branding & Marketplace listing

Paste this as the opening message of the new session.

---

## Context

I'm filling out the Slack app configuration and Marketplace submission for the
**Bratrax** Slack agent — a bot that answers natural-language questions about a
store's attribution data in Slack ("Why did blended ROAS drop last week?").

Bratrax is DTC attribution analytics for **Shopify and WooCommerce**. $99/mo flat
(Bratrax Lite), plus a $5,000/mo Clear Vision tier. Operated by Inceptly LLC.
Enrollment is currently **waitlist-only** — doors open in waves.

A previous session drafted the listing copy from the marketing site but could not
read the Slack implementation, because that session was scoped to
`yuolel/bratrax-wip` (the static marketing site) and a cross-tier restriction
blocked attaching the `VidTao` repos. That's why this session has all three.

## Repos in this session and what I believe each is

- **`yuolel/bratrax-wip`** — the static marketing site (bratrax.com). Contains
  `assets/slack-app-listing.md` (the listing copy), `assets/bratrax-design-system.md`,
  `faq/index.html`, `privacy/index.html`, `terms/index.html`, dashboard screenshots.
  Branch with the work: `claude/bratrex-slack-agent-branding-u7gby7`.
- **`VidTao/bratrax`** — private. Presumed home of the product and the Slack app
  implementation. **Unverified.**
- **`VidTao/rill`** — public fork. Rill is an open-source BI/dashboard tool, so
  this is probably the dashboard layer. **Unverified — confirm before relying on it.**

## What's already settled (paste-ready)

| Slack field | Value |
|---|---|
| App name | `Bratrax` |
| Short description | `Ask your Shopify or WooCommerce numbers anything — spend, revenue, ROAS, and attribution, in Slack.` |
| Background color | `#0A0A0A` (brand `--color-bg`; **not** `#0b0b0b`) |
| Categories (max 3) | Analytics · Marketing · Bots |
| Privacy policy URL | `https://bratrax.com/privacy-policy` |
| Support URL | `https://bratrax.com/faq` |
| Support email | `support@bratrax.com` |
| Supported languages | English (U.S.) |
| YouTube video | Skip for v1 |

The long description is in `assets/slack-app-listing.md` on the branch above,
along with the app-image shot list and the reasoning behind each choice. If that
repo didn't attach, ask me and I'll paste it.

## What I need help with

### 1. Read the Slack implementation and tell me what it actually does

Nobody has verified the listing copy against the code. The long description
currently asserts: read-only Q&A, connect-your-account-then-pick-a-channel setup,
and a specific connector list. **If the code disagrees, the copy is wrong** — and
Slack's reviewers test against the running app, not the listing.

Specifically:
- What OAuth scopes does it request? (Determines what the privacy policy must disclose.)
- Is it read-only Q&A, or does it also push proactive alerts / scheduled digests?
  A digest feature is a strong listing line that's currently missing.
- Does it answer via an LLM? If so, **whose API key** — Bratrax's or the customer's?
  (Critical for the privacy policy — see §3.)
- Which store platforms and ad connectors does the Slack surface actually reach?
- Is there a `/slack` install route or landing page already built anywhere?

### 2. Decide "Installing Your App" — and this hinges on one code answer

Slack offers two options:
- **Install from your landing page** — Marketplace visitors go to my page first, I
  control what happens before OAuth.
- **Install from Slack Marketplace** — requires a *Direct install URL* that drops
  the user straight into the Slack OAuth consent screen.

Prior recommendation was **landing page**, because the app is useless without a
Bratrax account with connected store data (direct install = a bot in your
workspace that can't answer anything, which is exactly what reviewers test), and
because enrollment is waitlist-only. Choosing landing page also removes the
Direct install URL requirement.

**The code question that decides it:** can the OAuth callback handle a Slack
install from someone with *no* Bratrax account yet? If yes — install completes,
then the bot DMs "connect your Bratrax account" with a button — then direct
Marketplace install is viable and converts better. If no, it must be landing page.

### 3. Fix the privacy policy — it currently contradicts the Slack app

I do **not** need a separate policy for the Slack app; one policy can cover it.
But the current one is not sufficient as written. Confirmed by reading
`privacy/index.html` (effective July 29, 2026):

- **Direct contradiction.** The summary says *"Bratrax does not route your data
  through any LLM,"* and §4.2 says *"We do not send your data to any LLM unless
  you initiate the connection."* A Slack bot that answers natural-language
  questions almost certainly does route store data through an LLM server-side.
  Even if it uses the customer's own Anthropic key, Bratrax's server is making
  the call — so that sentence becomes false. **This needs rewording regardless
  of whose key it is.** Answer §1's LLM question first, then fix the wording.
- **§2.2 doesn't list Slack.** It enumerates Shopify, Meta, Google Ads and says
  more "may be supported in the future." Slack is also a different *kind* of
  connection — not a data source you pull from, but a surface you read from and
  write into. Needs its own treatment: what the app reads in a workspace, what's
  stored (workspace ID, bot token, channel IDs, message content?), retention, and
  what happens to the token on uninstall.
- **§4.1 subprocessors doesn't name Slack.** When the bot posts revenue figures
  into a channel, Customer Data flows to Slack. That's arguably a new disclosure.
- §2.4 (no sensitive personal info) is unaffected.

Slack's reviewers check the privacy policy for platform-specific data handling
and reject on its absence.

### 4. Two things to build

- **`https://bratrax.com/slack`** — doesn't exist, and the Installation landing
  page field can't be empty. Needs the Slack-specific demo (a channel screenshot
  with a real answer), both store paths, connect-and-go steps, waitlist CTA.
  Build in `yuolel/bratrax-wip`; follow `assets/bratrax-design-system.md`.
  Interim unblock: point the field at `https://bratrax.com` so the form saves.
- **A Slack section in the FAQ.** `bratrax.com/faq` is the Support URL, and it
  currently contains nothing about Slack. Reusing the main support URL is fine
  with Slack — it wants a working help resource, not a Slack-dedicated one — but
  a reviewer who clicks through and finds no Slack content may leave a comment.
  Three Q&As cover it: how to install, what the app can see, how to disconnect.

## Order I'd like to work in

1. Read `VidTao/bratrax` and answer §1. Everything else depends on it.
2. Reconcile `assets/slack-app-listing.md` against reality; flag every claim that
   doesn't hold.
3. Settle the install method (§2).
4. Draft the privacy policy amendment (§3).
5. Build `/slack` and the FAQ section (§4).

## One caveat about the waitlist

Slack's review team tests that an installed app actually functions. With doors
closed, a reviewer may not be able to get a working account. Confirm we can hand
them live credentials before submitting, or expect a rejection that has nothing
to do with the copy.
