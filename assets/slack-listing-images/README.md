# Slack Marketplace listing images

Three 1600×1000 PNGs for the Bratrax listing, plus the source that produces them.

| File | Headline | Shows |
|---|---|---|
| `01-revenue-chart.png` | See what actually drove **revenue** | A charted answer with the full button row — deep link plus the 7/30/90-day re-runs |
| `02-follow-up.png` | Ask the obvious **follow-up** | Two exchanges in one thread, the second scoped off the first |
| `03-suggested-prompts.png` | Know what to ask on **day one** | The Messages tab on first open, with the three suggested prompts |

Upload `01` first — Slack's reviewers study the first image hardest, and it is
the one that shows the most functionality in a single frame.

## Regenerating

```bash
python3 build.py     # writes the three self-contained HTML files
python3 render.py    # renders each to an exactly 1600×1000 PNG
```

`render.py` needs Pillow and a Chromium build; the path to Chromium is a
constant at the top of the file.

Edit copy in `build.py` (the three `IMG*_BODY` blocks), styling in
`_shared.css`. The HTML files are generated — do not hand-edit them.

## Why these are rebuilt rather than screenshotted

Slack's own example listing image is a **redrawn** message card on a flat
colour field, not a raw capture, and the message text in it is far larger than
Slack's real UI. That is deliberate: listing images are displayed small, so a
to-scale screenshot of a 15px Slack message is unreadable in the gallery. These
reproduce the message at roughly 1.5× so it survives the thumbnail.

Everything inside the card is transcribed verbatim from real `@bratrax`
exchanges in the demo workspace — same figures, same wording, same buttons.
Slack returns submissions for images "completely unrelated to your app", and
reviewers compare the listing against the app when they test it.

## Two conventions worth knowing before editing

**The chart is orange on purpose.** Five points and one series puts it inside
the 12×20 native cap in `slack/brain/charts.py`, so Slack renders it as a
native `data_visualization` block — and Slack styles those, not us. Restyling
it to the Bratrax categorical palette would show customers something they will
never see. Charts past those caps come back as matplotlib PNGs and *do* use
the Bratrax palette; a future image of a 30-day trend should look different
here, and that is correct.

**Border-radius splits at the card edge.** The Bratrax frame and the outer
white card are square, per the design system. Elements inside the card keep
their real Slack radii — buttons, avatars, the chart container. Squaring those
off stops the card reading as Slack, which defeats the purpose.

## The render trap

Headless Chromium's `--window-size=W,H` sizes the *window*: the page gets a
viewport 87px shorter while the screenshot is still H tall, padded with the
body background. The graph paper and vignette are `position: fixed`, so they
cover only the viewport and leave a band with no grid across the bottom.
`render.py` compensates the window height so the viewport lands at exactly
1000, then crops back with Pillow. If Chromium is upgraded, re-measure that
offset — the script fails loudly rather than silently shipping a seam.
