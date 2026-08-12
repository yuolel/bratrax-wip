# Bratrax Bulletin — coverage ledger

An index of every changelog entry and whether the Bratrax Bulletin has covered
it. Two routines share this file:

- **The weekly release-comms routine writes new rows.** Whenever it adds entries
  to `changelog/index.html`, it appends one row per entry with `Status: pending`,
  in the same pull request. That makes this file the inventory of what shipped.
- **The monthly Bulletin routine reads and updates rows.** `pending` rows are its
  candidates; after drafting an issue it marks the ones it used.

Because the ledger is maintained here, the Bulletin never has to parse the
changelog's HTML — it reads this table. That is the point of the file.

> **This repository is public.** Keep this file free of anything you would not
> publish: no reasoning about why something was held back, no unreleased feature
> names, no commentary on strategy. Slug, title, type, date, status, issue — and
> nothing else. The status vocabulary carries all the meaning that is needed.

## Status vocabulary

| Status | Meaning | A candidate again? |
|---|---|---|
| `pending` | On the changelog, not yet covered | **Yes — this is the candidate pool** |
| `sent` | Went out as a full entry in an issue | No |
| `recapped` | Appeared in an "Also shipped" list, or was passed over when one ran | No |
| `withheld` | Excluded by decision | No |

Anything not `pending` is closed. An entry deliberately cut from an issue does
not come back around: old news does not get a second audition.

**An "Also shipped" list is last call.** When one runs, every remaining `pending`
row that the issue did not use as a full entry becomes `recapped` — the ones it
printed and the ones it passed over. Otherwise thin entries come up for
re-litigation every month.

**To resurface something**, set its row back to `pending`. Hand-editing is
expected and is the intended override.

## The ledger

`Added` is the date the weekly routine recorded the entry. Rows marked `—` were
seeded by hand when the file was created and predate that.

| Slug | Title | Type | Added | Status | Issue |
|---|---|---|---|---|---|
| `amazon-integration` | Connect Amazon Ads and Amazon Seller Central to Bratrax | New | — | sent | #1 |
| `email-sms-attribution` | Email and SMS touchpoints now appear in your attribution paths | Improved | — | sent | #1 |
| `commerce-profile-graph` | See who's actually behind your revenue | New | — | sent | #1 |
| `media-spend-scope` | Choose exactly which ad accounts count toward your media spend | Improved | — | sent | #1 |
| `support-chat` | Get help without leaving your dashboard | New | — | sent | #1 |
| `pinterest-ads` | Pinterest Ads attribution is live | New | — | recapped | #1 |
| `order-timeline` | See the full story behind every order | New | — | recapped | #1 |
| `bloomreach-integration` | Connect Bloomreach to Bratrax | New | — | recapped | #1 |
| `multi-store-accounts` | Manage multiple stores from one account | New | — | recapped | #1 |
| `dashboard-navigation-fix` | Dashboards load correctly every time you return to them | Improved | — | recapped | #1 |
| `faster-dashboards` | Watch your dashboards update in real time | Improved | — | recapped | #1 |
| `sync-status` | See exactly when your data last synced | Improved | — | recapped | #1 |
| `woocommerce-integration` | Connect your WooCommerce store to Bratrax | New | — | withheld | — |
| `utm-templates` | Copy-paste UTM templates for your ad platforms | New | — | pending | — |

## Issues

The Bulletin routine checks the most recent row's post before drafting: if that
post is still an unsent draft, it drafts nothing and says so in Slack.

| # | Subject | beehiiv post | Status |
|---|---|---|---|
| 1 | Bratrax Bulletin #1: 4 new integrations + who's behind every order | `post_25703e83-bcba-4593-8853-fb10982ec6ca` | draft |
