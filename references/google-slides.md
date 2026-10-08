# Native Google Slides editing

Use this workflow for in-place edits to an existing SGLang/RadixArk presentation.
The live presentation is the source of truth, even when a local PPTX or build
script exists. Do not overwrite newer online edits from a stale local artifact.

## Access and scope

- Discover the environment's authorized Slides read/write and Drive media/export
  tools. Follow an installed Google Slides skill's connector instructions when
  available; tool names and payload wrappers vary between environments.
- Confirm the presentation identity from the user-provided link and a fresh read.
  If access is unavailable, request the normal connection/authorization flow.
  Do not extract credentials or implement an ad hoc OAuth flow in this skill.
- Modify the same presentation unless the user requests a copy. Do not change
  sharing permissions or publish media merely to make embedding easier.
- Resolve the requested pages by title/content, then retain their object IDs.
  Slide numbers are display positions, not stable identifiers. If titles are
  ambiguous, inspect their content or ask before writing.

## Read before editing

1. Read the native presentation, including page size, slide order and IDs,
   elements (including groups), text runs, notes, and skipped-slide state. Keep a
   before snapshot and a compact slide/element inventory in the talk workspace;
   avoid dumping a large presentation JSON into the conversation.
2. Inspect rendered target pages and any user-selected style reference. Read
   native properties as well: screenshots alone do not capture text runs,
   editable structure, theme inheritance, or speaker notes.
3. Map the requested change to objects to keep, modify, add, or remove. Preserve
   unaffected content, notes, media, and slides. Explain substantial replacements
   before making them; a request to restyle a diagram is not a request to rewrite
   its explanation or the whole talk.

## Match the reference, not just its colors

For "use the blocks from this other page", compare fill, outline, corner shape,
padding, typography, alignment, and spacing. Prefer duplicating a suitable native
element using supported tools, then changing its content and placement. Confirm
that duplication preserved the relevant properties and did not carry stale links.

Use the deck's existing visual language, or the house tokens for new content:
`TINT2` / `ACC2` for a pale teal panel and its accent, `TINT` / `ACC` for the warm
counterpart, `PANEL` for neutral grouping. Do not substitute saturated fills when
the selected reference uses pale panels. Keep labels and connectors editable;
do not flatten a simple diagram into a screenshot.

Native editing pitfalls:

- Geometry combines element size and affine transform, including parent-group
  transforms. Do not treat raw width/height as displayed bounds or reset scale to
  one blindly. Convert units explicitly: 72 points/inch, 12,700 EMU/point.
- API-created `ROUND_RECTANGLE` shapes may have visibly different rounding from
  the reference. `updateShapeProperties` does not expose a corner-radius field
  or change `shapeType`. Reuse suitable geometry, or use supported UI controls
  for shape adjustments and inspect the result. Do not invent API properties.
- Keep panel backgrounds behind labels and connectors. Verify z-order after
  creation or duplication, particularly when elements overlap.
- Preserve mixed text styles, bullets, links, and paragraph settings. Avoid
  whole-shape formatting for a partial text change. Use object/range edits;
  use slide-scoped `replaceAllText` only after checking the intended matches.

## Apply bounded native changes

- Prefer native batch updates with explicit field masks over broad replacement.
  Keep each batch coherent and within the tool's supported request schema.
- When available, send `writeControl.requiredRevisionId` from the fresh read.
  On conflict, reread and rebase the intended changes; do not remove the guard
  just to force a stale write. Without revision support, reread targets just
  before writing and acknowledge the remaining concurrent-edit risk.
- For an unknown outcome or timeout, inspect current objects/files before
  retrying creation or upload. Use caller-assigned object IDs when supported
  to make readback unambiguous; do not blindly duplicate a successful operation.
- If the API cannot express an adjustment, use supported browser controls with
  freshly inspected UI state. Never reuse coordinates from another deck/session.
  If neither route supports it, report the limitation instead of claiming success.
- Save the applied requests and before/after snapshots in the talk workspace,
  not this skill repository. JSON snapshots aid comparison but are not a complete
  backup of every editor feature. Use an authorized native copy/version workflow
  when a substantial replacement needs a recoverable original.

## Generation samples and video

- Keep sample provenance: source page, model, and generation settings when known.
  Distinguish a sample actually produced by SGLang-Diffusion from a model vendor's
  showcase. Do not present visual examples as performance measurements.
- Preserve aspect ratio; fit images/videos without stretching or cutting off
  meaningful content. Keep captions separate from the media object.
- Use native video objects for playable samples. If a sample requires a Drive
  upload, use supported authorized upload tools and retain the resulting file ID.
  An arbitrary MP4 URL is not necessarily a supported native video source.
- Check access for the intended audience separately from deck access. Do not
  automatically make a video public. Default to manual playback unless requested
  otherwise; preserve or explicitly choose the intended audio behavior.
- Successful insertion is not proof of playback. Verify in presentation mode
  when possible. Drive processing may be asynchronous: use bounded checks, then
  report pending processing or unverified playback. A PDF poster frame cannot
  establish that the video plays.

## Verify and deliver

1. Read back the presentation. Match objects by ID and check content, slide order,
   notes, skipped state, media references, and the intended edits. Compare
   unaffected slides against the before snapshot; investigate unexpected changes.
   Ignore only identified volatile metadata (for example expiring image-content
   or thumbnail URLs), not source URLs, media IDs, or arbitrary property changes.
2. Render or export the updated native deck and inspect every changed page. For
   structural or deck-wide changes, inspect all pages. Check overflow, overlaps,
   arrows, margins, corner shapes, image crops, and font rendering. Follow stricter
   QA requirements from the active presentation tooling when applicable.
3. Validate interactive media separately. Distinguish structural checks, visual
   checks, and playback checks; if one is unavailable, say so explicitly.
4. Return the same presentation's link, preferably pointing to the changed page,
   plus a brief change summary and any remaining limitations. Use an actual native
   render for a preview, not the old PPTX. Do not claim local build files were
   synchronized unless that was requested and actually done.

Keep private presentation IDs, uploaded samples, credentials, and generated
snapshots out of commits to this reusable skill.

## API references

Consult current schemas rather than guessing fields:

- [Batch updates and revision control](https://developers.google.com/workspace/slides/api/reference/rest/v1/presentations/batchUpdate)
- [Native request types](https://developers.google.com/workspace/slides/api/reference/rest/v1/presentations/request)
- [Shape properties](https://developers.google.com/workspace/slides/api/reference/rest/v1/presentations.pages/shapes)
- [Element transforms](https://developers.google.com/workspace/slides/api/guides/transform)
- [Video properties](https://developers.google.com/workspace/slides/api/reference/rest/v1/presentations.pages/videos)
