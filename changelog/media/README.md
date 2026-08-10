# Changelog entry images

Screenshots shown inside entries on <https://bratrax.com/changelog>.

## Naming

One file per entry, named for that entry's slug — the `id` on its `<h3>` in
`changelog/index.html`:

| Entry `<h3 id="...">` | File |
| --- | --- |
| `amazon-integration` | `amazon-integration.png` |
| `support-chat` | `support-chat.png` |

## How to reference one

The image goes between the `</h3>` and the `<div class="a">` body, and always
carries alt text:

```html
<article class="cl-entry" data-type="New">
  <h3 id="amazon-integration">Connect Amazon Ads and Amazon Seller Central to Bratrax<span class="cl-tag cl-tag-inline" style="color:var(--color-acid)">New</span></h3>
  <img src="https://raw.githubusercontent.com/yuolel/bratrax-wip/bratrax-com-static/changelog/media/amazon-integration.png" alt="Bratrax Integrations page showing Amazon Ads and Amazon Seller Central ready to connect">
  <div class="a"><p>…</p></div>
</article>
```

Use the absolute `raw.githubusercontent.com` URL rather than a relative path —
that's the convention the homepage already uses for its `dashboards/*.png`
product shots, and it resolves regardless of how the page is served.

## Specs

- **Format:** PNG. Use a GIF only when motion genuinely carries the meaning —
  a few seconds of UI is easily 2–5 MB versus ~200 KB for a PNG, and would
  dominate the weight of an otherwise very light page.
- **Width:** capture at **~1000px or wider**. The page renders entry images at
  `width: 100%`, which is **~916px** on desktop, so anything narrower gets
  upscaled and looks soft.
- **Shape:** landscape. A portrait screenshot stretched to 916px wide becomes a
  very tall block that dominates the entry.
- **Weight:** roughly **100–250 KB**, the band the existing `dashboards/*.png`
  shots sit in. Crop to the relevant region instead of shipping a full 4K
  desktop capture.
- **Theme:** dark UI — it matches the changelog page's own palette.
- **Alt text:** always. The page carries JSON-LD and cares about SEO, and it's
  the accessible default.

## Which entries get an image

Only ones with a distinct visual surface a customer would recognise: a new
dashboard or panel, a new UI control, a new connector card, a new settings
screen.

Skip entries where there is nothing meaningful to show — bug fixes,
performance improvements, backend attribution changes, or anything whose only
"visual" is a number that looks the same as before.

Images are always optional. Every entry is written to read completely on its
own, so a missing screenshot never blocks publishing.
