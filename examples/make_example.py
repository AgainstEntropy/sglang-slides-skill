# /// script
# requires-python = ">=3.10"
# dependencies = ["python-pptx>=1.0", "qrcode[pil]"]
# ///
# Pattern specimen deck — one design-system pattern per slide, ALL content is
# neutral placeholder text.  Do not put real talk content here; copy the page
# you need into your own build script and fill it in there.
# Build:  uv run make_example.py   →  example-deck.pptx

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from sgl_deck import (ACC, ACC2, CW, INK, LINE, MUT, MX, PANEL, SUB, TINT,
                      TINT2, W, Deck)

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"

d = Deck(author="RadixArk · SGLang Team", title="RadixArk deck template — pattern specimens")

# ---- 1 · PATTERN: title slide --------------------------------------------------
s = d.slide()
lw = 4.4
d.image(s, ASSETS / "sglang-logo.png", (W - lw) / 2, 1.0, w=lw)
d.text(s, "Deck Title Goes Here", 0, 2.75, W, 0.85, size=40, bold=True, align="center")
d.text(s, "One-line subtitle — what this talk is about, in twelve words or fewer",
       0, 3.65, W, 0.5, size=17, color=SUB, align="center")
d.text(s, "Speaker Name — RadixArk · SGLang Team", 0, 4.95, W, 0.4, size=15, align="center")
d.text(s, "Venue · Month DD, YYYY", 0, 5.4, W, 0.35, size=12.5, color=MUT, align="center")
d.text(s, "github.com/sgl-project/sglang", 0, 6.9, W, 0.3, size=10.5, color=MUT, align="center")

# ---- 2 · PATTERN: stat row + lead bullets ---------------------------------------
s = d.slide()
d.eyebrow(s, "PATTERN · STAT ROW")
d.title(s, "Claim in the title — numbers as the evidence below")
d.stat_row(s, [("42", "first metric, small caption"), ("1.8×", "second metric"),
               ("99 %", "third metric"), ("7", "fourth metric")], y=1.45)
d.lead_bullets(s, [
    ("Bold lead — ", "one line of gray explanation; keep it under two lines on screen"),
    ("Noun phrase — ", "the lead names a thing, the rest says why it matters"),
    ("Restraint — ", "three to five bullets per slide, never more"),
], x=MX, y=3.0, w=CW, h=2.5, size=13.5)
d.text(s, "One punchline per slide — alone, bold, accent.",
       MX, 6.2, CW, 0.45, size=15, bold=True, color=ACC)

# ---- 3 · PATTERN: comparison table ----------------------------------------------
s = d.slide()
d.eyebrow(s, "PATTERN · COMPARISON TABLE")
d.title(s, "Two columns compared, row labels bold, ours in accent")
d.table(s, [
    [("", {"fill": PANEL}), ("Their approach", {"bold": True, "fill": PANEL}),
     ("Our approach", {"bold": True, "fill": PANEL, "color": ACC})],
    [("Dimension one", {"bold": True}), "placeholder description", "placeholder description"],
    [("Dimension two", {"bold": True}), "placeholder description", "placeholder description"],
    [("Dimension three", {"bold": True}), "placeholder description", "placeholder description"],
    [("Dimension four", {"bold": True}), "placeholder description", "placeholder description"],
], x=MX, y=1.6, col_w=[2.2, 4.9, 5.03], row_h=0.62)
d.text(s, "Header row gets the PANEL fill; keep cells to one line each; add a fifth column only if you must.",
       MX, 5.1, CW, 0.4, size=11.5, italic=True, color=MUT)
d.text(s, "Bottom takeaway — one sentence, accent, bold.",
       MX, 6.15, CW, 0.45, size=15, bold=True, color=ACC)

# ---- 4 · PATTERN: cards grid ------------------------------------------------------
s = d.slide()
d.eyebrow(s, "PATTERN · CARDS GRID")
d.title(s, "One card per item — highlight at most one")
cards = [("Card title", "one detail line — versions, scope, or a single property"),
         ("Card title", "one detail line"), ("Card title", "one detail line"),
         ("Card title", "one detail line"),
         ("Highlighted card", "the ONE card that deserves the accent outline"),
         ("Card title", "one detail line")]
