#!/usr/bin/env python3
"""Compose the Slack Marketplace listing images.

Each image is a real Slack screenshot (identity-patched by patch.py, otherwise
untouched) laid on a Bratrax-branded 1600x1000 plate carrying the headline and
the wordmark.

The plate is rendered from HTML rather than drawn with Pillow so the Bratrax
type — Outfit 900 headline, Space Mono wordmark, the acid highlighter pill —
comes out exactly as the design system specifies. Pillow then pastes the
screenshot into a reserved band and rules a hairline around it.

Why the screenshots are pasted rather than redrawn: a rebuilt Slack card that
is 95% right reads as suspicious to a reviewer comparing the listing against
the live app. A real capture cannot.

THE RENDER TRAP: headless Chromium's `--window-size=W,H` sizes the *window*.
The page gets a viewport CHROME_OFFSET px shorter while the screenshot is still
H tall, padded out with the body background — so the `position: fixed` graph
paper and vignette stop short and leave a band with no grid across the bottom.
The window height is compensated so the viewport lands at exactly 1000, then
the capture is cropped back. Re-measure CHROME_OFFSET if Chromium is upgraded;
the code below fails loudly rather than shipping a seam.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
SHOTS = HERE / "shots"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

W, H = 1600, 1000
CHROME_OFFSET = 87

# Band reserved for the screenshot: below the headline, above the wordmark.
BAND_TOP, BAND_H = 150, 700
BAND_MAX_W = 1320
# Screenshots soften when enlarged, so the band is allowed to go unfilled
# rather than push a capture past this.
MAX_UPSCALE = 1.15

HAIRLINE = (220, 216, 206)

FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=Outfit:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap"
)

PLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1600">
<title>{title}</title>
<link href="{fonts}" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  /* Canvas colour on <html> too, so no bare page shows through if the render
     area is ever larger than the fixed-size body. COLOUR ONLY — the grid lives
     solely on .graph-paper. Duplicating it here stacks two grids outside the
     body box and the lines render visibly darker there. */
  html {{ background-color: #F5F2EB; min-height: 100%; }}
  body {{
    width: 1600px; height: 1000px; overflow: hidden;
    background: #F5F2EB; font-family: 'Outfit', sans-serif; position: relative;
  }}

  .graph-paper {{
    position: fixed; inset: 0;
    background-image:
      linear-gradient(rgba(160,150,130,0.15) 1px, transparent 1px),
      linear-gradient(90deg, rgba(160,150,130,0.15) 1px, transparent 1px);
    background-size: 40px 40px; pointer-events: none;
  }}
  .vignette {{
    position: fixed; inset: 0;
    background: radial-gradient(ellipse at 50% 50%, transparent 45%, rgba(0,0,0,0.06) 100%);
    pointer-events: none;
  }}

  .frame {{
    position: relative; z-index: 1; width: 1600px; height: 1000px;
    padding: 54px 0 56px 0;
    display: flex; flex-direction: column; align-items: center;
  }}
  .headline {{
    font-family: 'Outfit', sans-serif; font-weight: 900; font-size: 56px;
    letter-spacing: -0.5px; color: #1A1A18; text-align: center; line-height: 1.08;
  }}
  /* Acid green is never text on cream — contrast fails. The accent word takes
     the highlighter pill instead: black on solid, undiluted acid. */
  .pill {{ background: #D4FF00; color: #0A0A0A; padding: 2px 12px 4px 12px; }}
  .wordmark {{
    font-family: 'Space Mono', monospace; font-size: 15px; letter-spacing: 3px;
    text-transform: uppercase; color: #7A7568; margin-top: auto;
  }}
</style>
</head>
<body>
  <div class="graph-paper"></div>
  <div class="vignette"></div>
  <div class="frame">
    <div class="headline">{headline}</div>
    <div class="wordmark">bratrax &nbsp;·&nbsp; attribution that adds up</div>
  </div>
</body>
</html>
"""

# Numbered in the order they should be uploaded. The first four are the
# recommended listing set; 05 is a spare.
#
# `email-connect-slack` is deliberately NOT part of that set. Slack's image
# guidance is "show your app/service in the context of Slack, not other tools
# your service may integrate with", and that capture is the Bratrax web app.
# It is built here for the customer email, where showing people where to click
# is the whole point.
IMAGES = [
    (
        "01-campaign-table",
        'The whole table, in the <span class="pill">thread</span>',
        "shot-campaign-table.png",
    ),
    (
        "02-channel-trend",
        'See every channel at <span class="pill">once</span>',
        "shot-channel-trend.png",
    ),
    (
        "03-follow-up",
        'Ask the obvious <span class="pill">follow-up</span>',
        "shot-follow-up.png",
    ),
    (
        "04-suggested-prompts",
        'Know what to ask on <span class="pill">day one</span>',
        "shot-prompts.png",
    ),
    (
        "05-revenue-chart",
        'See what actually drove <span class="pill">revenue</span>',
        "shot-chart.png",
    ),
    (
        "email-connect-slack",
        'Connect it from your <span class="pill">settings</span>',
        "shot-settings-slack.png",
    ),
]


def render_plate(slug: str, headline: str) -> Image.Image:
    html = HERE / f"_plate-{slug}.html"
    html.write_text(PLATE.format(title=slug, fonts=FONTS, headline=headline))

    raw = HERE / f"_raw-{slug}.png"
    subprocess.run(
        [
            CHROME, "--headless", "--no-sandbox", "--disable-gpu",
            "--hide-scrollbars", "--force-device-scale-factor=1",
            f"--window-size={W},{H + CHROME_OFFSET}",
            # Google Fonts must land before the capture; a fallback face changes
            # every measurement and silently reflows the headline.
            "--virtual-time-budget=10000",
            f"--screenshot={raw}", html.as_uri(),
        ],
        capture_output=True, check=True,
    )

    with Image.open(raw) as im:
        if im.size != (W, H + CHROME_OFFSET):
            raise SystemExit(
                f"{slug}: expected {(W, H + CHROME_OFFSET)} from Chromium, got "
                f"{im.size} — re-measure CHROME_OFFSET"
            )
        plate = im.crop((0, 0, W, H)).convert("RGB")
    raw.unlink()
    return plate


def place(plate: Image.Image, shot_path: Path) -> tuple[int, int]:
    shot = Image.open(shot_path).convert("RGB")
    scale = min(BAND_MAX_W / shot.width, BAND_H / shot.height, MAX_UPSCALE)
    size = (round(shot.width * scale), round(shot.height * scale))
    shot = shot.resize(size, Image.LANCZOS)

    x = (W - size[0]) // 2
    y = BAND_TOP + (BAND_H - size[1]) // 2
    plate.paste(shot, (x, y))

    # A hairline stands the white capture off the cream. The design system
    # rules out a shadow here: white on cream already reads as elevated.
    from PIL import ImageDraw

    ImageDraw.Draw(plate).rectangle(
        (x - 1, y - 1, x + size[0], y + size[1]), outline=HAIRLINE, width=1
    )
    return size


if __name__ == "__main__":
    for slug, headline, shot_name in IMAGES:
        plate = render_plate(slug, headline)
        size = place(plate, SHOTS / shot_name)
        out = HERE / f"{slug}.png"
        plate.save(out, "PNG", optimize=True)
        print(f"{out.name}  {W}x{H}  shot {size[0]}x{size[1]}  "
              f"{out.stat().st_size / 1024:.0f} KB")
