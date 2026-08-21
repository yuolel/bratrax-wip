#!/usr/bin/env python3
"""Render each listing HTML to an exactly 1600x1000 PNG.

Two things make this non-obvious:

1. Headless Chromium's `--window-size=W,H` sizes the WINDOW, not the viewport —
   it hands the page a viewport 87px shorter (measured, not assumed; see
   CHROME_OFFSET) while still writing an H-tall screenshot, padding the
   difference with the body background. So `position: fixed` overlays — which
   the graph paper and vignette must use — stop 87px short and leave a visible
   band with no grid. Compensating the window height puts the viewport at
   exactly 1000 and the overlays cover the whole canvas.

2. That makes the screenshot 1087 tall, so it gets cropped back to 1600x1000
   from the top-left. The bundled ffmpeg can't decode Chromium's PNGs
   ("Invalid data found"), so Pillow does the crop.

Re-measure CHROME_OFFSET if Chromium is ever upgraded: render _probe.html and
read the viewport size it prints.
"""

import subprocess
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

W, H = 1600, 1000
CHROME_OFFSET = 87

SLUGS = ["01-revenue-chart", "02-follow-up", "03-suggested-prompts"]

for slug in SLUGS:
    html = HERE / f"{slug}.html"
    raw = HERE / f"_raw-{slug}.png"
    out = HERE / f"{slug}.png"

    subprocess.run(
        [
            CHROME,
            "--headless",
            "--no-sandbox",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={W},{H + CHROME_OFFSET}",
            # Google Fonts have to land before the capture: a fallback face
            # silently changes every measurement and the layout reflows.
            "--virtual-time-budget=10000",
            f"--screenshot={raw}",
            html.as_uri(),
        ],
        capture_output=True,
        check=True,
    )

    with Image.open(raw) as im:
        if im.size != (W, H + CHROME_OFFSET):
            raise SystemExit(
                f"{slug}: expected {(W, H + CHROME_OFFSET)} from Chromium, got "
                f"{im.size} — re-measure CHROME_OFFSET with _probe.html"
            )
        im.crop((0, 0, W, H)).save(out, "PNG", optimize=True)

    raw.unlink()
    kb = out.stat().st_size / 1024
    print(f"{out.name}  {W}x{H}  {kb:.0f} KB")
