---
name: write-natural-science-fund-proposals
description: Draft, revise, and finalize Chinese natural science fund proposals in the user's established academic style. Use when Codex must edit a grant DOCX, learn style from a reference fund PDF/DOCX, restructure research rationale, literature review, scientific questions, three research-content blocks, methods, limitations, feasibility, annual plans, expected outcomes, achievements, sensors, citations, or references; synchronize正文 with figures; verify publication and bibliography facts; or perform final logic, formatting, and submission-readiness audits.
---

# Write Natural Science Fund Proposals

Write as a proposal co-author and final editor. Preserve the user's latest document, established terminology, and formal mechanism-oriented voice.

## Core Workflow

1. Locate the newest user-edited DOCX. Treat it as the editing base and preserve it.
2. Identify style references. Convert referenced PDFs to Markdown before substantive reading, then inspect original PDF pages for layout-sensitive details.
3. Extract the proposal title, two scientific questions, three research contents, corresponding methods, limitations, figures, outcomes, annual plan, and achievements.
4. Build a consistency matrix before rewriting. Use [references/consistency-and-facts.md](references/consistency-and-facts.md).
5. Revise surgically in the existing structure. Follow the user's voice in [references/voice-and-structure.md](references/voice-and-structure.md).
6. Verify publications, journals, years, volumes, pages/article numbers, SCI claims, rankings, and cited facts with primary sources.
7. Apply proposal-specific Word formatting and final checks from [references/docx-and-final-qa.md](references/docx-and-final-qa.md).
8. Render the whole DOCX, inspect every page, fix layout defects, and rerender.
9. Run `scripts/audit_proposal_docx.py` and resolve errors before delivery.

## Logic Contract

- Use exactly two scientific questions for this small project.
- Use exactly three major research-content blocks.
- Map each research-content block to one expanded research-scheme block and one corresponding limitation/gap.
- Keep content focused on what is studied; put detailed tools, models, sensor specifications, and procedures in the scheme/method section.
- Keep figures, captions,正文 references, outcomes, and annual tasks consistent with the same three-block logic.
- Keep the annual plan separate from the technical route.
- Keep the final application/service target to one sentence.
- Reconcile every later edit across the full proposal instead of changing one isolated paragraph.

## Writing Contract

- Use formal Chinese academic prose with explicit objects, mechanisms, variables, causal links, evidence, and validation paths.
- Move from limitation or contradiction to the proposed mechanism and then to expected scientific contribution.
- Prefer precise verbs such as `构建`, `表征`, `解析`, `识别`, `量化`, `揭示`, `验证`, and `界定`.
- Use inline numbered logic such as `①②③` when it improves dense proposal prose.
- Avoid marketing language, inflated claims, generic AI phrasing, and decorative headings.
- Never write process language such as `国家基金本子`, `参考已有文件`, `沿用某本子`, or `根据修改指令` in the submission text.
- Avoid a paragraph ending with a last visual line containing only one Chinese character. Fix wording or spacing after rendering.

## Personal Formatting Rules

- Bold `翁建涛` and `Jiantao Weng` in the achievements section.
- Put `6.1.7 知识产权与设备方法基础。` on its own bold line. Start the explanatory paragraph on the next line.
- Format numeric in-text citations such as `[10,15-21]` as superscript. Do not superscript bibliography entries or `[J]`, `[M]`, and `[P]` document-type markers.
- Keep `申请软件著作权2项` consistent across annual plan and expected outcomes.
- Include noise level whenever listing temperature/humidity, CO2, PM2.5, and illuminance environmental sensors.
- Remove unresolved placeholders such as `需填`, `待补`, or bracketed sensor specifications.
- Use the figure-caption and diagram rules from `$design-natural-science-fund-figures` when figures are part of the task.

## Evidence And Integrity

- Never invent citations, DOI values, indexing status, quartiles, TOP status, corresponding-author roles, equipment ranges, or accuracy values.
- Browse current primary sources for time-sensitive bibliographic and ranking claims.
- Prefer publisher pages, Crossref, official journal pages, Web of Science/Clarivate records when accessible, and manufacturer datasheets.
- Mark uncertain facts for verification instead of presenting them as settled.
- Keep quoted source text minimal and paraphrase in the user's voice.

## Deliverables

- Save a new versioned DOCX; do not overwrite the user's source.
- Preserve unrelated formatting and user edits.
- Deliver only the requested final artifact unless the user asks for audit reports or intermediates.

## Bundled example

See [assets/proposal-core-logic.png](assets/proposal-core-logic.png) for a reconstructed diagram of the proposal's argument skeleton: basis/gap → two scientific questions → three research contents and evidence → contribution and application boundary. The example is synthetic and does not use a user-supplied proposal or project data.

## Resources

- Read [references/voice-and-structure.md](references/voice-and-structure.md) before drafting or rewriting正文.
- Read [references/consistency-and-facts.md](references/consistency-and-facts.md) before changing research logic, sensors, achievements, or bibliography claims.
- Read [references/docx-and-final-qa.md](references/docx-and-final-qa.md) before finalizing a DOCX.
- Run `python scripts/audit_proposal_docx.py proposal.docx` for deterministic checks.
