# Launch checklist

Tracking the SEO + infrastructure swaps needed when bratrax.com flips from
redirector to flagship Lite landing page.

## Canonical swap (lite.bratrax.com → bratrax.com)

Today, all canonicals + `og:url` on `/`, `/a/`, `/b/` point at
`https://lite.bratrax.com/a/` to consolidate the A/B test into one indexed
URL. When bratrax.com starts serving the Lite landing page directly, do the
following in one deploy:

- [ ] Stop the `bratrax.com` → `lite.bratrax.com` redirect; serve the Lite
      landing page directly at `https://bratrax.com/`.
- [ ] Add 301s the other way: `lite.bratrax.com/*` → `https://bratrax.com/`
      (or matching path) so accumulated link equity passes to the new home.
- [ ] Update `<link rel="canonical">` on `/index.html`, `/a/index.html`,
      `/b/index.html` from `https://lite.bratrax.com/a/` →
      `https://bratrax.com/`.
- [ ] Update `<meta property="og:url">` on the same three pages to match.
- [ ] Update the Product JSON-LD `offers.url` (currently
      `https://lite.bratrax.com/`) to `https://bratrax.com/` in both
      `/a/index.html` and `/b/index.html`.
- [ ] Update the Organization JSON-LD `logo` URL if the favicon moves with
      the domain.
- [ ] Generate `sitemap.xml` listing `https://bratrax.com/` (and any
      `/vs/` comparison pages, blog posts) with `lastmod` dates.
- [ ] Add `robots.txt` referencing the sitemap.
- [ ] Submit the new sitemap in Google Search Console; request re-indexing
      of `https://bratrax.com/`.
- [ ] Verify in GSC that `lite.bratrax.com/a/` shows the redirect and
      eventually drops out of the index.

## Other pre-launch SEO TODOs (not yet done)

- [ ] Replace the JS-only redirect at `/index.html` with a server-side
      redirect (or render the winning variant directly at the root).
      Crawlers without JS currently see only "Loading…".
- [ ] Pick the winning A/B variant; `noindex` the loser or remove it.
- [ ] Wire `form action` on all email-form elements to a real endpoint
      (currently `#`).
- [ ] Add `alt` text to product preview screenshots when they return to
      the page.
- [ ] If the title for `/b/` is kept, trim it under ~60 chars
      (currently 79) so it doesn't truncate in mobile SERPs.
