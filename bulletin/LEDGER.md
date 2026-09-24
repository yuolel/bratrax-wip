# Bratrax Bulletin — coverage ledger

**This repository is public. Keep this file free of anything you would not publish.**

The contract between two routines:

- The **weekly release-comms routine** appends a `pending` row for every entry
  it adds to `changelog/index.html`, in the same commit as the changelog edit.
- The **monthly Bulletin routine** treats `pending` rows as its candidate pool,
  and closes them out after drafting an issue.

Changelog entries carry no per-entry dates — only month groupings — so a
date-based coverage window is impossible. The `<h3 id="...">` slug is the stable
key, which is why this file is keyed on slugs.

## Statuses

| Status | Meaning |
|---|---|
| `pending` | Shipped and on the changelog; not yet covered by an issue. The candidate pool. |
| `sent` | Covered as a headline entry in the named issue. Closed. |
| `recapped` | Covered as an *Also shipped* bullet in the named issue. Closed. |
| `withheld` | A human decided it does not go in the Bulletin. Closed permanently — not "maybe next time". |

A row's status records **which issue covers it**. Whether that issue was
actually published is answered by the Issues table below.

`source` is `changelog` unless the item never had a changelog entry, in which
case it is `manual` — otherwise a thing like a video playlist or a launch reads
as never-covered forever.

## Entries

| Slug | Title | Type | Added | Status | Issue | Source |
|---|---|---|---|---|---|---|
| `order-timeline` | See the full story behind every order | New | 2026-05 | recapped | #1 | changelog |
| `utm-templates` | Copy-paste UTM templates for your ad platforms | New | 2026-06 | withheld | — | changelog |
| `woocommerce-integration` | Connect your WooCommerce store to Bratrax | New | 2026-06 | withheld | — | changelog |
| `pinterest-ads` | Pinterest Ads attribution is live | New | 2026-06 | recapped | #1 | changelog |
| `sync-status` | See exactly when your data last synced | New | 2026-06 | recapped | #1 | changelog |
| `faster-dashboards` | Watch your dashboards update in real time | Improved | 2026-06 | recapped | #1 | changelog |
| `commerce-profile-graph` | See who's actually behind your revenue | Improved | 2026-06 | sent | #1 | changelog |
| `multi-store-accounts` | Manage multiple stores from one account | New | 2026-06 | recapped | #1 | changelog |
| `dashboard-navigation-fix` | Dashboards load correctly every time you return to them | Improved | 2026-07 | recapped | #1 | changelog |
| `bloomreach-integration` | Connect Bloomreach to Bratrax | Improved | 2026-07 | recapped | #1 | changelog |
| `media-spend-scope` | Choose exactly which ad accounts count toward your media spend | Improved | 2026-07 | sent | #1 | changelog |
| `email-sms-attribution` | Email and SMS touchpoints now appear in your attribution paths | Improved | 2026-07 | sent | #1 | changelog |
| `support-chat` | Get help without leaving your dashboard | Improved | 2026-08 | sent | #1 | changelog |
| `amazon-integration` | Connect Amazon Ads and Amazon Seller Central to Bratrax | New | 2026-08 | sent | #1 | changelog |
| `amazon-cost-settings` | Track your Amazon product costs in Cost settings | New | 2026-08 | recapped | #2 | changelog |
| `connector-reconnect-alerts` | Get notified when a platform connection needs reconnecting | Improved | 2026-08 | recapped | #2 | changelog |
| `referral-attribution-fix` | More accurate attribution when checkout redirects through a payment gateway | Improved | 2026-09 | recapped | #2 | changelog |
| `one-click-reconnect` | Reconnect a broken platform connection in one click | Improved | 2026-09 | recapped | #2 | changelog |
| `brand-domains` | Tell Bratrax about the other domains you own | New | 2026-09 | sent | #2 | changelog |
| `custom-pages-pixel` | Track advertorials and bridge pages with a generic pixel | New | 2026-09 | sent | #2 | changelog |
| `add-a-store` | Start a second store without contacting support | New | 2026-09 | recapped | #2 | changelog |
| `shopify-permission-alerts` | Approve new Shopify permissions in one click | Improved | 2026-09 | recapped | #2 | changelog |
| `regional-shipping-costs` | Set shipping costs by region | New | 2026-09 | sent | #2 | changelog |
| `order-exclusions` | Exclude wholesale or bulk orders from your numbers | New | 2026-09 | sent | #2 | changelog |
| `video-walkthroughs` | Browse short, feature-by-feature video walkthroughs | New | 2026-09 | recapped | #2 | changelog |

**Pending: none.** Every entry on the live changelog is accounted for.

## Issues

| # | Date | beehiiv post | Status |
|---|---|---|---|
| 1 | 2026-08-11 | `post_25703e83-bcba-4593-8853-fb10982ec6ca` | published |
| 2 | 2026-09-23 | `post_1ee7cf45-c6fd-4633-a43c-4e89fe25e150` | published |

## Withheld, and why

- **`utm-templates`** — cut from #1 and again from #2. Two consecutive cuts, so
  closed rather than carried a third time.
- **`woocommerce-integration`** — the list already received four dedicated
  WooCommerce emails in July 2026. Re-announcing it would be the fifth.
