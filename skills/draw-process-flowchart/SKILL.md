---
name: draw-process-flowchart
description: Create, revise, and QA publication-ready process flowcharts in a coherent Chinese journal-style visual system with configurable stage count, horizontal or vertical layouts, colored headers, aligned separators, filled process arrows, line icons, Microsoft YaHei typography, and PNG/SVG/PDF export. Use when a user asks to draw, redesign, standardize, or embed a process, evidence chain, decision framework, implementation workflow, or similar paper figure; the subject matter and number of stages can vary.
---

# Process flowchart

Use this skill to turn any ordered process, decision framework, evidence chain, or implementation workflow into a clear, publication-ready flowchart. The supplied reference image is a style reference, not a fixed four-column template: choose the number of stages and the orientation from the content.

## Workflow

### 1. Define the semantic contract

List the actual stages before drawing. Use two to six stages by default; split a stage only when it has a distinct decision, owner, input/output, or evidence type. Merge stages when adjacent boxes would contain repetitive wording.

Choose the reading direction:

- use a horizontal sequence for 2–6 compact stages and wide pages;
- use a vertical sequence for long labels, many stages, or narrow portrait pages;
- use a two-dimensional matrix only when two independent dimensions are analytically necessary.

Write the main sequence in one line, for example:

`输入/观察 → 分析/设计 → 执行/交付 → 反馈/复核`

Add an optional secondary implementation band only when it adds a distinct handoff or lifecycle. Align its labels to the corresponding main stages; do not repeat the main-panel text.

Define one question for each stage:

- What evidence or input starts the process?
- What analysis, verification, or classification happens next?
- What options, actions, or decisions follow?
- How is implementation, delivery, feedback, or review closed?

Preserve the user’s terminology and causal logic. Do not invent statistics, standards, costs, or causal claims to fill empty space.

### 2. Structure the content

Use two to four short content groups per stage. Each group has:

1. a short colored label (bold);
2. one concise explanation line;
3. a light dashed separator below the group when another group follows.

Keep all stages in the same internal structure unless the user explicitly requests a matrix, card, or comparison layout. Do not give one stage extra inner cards merely because it contains multiple options; use text hierarchy and separators first.

Keep explanatory notes short and muted. Put definitions, sample boundaries, or caveats in the note line rather than in the primary labels. Keep figure titles and captions in the manuscript when the document already supplies them; do not duplicate them inside the image.

### 3. Apply the visual system

Read [references/style-spec.md](references/style-spec.md) for the exact tokens and adaptation rules. The reference style uses:

- white background, equal stage modules, thin gray outer borders;
- a deep navy → teal → green palette, extended by light tints when more stages are needed;
- dark filled arrows between stages;
- one small white line icon per stage, selected to match the stage meaning;
- no gradients, shadows, hatch fills, clip-art mixtures, or decorative loops.

Use a real Microsoft YaHei file whenever the user requests Microsoft YaHei. Register regular and bold font files explicitly with Matplotlib `FontProperties(fname=...)`; do not rely on family-name lookup or synthetic bold. Verify the font in the exported SVG and report a font issue rather than silently substituting another CJK font.

Use bold typography for headers, group labels, primary explanations, action text, and lifecycle labels. Use regular or muted text only for secondary notes. Keep hierarchy visible through size, color, and whitespace rather than adding unnecessary borders.

### 4. Draw deterministically

Prefer a reproducible Matplotlib/SVG workflow. Start from [scripts/draw_flowchart_template.py](scripts/draw_flowchart_template.py), set `orientation` and `stages`, and replace the example labels with the user’s content. Keep helpers separate for:

- stage geometry and header bands;
- header line icons;
- aligned separators;
- filled polygon arrows;
- optional lifecycle/implementation band;
- multi-format export.

For a four-stage horizontal layout, use the reference geometry in [references/style-spec.md](references/style-spec.md). For other stage counts, calculate equal module widths and use the same outer margins, gap widths, header height, and content baselines wherever the labels fit. Shorten wording before shrinking typography.

Export at least 300 dpi PNG plus editable SVG and PDF. Set `svg.fonttype = "none"` so text remains searchable/editable when possible. Embed the PNG or PDF in the manuscript only after inspecting the standalone figure.

### 5. QA before delivery

Inspect the standalone figure at 100% and then inspect the rendered manuscript pages. Confirm all of the following:

- the chosen stage count and reading direction are obvious;
- headers share a consistent baseline and height within the chosen layout;
- text groups are vertically centered in their allotted regions;
- dashed separators use one dash pattern, line width, color, inset, and balanced gaps;
- all stages use the same internal-card policy;
- filled arrows sit in the gaps, do not touch borders, and point in the intended direction;
- optional bottom labels align to their parent stages and are large enough;
- icons share stroke width, color, scale, and optical alignment;
- no text touches a colored header, separator, outer border, or output bar;
- no label wraps or clips after manuscript scaling;
- the figure number/caption sequence is unchanged after embedding;
- the exported SVG contains Microsoft YaHei regular/bold rather than an unintended fallback.

For DOCX delivery, use the document-rendering skill’s render → inspect-every-page loop. Re-render after every geometry or font change. Preserve the original manuscript and write the revised file to a new output path.

## Visual example

The bundled image at [assets/research-evidence-flow.png](assets/research-evidence-flow.png) is a reconstructed five-stage research evidence-chain example. It is synthetic demonstration content, not a user-supplied figure or project data.

## Invocation examples

- “Use `$draw-process-flowchart` to turn this research method into a five-stage journal figure.”
- “Use `$draw-process-flowchart` to redesign this workflow vertically with the same colors, arrows, icons, and Microsoft YaHei typography.”
- “Use `$draw-process-flowchart` to standardize this two-stage comparison diagram and export PNG/SVG/PDF.”
