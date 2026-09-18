# LaTeX Vault in Obsidian

This repository is an Obsidian vault containing the multivariable-calculus work and physics/movement quiz materials. The `.tex` files are the editable source; the TikZ diagrams are part of the source and can be revised directly.

## Export to PDF

1. Install a LaTeX distribution such as MiKTeX or TeX Live, and make sure `pdflatex` is available.
2. In Obsidian, open `C:\Users\notso\Documents\Latex Vault`.
3. Use the command palette (`Ctrl+P`) and run **LaTeX: Build current file**, or run **LaTeX: Choose file to build** to select any `.tex` file in the vault.
4. The resulting PDF is written beside its source file. Run the command again if you later add cross-references.

The vault's **LaTeX Builder** plugin uses `pdflatex` by default. You can change the compiler and arguments in **Settings â†’ Community plugins â†’ LaTeX Builder**.

## GitHub sync

Use the command palette commands from the **Git Sync** plugin:

- **Git: Pull latest vault changes** pulls fast-forward-only updates from `origin/main`.
- **Git: Commit and push vault changes** stages all changes, creates a dated commit, and pushes to `origin/main`.

## Assigned calculus solutions

Each chapter has one self-contained LaTeX source and a compiled PDF. Exercise and subpart labels follow the assignment screenshot. Graphs use editable TikZ/PGFPlots.

| Chapter | Source | PDF | Coverage |
|---|---|---|---|
| 12 | [LaTeX](Multi%20Chapter%2012/Chapter_12_Solutions.tex) | [PDF](Multi%20Chapter%2012/Chapter_12_Solutions.pdf) | 87/87 |
| 13 | [LaTeX](Multi%20Chapter%2013/Chapter_13_Solutions.tex) | [PDF](Multi%20Chapter%2013/Chapter_13_Solutions.pdf) | 46/46 |
| 14 | [LaTeX](Multi%20Chapter%2014/Chapter_14_Solutions.tex) | [PDF](Multi%20Chapter%2014/Chapter_14_Solutions.pdf) | 106/107; Question 104 needs its prompt |
| 15 | [LaTeX](Multi%20Chapter%2015/Chapter_15_Solutions.tex) | [PDF](Multi%20Chapter%2015/Chapter_15_Solutions.pdf) | 111/111 |
| 16 | [LaTeX](Multi%20Chapter%2016/Chapter_16_Solutions.tex) | [PDF](Multi%20Chapter%2016/Chapter_16_Solutions.pdf) | 89/89 |

The exact selection is recorded in `assignment_manifest.json`. There are no duplicate or extra exercise labels. Total available coverage is 439 of 440 assignments.

### Missing source prompts

- Section 14.3, Question 104: the uploaded ninth-edition section ends at Question 101. Question 103 has been removed at the user's request.
- Section 14.8, Questions 17, 19, and 21 now solve Section 14.7, Questions 3, 7, and 25 as requested. The printed textbook says Section 4.7. The substituted problems are unconstrained, so the solutions explain why Lagrange multipliers do not apply and use full critical-point classification instead.

Each lesson starts on a new page with a bold lesson heading; questions use their simple numbers within that lesson. Diagram-based estimates remain identified as approximate.

### Textbook and Git LFS

`Multi Textbook/*.pdf` is tracked through Git LFS. Install Git LFS before cloning or pulling this repository, then run `git lfs pull` if the textbook initially appears as a short pointer file. The uploaded textbook was verified by downloading its LFS object in a separate checkout and comparing its SHA-256 hash with the local PDF.

Build a chapter with `pdflatex` twice to update its table of contents. Build intermediates are ignored; editable sources and compiled PDFs are kept in the repository.
