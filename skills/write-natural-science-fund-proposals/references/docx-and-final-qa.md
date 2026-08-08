# DOCX And Final QA

## File Handling

- Use the newest user-adjusted DOCX as the base.
- Preserve the source and save a versioned output.
- Keep unrelated user edits and formatting.
- Use deterministic OOXML or python-docx edits for repeated formatting changes.

## Reference PDFs

- Run `~/.local/bin/pdf2md-auto convert <reference.pdf>` before substantive reading.
- Read the generated `.pdf.md` first.
- Inspect the original PDF only for figures, tables, fonts, and page layout.

## Required Formatting

- Superscript numeric in-text citations such as `[10,15-21]`.
- Keep bibliography numbers and `[J]`, `[M]`, `[P]` at baseline.
- Bold the applicant's Chinese and English name in achievements.
- Put `6.1.7 知识产权与设备方法基础。` on a separate bold paragraph.
- Start `围绕建筑环境感知、人员行为记录、建筑性能评价和运行调控……` in the next paragraph.
- Use figure captions consistent with the drawing skill: centered, HuaWen Songti/STSong 11 pt regular; Latin in Times New Roman.

## Forbidden Submission Language

Remove all internal process wording, including:

- `国家基金本子`
- `参考国家基金`
- `参考已有文件`
- `沿用已有本子`
- `根据修改指令`
- `需填`, `待补`, `待核实`

Search headers, footers, text boxes, tables, captions, and body paragraphs.

## Figure-Text Audit

- Confirm every figure matches the surrounding正文.
- Confirm every figure number and caption is referenced correctly.
- Rebuild all affected figures when core wording changes.
- Keep content, method, scientific-question, outcome, and application wording synchronized.
- Keep the technical route free of annual-plan language.

## Render Audit

1. Render the entire DOCX to page PNGs.
2. Inspect all pages and figure pages at full resolution.
3. Check missing glyphs, overlap, clipping, paragraph spacing, page breaks, orphan headings, and one-character final lines.
4. Fix and rerender until clean.

LibreOffice may omit unsupported Chinese fonts during QA. If this occurs, verify OOXML font properties and distinguish renderer substitution from missing document text.

## Package And Structure Audit

- Confirm the DOCX ZIP package has no errors.
- Confirm no tracked insertions/deletions or reviewer comments remain unless requested.
- Confirm expected figure count and embedded-image hashes.
- Confirm no forbidden phrases or unresolved placeholders.
- Confirm achievements, software-copyright count, sensor list, and bibliography claims.

Run `scripts/audit_proposal_docx.py` before delivery, then perform visual QA because structural checks cannot detect line wrapping or page-layout defects.
