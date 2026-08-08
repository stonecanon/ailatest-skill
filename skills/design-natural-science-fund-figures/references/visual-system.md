# Visual System

## Palette

Use this restrained hierarchy consistently:

| Role | Color | Use |
|---|---|---|
| Primary blue | `#4C689B` | Main headers, content headers, outcomes |
| Deep blue | `#1A4175` | Highest-level title or rare structural emphasis |
| Blue border | `#7E95B7` | Outlines, icons, secondary connectors |
| Pale blue | `#E2E8F0` | Section labels, neutral bands |
| Off-white | `#F7F8FA` | Panel backgrounds |
| Border gray | `#AAB6C6` | Neutral outlines |
| Scientific red | `#D34545` | Scientific questions, uncertainty/risk emphasis |
| Method orange | `#E88925` | Method evidence, organizational logic, limited highlights |
| Pale orange | `#FCEBD7` | Real-image or method-evidence rows |
| Evaluation green | `#5A9D77` | Confidence, calibration, positive performance only |
| Black | `#000000` | All text on light fills |
| White | `#FFFFFF` | All text on dark fills |

Do not introduce additional hue families without a semantic reason. Keep same-level boxes on the same fill.

## Shadows

Use one short lower-right shadow. Never stack near and far shadows or use broad Gaussian glow.

For a viewBox around 1800-2200 px:

```svg
<filter id="figmaShadow" x="-8%" y="-8%" width="120%" height="125%"
        color-interpolation-filters="sRGB">
  <feDropShadow dx="4" dy="5" stdDeviation="1.4"
                flood-color="#374151" flood-opacity="0.28"/>
</filter>
```

Apply the shadow to meaningful boxes and major panels. Keep tiny separators, arrows, internal rules, and icon strokes shadow-free.

## Shapes And Borders

- Use corner radius 6-8 SVG units for ordinary boxes; do not exceed 12 unless the shape is intentionally circular.
- Use 1.5-2 px borders at the master SVG scale.
- Avoid black outlines. Use `#AAB6C6`, `#7E95B7`, or a darker semantic fill color.
- Use white or very light panel fills; do not tint every nested layer.
- Do not use a colored strip on every detail box. Reserve strips for true hierarchy or risk emphasis.

## Typography

Use this font stack inside SVG:

```css
font-family: "Microsoft YaHei", "Microsoft YaHei UI", "微软雅黑",
             "PingFang SC", Arial, sans-serif;
```

- Main title: bold/800, largest size.
- Content or panel title: bold/800.
- Core box label: bold/800.
- Supporting detail: 700 only when needed; never use thin text.
- Text fills: only `#000000` or `#FFFFFF`.
- Letter spacing: `0`.
- Ensure Chinese text remains legible when the figure is placed at 16.37 cm width.

## Arrows And Connectors

- Use one connector language across a figure.
- Use short shafts and small arrowheads.
- Align vertical arrows to exact box centers.
- Mirror left/right branches mathematically.
- End connectors at shape borders. Do not leave floating gaps or run lines through filled boxes.
- Use smooth circular tangent arrows for loops; keep the loop a true circle.
- Avoid decorative curves when orthogonal or direct connectors communicate the relation better.

## Icons And Images

- Use distinct icons for distinct concepts.
- Use the recognizable AutoCAD product mark for AutoCAD drawings.
- Use a building-information-model or building-plus-data-cube icon for BIM/IFC.
- Differentiate topology, semantics, tolerance, floor-plan boundary, and component semantics visually.
- Use real site and platform images when available. Crop them cleanly and preserve inspectable content.
- Do not use purely atmospheric stock imagery.
