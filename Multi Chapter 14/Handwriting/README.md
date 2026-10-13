# Chapter 14 handwriting editing bundle

The current homework is [the latest handwritten PDF](../../output/pdf/Completed%20Multi%20Chapter%2014%20HW%20-%20Right%20Lean%20and%20Reduced%20Vertical%20Variation.pdf). Further edits are expected. Do not treat this cleanup as final approval of the homework.

## What is preserved

- `sources/Original Homework.pdf`: the user's original six pages, including the original graphs and lined-page template. This copy removes the dependency on Downloads.
- `sources/Handwriting Reference.pdf`: the supplied character samples.
- `sources/Lagrange Prompt *.png` and the Lagrange provenance/solutions: the supplied statements and the user's mapping to 14.8 #17, #19, and #21. The provenance's earlier graph-spacing hold is historical; the spaces in `assets/condensed-graph-spaces.json` are current.
- `assets/`: sampled character centerlines, authentic alternate letters and numerals, the two required fonts, layout data, and the variation records needed to rebuild.
- `assets/layout-base.pdf`: an authoring input before the final variation and 14.2 rewrite. It is required for rebuilding; it is not an older finished homework to use or submit.
- `placements.json`: the current generated rows, equations, question tags, page coordinates, and glyph metadata. These describe the rows before per-character displacement; `verification/lean-glyphs.json` records the actual transformations. The original math on pages 1-3 and 5 is in the original PDF rather than this row list.
- `sources/*solutions.json`: earlier mathematical working data, retained as references. The current row content is in `placements.json`; use it to avoid restoring superseded wording or substitutions.
- `verification/`: the latest layout/style checks and selected earlier math audits. Earlier audits do not establish that later work has been rechecked mathematically.
- The existing `../Chapter_14_Solutions.tex`, its typeset PDF, the vault's `assignment_manifest.json`, and the textbook remain in their original locations.

## Rebuild without replacing the current PDF

From the vault root, use a Python environment with the packages in `requirements.txt`:

```powershell
python "Multi Chapter 14/Handwriting/rebuild.py" --verify-current
```

This creates a review copy and regenerated metadata in the ignored `build/` folder. It checks all 31 rendered pages against the current PDF when `--verify-current` is supplied. The existing delivered PDF is never overwritten by the rebuild command. After intentional edits, omit that flag, render the review copy with Poppler, visually inspect every changed page and every affected limit/root/fraction, and only then replace the current PDF and refresh the metadata.

`lean_variation.py` applies the current style to the layout base. `lean_14_2.py` rewrites 14.2 and preserves its graph. `natural_handwriting.py`, `refine_symbols.py`, `handwritten_layout.py`, `fullsize_fractions.py`, and `inspect_long_fractions.py` are the renderer and fraction helpers. The font and character files are already built; historical extraction/build scripts and obsolete PDF stages are unnecessary for this workflow.

For content edits elsewhere, update the relevant row in the layout base and its paired `assets/numerals-placements.json` before rebuilding. Do not change only the metadata: it does not paint the PDF. For page/layout edits, keep page numbers and coordinates in the graph-space and placement files synchronized. The current PDF can also be edited directly, but preserve the matching metadata and do not claim that an earlier base can reproduce a new direct edit until it has been updated and checked.

## Current style and layout requirements

- Body writing is 17 pt; lesson headings are 19 pt. Physical pen width stays 1.5938 pt even for small symbols, exponents, and enlarged red question marks.
- Authentic character alternatives vary between nearby occurrences. Math/variable variation is 1.15 times the earlier uneven version; text variation is 1.4 times it.
- Vertical displacement and vertical warp are reduced to 0.25 of the previous amount. Tilt variation is multiplied by 1.15; right slant uses shear -0.105 about each glyph's center. Horizontal variation remains unchanged.
- Keep the concise original work and prose. Use full expressions rather than invented A/B/C abbreviations. Text x/l/t differ from the variable versions.
- Keep radicals connected with slightly rounded corners and no small flat left lead. Keep relationship and limit arrows short with compact spacing.
- Use stacked fractions. Long numerators and denominators use consecutive notebook lines at normal size; do not squeeze them into one line.
- Do not redraw, restyle, or alter original graphs. Keep all reserved drawing spaces; their positions are in `assets/condensed-graph-spaces.json`.
- Keep each subpart on the page where that subpart starts. A whole question may span pages. New lessons start a new page; avoid excessive gaps between ordinary questions.
- Large red question marks indicate conceptual difficulty, not computational length. Currently they mark 14.3 #101 and 14.7 #41.

The stable output path is listed above. Put temporary renders, comparison boards, and intermediate PDFs in `build/` or the vault's ignored `tmp/`, not among finished exports.

The 2026-10-12 cleanup moved superseded exports and temporary files to `C:\Users\notso\Documents\Codex Artifact Archive\latex-vault-cleanup-2026-10-12` for recovery. This archive is outside the repository and is not required for the verified rebuild. The cleanup and rebuild checks are recorded in `verification/cleanup-report.json` and `verification/rebuild-verification.json`.
