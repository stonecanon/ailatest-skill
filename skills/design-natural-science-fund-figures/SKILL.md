---
name: design-natural-science-fund-figures
description: Design, revise, standardize, and insert figures for Chinese natural science fund proposals, especially technical route diagrams, research-content logic diagrams, data-flow diagrams, active-observation loops, evaluation charts, and research-background figures. Use when Codex must create or update SVG/PNG figures, synchronize figures with a Chinese grant proposal or DOCX, match the user's established fund-proposal visual style, or audit figure-text consistency, colors, typography, arrows, shadows, and Word captions.
---

# Design Natural Science Fund Figures

Create proposal figures as compact scientific arguments, not decorative infographics. Treat the latest proposal text as the source of truth and preserve the user's established visual language.

## Core Workflow

1. Identify the latest editable DOCX and all reference PDF/DOCX files. Never assume an older output is current.
2. Extract the proposal's title, scientific questions, research contents, methods, outcomes, and final application statement.
3. Build a content map before drawing. Keep every figure label traceable to proposal text.
4. Select a figure architecture from [references/figure-patterns.md](references/figure-patterns.md).
5. Apply the exact visual system in [references/visual-system.md](references/visual-system.md).
6. Author SVG as the primary editable source. Export a 2x PNG preview for Word compatibility.
7. Insert or replace the figure in the latest DOCX without disturbing unrelated formatting.
8. Render the entire DOCX and inspect every page. Follow [references/word-and-qa.md](references/word-and-qa.md).
9. Run `scripts/audit_svg_style.py` on all final SVG files and resolve errors before delivery.

## Content Contract

- Use exactly three research-content blocks unless the proposal itself has changed and the user explicitly approves another count.
- Use exactly two scientific questions for a small natural-science-fund project.
- State research content as what will be studied. Put sensors, algorithms, software, and detailed tools in the method layer.
- Keep research content, research scheme, limitations, scientific questions, outcomes, and figures one-to-one and internally consistent.
- Keep annual plans out of the technical route diagram.
- Write the final application or service target as one concise sentence.
- Keep the technical route distinct from the research-content relationship figure. Do not duplicate the same composition twice.
- Use real experimental-platform, site, route, or matching-result images when they clarify evidence. Do not replace inspectable evidence with generic decoration.

## Layout Contract

- Use a white background and no black outer frame.
- Prefer a taller, compact page-filling composition over an excessively wide diagram.
- Make major headings larger than section headings, and section headings larger than detail text.
- Fill shapes with text appropriately; compress boxes instead of leaving large empty areas.
- Keep same-level shapes the same color and size treatment.
- Center and mirror paired connectors. Make connectors touch shape borders without gaps or overlaps.
- Use short arrows with restrained arrowheads. Avoid oversized arrows and long empty shafts.
- Use exact circles for circular processes. Add readable x- and y-axis titles to charts.
- Avoid nested-card clutter, redundant icons, and icons that are visually indistinguishable.

## Typography Contract

- Use Microsoft YaHei for all text inside figures.
- Use bold weight for titles, section headers, scientific questions, outcomes, and core content.
- Restrict figure text colors to black or white.
- Use HuaWen Songti/STSong-style Chinese captions in Word at 11 pt, regular weight, centered; use Times New Roman for Latin text and numerals.
- Keep labels readable at the final Word width, not merely at SVG editing scale.

## Deliverables

- Deliver SVG as the editable master.
- Produce a 2x PNG preview for DOCX insertion.
- When the request includes Word, deliver a new versioned DOCX rather than overwriting the user's source.
- Keep temporary renders and contact sheets as internal QA artifacts unless the user requests them.

## Bundled example

See [assets/figure-workflow.png](assets/figure-workflow.png) for a reconstructed example of the figure-design workflow. The example is synthetic and does not use a user-supplied figure.

## Resources

- Read [references/visual-system.md](references/visual-system.md) for exact colors, shadows, borders, typography, and arrow rules.
- Read [references/figure-patterns.md](references/figure-patterns.md) for the five recurring proposal-figure architectures.
- Read [references/word-and-qa.md](references/word-and-qa.md) before inserting figures into DOCX or delivering final files.
- Run `python scripts/audit_svg_style.py figure1.svg figure2.svg ...` for deterministic SVG checks.
