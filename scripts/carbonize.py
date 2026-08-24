# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
"""carbonize — render a code snippet to a brand-styled carbon.now.sh PNG.

Usage:  uv run carbonize.py <snippet-file> <out.png> [--font-size 14px]

Wraps carbon-now-cli (needs node/npx; downloads Playwright chromium on first
run) with the SGLang deck settings, then trims the dead space carbon's editor
leaves under short snippets and rebuilds the bottom rounded corners.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

SETTINGS = {
    "theme": "one-light",
    "backgroundColor": "rgba(0,0,0,0)",
    "windowTheme": "none",
    "windowControls": True,
    "fontFamily": "JetBrains Mono",
    "fontSize": "14px",
    "lineHeight": "140%",
    "lineNumbers": False,
    "dropShadow": False,
    "paddingVertical": "14px",
    "paddingHorizontal": "18px",
    "widthAdjustment": True,
    "exportSize": "2x",
    "type": "png",
}
CORNER_RADIUS = 30  # px at 2x export


def trim_bottom(png: Path, pad: int = 30) -> None:
    """Crop the empty editor area below the last code pixels; re-round corners."""
    img = Image.open(png).convert("RGBA")
    px = img.load()
    w, h = img.size
    # card bbox from alpha
    alpha = img.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        return
    cl, ct, cr, cb = bbox
    # card background color: sample inside the BOTTOM-left corner (the top-left
    # corner holds the window-control dots and poisons the sample)
    bg = px[cl + CORNER_RADIUS + 10, cb - CORNER_RADIUS - 10][:3]
    # last row that differs from the background (scan card interior, skip corners)
    def row_has_content(y):
        for x in range(cl + CORNER_RADIUS, cr - CORNER_RADIUS, 4):
            r, g, b, a = px[x, y]
            if a > 0 and (abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2])) > 24:
                return True
        return False
    content_bottom = ct
    for y in range(cb - CORNER_RADIUS, ct, -1):
        if row_has_content(y):
            content_bottom = y
            break
    new_cb = min(cb, content_bottom + pad + CORNER_RADIUS)
    if new_cb >= cb - 4:
        return  # nothing worth trimming
    # crop, keeping the same transparent outer margin at the bottom as the top
    img = img.crop((0, 0, w, new_cb + ct))
    # rebuild rounded corners on the (new) card bbox
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (cl, ct, cr - 1, new_cb - 1), radius=CORNER_RADIUS, fill=255)
    a2 = img.getchannel("A").point(lambda v: v)  # copy
    img.putalpha(Image.composite(a2, Image.new("L", img.size, 0), mask))
    # hairline border so a light card reads against a white slide
    ImageDraw.Draw(img).rounded_rectangle(
        (cl, ct, cr - 1, new_cb - 1), radius=CORNER_RADIUS,
        outline=(221, 221, 221, 255), width=2)
    img.save(png)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("snippet")
    ap.add_argument("out")
    ap.add_argument("--font-size", default=None, help='e.g. "16px"')
    args = ap.parse_args()

    out = Path(args.out).resolve()
    settings = dict(SETTINGS)
    if args.font_size:
        settings["fontSize"] = args.font_size

    with tempfile.TemporaryDirectory() as td:
        subprocess.run(
            ["npx", "-y", "carbon-now-cli", str(Path(args.snippet).resolve()),
             "--settings", json.dumps(settings),
             "--save-to", td, "--save-as", "carbon", "--skip-display"],
            check=True)
        Path(td, "carbon.png").replace(out)
    trim_bottom(out)
    img = Image.open(out)
    print(f"wrote {out} ({img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    sys.exit(main())
