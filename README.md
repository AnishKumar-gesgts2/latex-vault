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
| 14 | [LaTeX](Multi%20Chapter%2014/Chapter_14_Solutions.tex) | [PDF](Multi%20Chapter%2014/Chapter_14_Solutions.pdf) | 103/108; missing source prompts below |
| 15 | [LaTeX](Multi%20Chapter%2015/Chapter_15_Solutions.tex) | [PDF](Multi%20Chapter%2015/Chapter_15_Solutions.pdf) | 111/111 |
| 16 | [LaTeX](Multi%20Chapter%2016/Chapter_16_Solutions.tex) | [PDF](Multi%20Chapter%2016/Chapter_16_Solutions.pdf) | 89/89 |

The exact selection is recorded in `assignment_manifest.json`. There are no duplicate or extra exercise labels. Total available coverage is 436 of 441 assignments.

### Missing source prompts

- Section 14.3, Exercises 103 and 104: the uploaded ninth-edition section ends at Exercise 101.
- Section 14.8, Exercises 17, 19, and 21: these refer to Section 4.7, Exercises 3, 7, and 25, respectively. Chapter 4 is not included in this multivariable volume.

These five are explicitly listed at the end of the Chapter 14 PDF. They have not been replaced with guessed questions. Diagram-based estimates are identified as approximate within the solutions.

### Textbook and Git LFS

`Multi Textbook/*.pdf` is tracked through Git LFS. Install Git LFS before cloning or pulling this repository, then run `git lfs pull` if the textbook initially appears as a short pointer file. The uploaded textbook was verified by downloading its LFS object in a separate checkout and comparing its SHA-256 hash with the local PDF.

Build a chapter with `pdflatex` twice to update its table of contents. Build intermediates are ignored; editable sources and compiled PDFs are kept in the repository.
