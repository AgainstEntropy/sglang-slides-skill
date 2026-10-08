# sglang-slides-skill — RadixArk/SGLang house-style presentations

A skill for generating RadixArk-style PPTX decks in Python (uv + python-pptx)
and editing existing Google Slides presentations directly:
design system + helper library + brand assets + native editing workflow.

**Start here: [`SKILL.md`](SKILL.md)** (the skill instructions, with the API cheat sheet and the hard rules).

| File | Contents |
|---|---|
| [`SKILL.md`](SKILL.md) | The skill itself: workflow, API cheat sheet, hard rules |
| [`references/google-slides.md`](references/google-slides.md) | Native Google Slides editing: preserve scope, reuse styles, handle media, verify changes |
| [`design-system.md`](design-system.md) | Design system: canvas/grid, colors, type scale, the 9 layout patterns, QA process, asset registry |
| [`sgl_deck.py`](sgl_deck.py) | python-pptx helper library (tokens are constants; `Deck` class + all helpers) |
| [`examples/make_example.py`](examples/make_example.py) | Script that builds the placeholder example deck (just `uv run` it) |
| `examples/example-deck.pptx` | **Placeholder example deck**: one slide per pattern — flip through it before starting a new deck |
| `examples/example-deck.pdf` | The same deck as PDF — regenerate with `soffice --headless --convert-to pdf example-deck.pptx` |
| `assets/` | sglang logo (wide and square), sgl-diffusion logo |
| [`scripts/make_qr.py`](scripts/make_qr.py) | URL → brand-colored QR png |

The style tokens were reverse-engineered from the official RDXA deck
(`~/RDXA/Slides/sglang-happyhour-7min.pptx`).
First real use case: [`../sglang-diffusion/talks/amazon/pptx-src/build.py`](../sglang-diffusion/talks/amazon/pptx-src/build.py)
(a 14-slide Amazon Robotics Lab talk).

## Google Slides editing

Provide the presentation link, the pages to change, and any reference page whose
style should be reused. The agent reads the live deck, edits native objects, and
checks the result in the same presentation. There is no PPTX upload round trip.

This is a workflow extension, not a Google API client or authentication service.
Your agent environment must provide an authorized Google Slides/Drive connector
or equivalent native API access. Supported browser controls can supplement API
operations that do not expose a needed visual adjustment. Without access, the
agent reports the missing capability instead of silently substituting a PPTX.
Video uploads also require Drive access; sharing the deck does not by itself
establish access to separately stored video files.

The existing `sgl_deck.py` API and PPTX build workflow are unchanged.

## Register as a Claude Code skill (optional)

```bash
ln -s "$(pwd)" ~/.claude/skills/sglang-slides
```

To publish it to the company skill marketplace, go through `rdxa-skills`' `/add-rdxa-skill` flow.
