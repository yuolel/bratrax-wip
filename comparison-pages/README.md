# Comparison Pages — Deployment Staging

Staging area for the `/vs/[competitor]` comparison pages. Files dropped here
will be moved into their final served paths (`vs/hyros/index.html`,
`vs/triple-whale/index.html`) before deploy.

This directory is **not** served as-is. It exists to hold the source HTML
files until they are renamed/moved into the `vs/` tree, and to keep the
internal MD research artifacts close to the code without publishing them.

## What needs to land in this directory

Drop these two files into `comparison-pages/` (filenames as-is — they will be
renamed during the move step):

- [ ] `bratrax-lite-vs-hyros.html`
- [ ] `bratrax-lite-vs-triple-whale.html`

Optionally drop the research artifacts into `comparison-pages/_research/`
(this subpath is not served and stays internal):

- [ ] `bratrax-lite-vs-hyros.md`
- [ ] `bratrax-lite-vs-triple-whale.md`

Source on Yuliya's machine:
`C:\Users\Yuliya\Jeeves\brands\bratrax\comparison-pages\`

## Deployment plan once HTML is uploaded

The repo follows the directory-with-index pattern (matches existing
`privacy/index.html` → `/privacy-policy`, `terms/index.html` →
`/terms-of-service`). Final layout:

```
vs/
├── hyros/
│   └── index.html              ← from bratrax-lite-vs-hyros.html
└── triple-whale/
    └── index.html              ← from bratrax-lite-vs-triple-whale.html
og/                             ← create, populate with brand PNGs
├── vs-hyros.png                ← 1200×630, social share preview
└── vs-triple-whale.png         ← 1200×630, social share preview
logo.png                        ← 512×512, schema logo
sitemap.xml                     ← new file, includes the two /vs/* entries
comparison-pages/
├── README.md                   ← this file
└── _research/                  ← internal MD artifacts, not served
    ├── bratrax-lite-vs-hyros.md
    └── bratrax-lite-vs-triple-whale.md
```

## URL mapping

| Source file | Production URL | Hosted file path |
|---|---|---|
| `bratrax-lite-vs-hyros.html` | `https://bratrax.com/vs/hyros` | `vs/hyros/index.html` |
| `bratrax-lite-vs-triple-whale.html` | `https://bratrax.com/vs/triple-whale` | `vs/triple-whale/index.html` |

Trailing-slash policy: **no trailing slash** — matches existing
`/privacy-policy` and `/terms-of-service`, and matches the canonical/og:url
already baked into the HTML.

## Steps Claude Code will run after HTML lands

1. Move `comparison-pages/bratrax-lite-vs-hyros.html` →
   `vs/hyros/index.html` (no edits to meta/schema).
2. Move `comparison-pages/bratrax-lite-vs-triple-whale.html` →
   `vs/triple-whale/index.html` (no edits to meta/schema).
3. Move the two MD files into `comparison-pages/_research/` if uploaded.
4. Create `sitemap.xml` at the repo root with entries for `/vs/hyros` and
   `/vs/triple-whale` (and `/privacy-policy`, `/terms-of-service` for
   completeness).
5. Create `og/` directory with a `.gitkeep` placeholder; real OG PNGs and
   `logo.png` to be uploaded separately by Yuliya.
6. Commit on `claude/upload-competitor-pages-QAsDv` and push.

## Items NOT handled by this branch

These are explicitly out of scope per the deployment brief and need separate
work:

- **Domain consolidation 301s** (`lite.bratrax.com/*` → `bratrax.com/*`) —
  Nginx/Cloudflare config, not files in this repo.
- **OG images and logo.png** — binary assets, must be supplied by Yuliya.
- **`pricing.md`, `llms.txt`, `robots.txt` audit, GSC property setup** —
  separate deploy tasks at the site root level.
- **`/vs/` breadcrumb hub page** — deferred until 5+ comparison pages exist.
  Breadcrumb 404s on click are acceptable per the brief; schema still
  validates.
- **Google Search Console sitemap submission** — manual step post-deploy.

## Decisions already locked in

- **File-naming convention:** Option A (directory-with-index) — matches
  existing `privacy/`, `terms/` pattern.
- **Trailing slash:** none, matching the rest of the site and the canonicals.
- **`lite.bratrax.com` CTA:** kept as-is. Per the root `README.md`,
  `lite.bratrax.com` is still live until the May 12 launch and the signup
  flow has not migrated.
- **MD research files:** stashed under `comparison-pages/_research/`,
  excluded from the sitemap.

## Open items needing Yuliya

- Confirm the OG image filenames (`vs-hyros.png`, `vs-triple-whale.png`)
  and the logo path. If the existing brand logo lives at a different path
  (e.g. `/assets/Bratrax Logo Light Inline.svg`), the JSON-LD
  `Article.publisher.logo.url` and `Organization.logo` fields in both HTML
  files need updating to match before deploy.
- Verify external links in the Receipts section (G2, Trustpilot, Shopify
  App Store reviewer pages) still resolve. Verified April 2026 per the
  brief; reviews can be edited or deleted by their authors.
- Confirm the Typeform URL `https://inceptly.typeform.com/brtrxclrvsn`
  still points to the Bratrax Clear Vision intake form.

## Post-deploy verification (per the brief)

1. Both pages return HTTP 200 at `/vs/hyros` and `/vs/triple-whale`.
2. Canonical, OG, and Twitter meta tags render on view-source.
3. Schema markup validates in Google's Rich Results Test and the Schema.org
   validator (Article, FAQPage, BreadcrumbList, Product, Organization,
   ItemList — zero errors expected).
4. OG previews render correctly in opengraph.xyz and Twitter's Card
   Validator.
5. Sticky table header pins under the site nav while scrolling. If the
   production nav height differs from the assumed 56px, adjust the
   `top: 56px` value on the `th` CSS rule in both HTML files.
6. Sticky sidebar TOC works on viewports ≥1024px.
7. Mobile floating "↑" button appears on viewports <1024px after 600px of
   scroll.
8. Cross-page links resolve — Hyros page → `/vs/triple-whale` and inverse.
9. External review links open correctly.
10. Submit `sitemap.xml` in Google Search Console and request indexing on
    both URLs.