for i, (name, detail) in enumerate(cards):
    x, y = MX + (i % 3) * 4.14, 1.6 + (i // 3) * 2.1
    hot = i == 4
    d.card(s, x, y, 3.85, 1.85, fill=TINT if hot else PANEL, line=ACC if hot else LINE)
    d.para(s, [[(name, {"bold": True, "size": 15, "color": ACC if hot else INK})],
               [(detail, {"size": 11.5, "color": SUB})]],
           x + 0.2, y + 0.16, 3.45, 1.55, space_after=4)
d.text(s, "One summary line under the grid — or leave the space empty.",
       MX, 5.95, CW, 0.4, size=13.5)

# ---- 5 · PATTERN: two-panel split --------------------------------------------------
s = d.slide()
d.eyebrow(s, "PATTERN · TWO-PANEL SPLIT")
d.title(s, "A taxonomy with exactly two sides — cool left, warm right")
d.card(s, MX, 1.55, 5.95, 4.35, fill=TINT2, line=TINT2)
d.card(s, 6.78, 1.55, 5.95, 4.35, fill=TINT, line=TINT)
d.text(s, "CATEGORY A — its promise", MX + 0.3, 1.85, 5.4, 0.4, size=15.5, bold=True, color=ACC2)
d.text(s, "CATEGORY B — its promise", 7.08, 1.85, 5.4, 0.4, size=15.5, bold=True, color=ACC)
d.bullets(s, ["member one", "member two", "member three"],
          MX + 0.3, 2.45, 5.4, 3.2, size=13.5, space_after=7)
d.bullets(s, ["member one", "member two", "member three"],
          7.08, 2.45, 5.4, 3.2, size=13.5, space_after=7)
d.text(s, "The rule that connects the two panels — centered and bold.",
       MX, 6.3, CW, 0.45, size=15, bold=True, color=ACC, align="center")

# ---- 6 · PATTERN: diagram + bullets --------------------------------------------------
s = d.slide()
d.eyebrow(s, "PATTERN · DIAGRAM")
d.title(s, "Bullets left, schematic right — one accent element only")
d.lead_bullets(s, [
    ("What the boxes are — ", "explain the diagram in words, left of it"),
    ("The accent rule — ", "exactly one element gets ACC: the thing the eye must land on"),
    ("Placeholders — ", "dashed border + italic gray = 'not filled in yet', visible at a glance"),
], x=MX, y=1.6, w=6.2, h=3.0)
d.text(s, "Punchline about the diagram.", MX, 5.2, 6.2, 0.4, size=14, bold=True, color=ACC)
fx = 7.3
d.box(s, fx, 1.9, 1.5, 0.6, PANEL, "input", text_color=INK)
d.arrow(s, fx + 1.55, 2.2, fx + 1.9, 2.2)
d.box(s, fx + 1.95, 1.9, 1.7, 0.6, "FFFFFF", "core step", text_color=ACC, line=ACC, line_w=1.5)
d.arrow(s, fx + 3.7, 2.2, fx + 4.05, 2.2)
d.box(s, fx + 4.1, 1.9, 1.3, 0.6, PANEL, "output", text_color=INK)
d.arrow(s, fx + 2.8, 2.55, fx + 2.8, 3.1, color=MUT, width=1.25)
d.ellipse(s, fx + 2.3, 3.15, 1.0, 0.55, "888888")
d.text(s, "state", fx + 2.3, 3.15, 1.0, 0.55, size=10, color="FFFFFF", align="center",
       valign="middle", space_after=0)
d.arrow(s, fx + 2.25, 3.35, fx + 0.75, 2.55, color=MUT, width=1.25, dash=True)
d.text(s, "feedback path — dashed", fx + 0.3, 3.6, 2.4, 0.3, size=9.5, italic=True, color=MUT)
d.card(s, fx, 4.35, 5.4, 1.6, fill="FFFFFF", line=LINE, dash=True)
d.text(s, "screenshot / render — drop in", fx, 4.35, 5.4, 1.6, size=10.5, italic=True,
       color=MUT, align="center", valign="middle", space_after=0)

# ---- 7 · PATTERN: code panel + QR close ------------------------------------------------
s = d.slide()
d.eyebrow(s, "PATTERN · CLOSE")
d.title(s, "Close — QR left, code right, thanks centered")
d.text(s, "WHERE TO GO NEXT", MX, 1.62, 3.6, 0.4, size=13, bold=True)
d.qr(s, "https://github.com/sgl-project/sglang", 0.95, 2.1, 2.15,
     caption="github.com/sgl-project/sglang")
carbon = HERE / "assets" / "carbon-snippet.png"
if carbon.exists():   # light carbon code card (built by scripts/carbonize.py); falls back to code_panel offline
    d.image(s, carbon, 8.35, 1.7, w=4.38)
else:
    d.code_panel(s, "pip install <your-package>\n\n<your-tool> run \\\n  --config config.yaml \\\n  --flag value",
                 8.35, 1.7, 4.38, 2.3)
d.rich(s, [("repo → path/to/entrypoint\n", {"bold": True, "size": 12.5, "br": True}),
           ("credits · acknowledgements · contact", {"size": 11.5, "color": SUB})],
       8.35, 4.25, 4.38, 0.8, space_after=4)
d.text(s, "Thank you — Speaker Name · RadixArk", 0, 6.35, W, 0.5, size=15, bold=True, align="center")

d.save(HERE / "example-deck.pptx")
