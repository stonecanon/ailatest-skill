# Configurable process-flowchart style specification

Use this reference for the visual system. The reference image is a four-stage horizontal example; adapt the same rules for two to six stages or a vertical layout.

## Layout selection

- Horizontal: 2–6 stages, short labels, landscape or wide manuscript column.
- Vertical: 2–6 stages, long labels, portrait page, or narrow column.
- Matrix: only when two independent dimensions must be compared; do not use it merely to fit more text.

Keep equal stage widths when the reading direction is horizontal. For a vertical layout, keep equal stage heights and a shared left text edge. Keep the arrow gap visibly separate from module borders.

## Reference four-stage geometry

Coordinate system: Matplotlib data coordinates on a `15.8 × 6.9` canvas.

```text
panel_x   = [0.42, 4.30, 8.18, 12.06]
panel_w   = 3.32
panel_y   = 1.30
panel_h   = 5.03
header_h  = 0.63
bottom_y  = 0.70
bottom_h  = 0.72
```

For `n` horizontal stages, calculate:

```python
outer_left, outer_right = 0.42, 15.38
gap = 0.56
panel_w = (outer_right - outer_left - gap * (n - 1)) / n
panel_x = [outer_left + i * (panel_w + gap) for i in range(n)]
```

Reduce the gap only when necessary to keep the stage text readable; never let arrows touch the borders.

## Colors

Use these four reference colors in order. For more stages, interpolate lighter tints within the same hue families instead of introducing unrelated saturated colors.

```python
HEADER = ["#34495E", "#2B7F97", "#4E8667", "#6E9655"]
BLACK = "#20262D"
MUTED = "#66717C"
BORDER = "#59636C"
RULE = "#AEB6BD"
LIGHT_RULE = "#D7DCE0"
```

Use the stage header color for that stage’s group labels. Use the first deep-navy color for the final output bar and process arrows unless the user supplies a different palette.

## Typography

Register actual font files before drawing:

```python
regular_props = FontProperties(fname="/path/to/MicrosoftYaHei-v11.3.ttc")
bold_props = FontProperties(fname="/path/to/MicrosoftYaHei-Bold-v11.3.ttc")
```

Suggested sizes for the reference canvas:

| Element | Size | Weight |
|---|---:|---|
| Header title | 18 pt | bold |
| Group label | 15 pt | bold |
| Main explanation | 12 pt | bold |
| Muted note | 10.6–11.2 pt | regular |
| Lifecycle label | 14.6 pt | bold |

For more stages or a smaller final footprint, shorten labels first. Use the smallest body text only after checking that the figure remains legible at the manuscript’s final scale.

## Separators and arrows

For the reference horizontal layout, use shared content baselines:

```text
group_labels = [5.34, 4.26, 3.16]
group_body   = [5.00, 3.92, 2.82]
dividers     = [4.62, 3.53, 2.44]
```

For other stage counts, divide the content region into equal-height bands and keep the same relationship: title, explanation, whitespace, then separator. Do not place a separator through a colored output bar.

Use one dash pattern everywhere:

```python
ax.plot([x0, x1], [y, y], color=RULE, lw=0.9,
        linestyle=(0, (4, 3)), dash_capstyle="butt")
```

Use a filled polygon for arrows rather than a thin annotation arrow. A compact horizontal arrow should have a rectangular tail and triangular head; a vertical arrow should use the same proportions rotated 90 degrees.

## Icons

Draw icons as simple vector strokes, all in white inside the colored header. Select icons that express the stage meaning, not generic decoration. Suitable examples include search/evidence, layers/structure, path/action, checklist/feedback, database/input, analysis, decision, delivery, and review.

Keep icon stroke widths around `1.7` data-scaled points, use the same optical size, and align icons to a shared header position. Do not mix emoji, filled clip art, and thin line icons.

## Content constraints

- Use two to four groups per stage.
- Keep each group to one label and one explanation line whenever possible.
- Apply the same internal-card policy to every stage.
- Use a bottom band only for a distinct handoff/lifecycle sequence.
- Keep captions and figure numbers in the manuscript, not duplicated inside the image.
