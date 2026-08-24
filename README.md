# sglang-slides-skill — a skill for building RadixArk/SGLang house-style pptx decks

A complete skill for generating RadixArk-style talk decks in Python (uv + python-pptx):
design system + helper library + brand assets + a placeholder example deck with one slide per pattern.

**Start here: [`SKILL.md`](SKILL.md)** (the skill instructions, with the API cheat sheet and the hard rules).

| File | Contents |
|---|---|
| [`SKILL.md`](SKILL.md) | The skill itself: workflow, API cheat sheet, hard rules |
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

## Register as a Claude Code skill (optional)

```bash
ln -s "$(pwd)" ~/.claude/skills/sglang-slides
```

To publish it to the company skill marketplace, go through `rdxa-skills`' `/add-rdxa-skill` flow.
