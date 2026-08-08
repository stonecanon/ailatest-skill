# Word And QA Workflow

## Source Handling

- Locate the newest user-adjusted DOCX by content and modification time.
- Preserve the source file and write a versioned output.
- Replace only the intended image paragraph and caption formatting.
- Keep figure width near the document's existing usable width; 16.37 cm is the established baseline for this proposal.

## Caption Style

- Center the caption.
- Use Chinese font `华文宋体` or `STSong`, 11 pt, regular weight.
- Use Times New Roman for Latin characters and numerals.
- Keep the figure paragraph with the caption.
- Keep the caption with the following content only when doing so does not create a large blank area.

## Rasterization

- Preserve SVG as the master.
- Export PNG at 2x the SVG viewBox dimensions or equivalent 144 dpi density.
- Confirm transparent or white backgrounds render as intended.
- Avoid screenshots as the editable source.

## Visual QA

1. Render the full DOCX with the document renderer.
2. Inspect every page, then inspect figure pages at full resolution.
3. Check cropping, overlap, tiny text, broken CJK glyphs, shadow clipping, arrow gaps, and caption placement.
4. Compare each embedded image hash with the intended final PNG to detect stale Word media.
5. Verify the DOCX ZIP package, tracked-change state, and comment state.

LibreOffice may fail to display some Chinese body fonts even when OOXML is correct. Distinguish renderer substitution from an actual missing caption by checking DOCX text and run font properties structurally.

## Final Checks

- Five figure captions and five embedded figures when the proposal uses five figures.
- All final SVG text fills are black or white.
- Every SVG includes Microsoft YaHei in the font stack.
- No broad Gaussian blur or dual shadow stack.
- Same-level colors remain consistent.
- Figure text matches proposal text exactly.
- No annual-plan wording appears in the technical route.
