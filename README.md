# LaTeX Vault in Obsidian

This repository is an Obsidian vault containing the multivariable-calculus work and physics/movement quiz materials. The `.tex` files are the editable source; the TikZ diagrams are part of the source and can be revised directly.

## Export to PDF

1. Install a LaTeX distribution such as MiKTeX or TeX Live, and make sure `pdflatex` is available.
2. In Obsidian, open `C:\Users\notso\Documents\Latex Vault`.
3. Use the command palette (`Ctrl+P`) and run **LaTeX: Build current file**, or run **LaTeX: Choose file to build** to select any `.tex` file in the vault.
4. The resulting PDF is written beside its source file. Run the command again if you later add cross-references.

The vault's **LaTeX Builder** plugin uses `pdflatex` by default. You can change the compiler and arguments in **Settings â†’ Community plugins â†’ LaTeX Builder**.

## Research learning notes

The [GBS learning path](GBS%20Learning/Learning%20Path.md) contains twelve Markdown lessons, worked examples, exercises with answer checks, a glossary, a progress tracker, and a proposal-writing workshop. Start with Lesson 00 and use the checkpoints to build toward independently drafting the GBS proposal.

## GitHub sync

Use the command palette commands from the **Git Sync** plugin:

- **Git: Pull latest vault changes** pulls fast-forward-only updates from `origin/main`.
- **Git: Commit and push vault changes** stages all changes, creates a dated commit, and pushes to `origin/main`.

## Assigned calculus solutions

Each chapter has one self-contained LaTeX source and a compiled PDF. Exercise and subpart labels follow the assignment screenshot. Graphs use editable TikZ/PGFPlots.

| Chapter | Source | PDF | Coverage |
|---|---|---|---|
| 13 | [LaTeX](Multi%20Chapter%2013/Chapter_13_Solutions.tex) | [PDF](Multi%20Chapter%2013/Chapter_13_Solutions.pdf) | 46/46 |


The exact selection is recorded in `assignment_manifest.json`. There are no duplicate or extra exercise labels. 

### Textbook and Git LFS

`Multi Textbook/*.pdf` is tracked through Git LFS. Install Git LFS before cloning or pulling this repository, then run `git lfs pull` if the textbook initially appears as a short pointer file. The uploaded textbook was verified by downloading its LFS object in a separate checkout and comparing its SHA-256 hash with the local PDF.

Build a chapter with `pdflatex` twice to update its table of contents. Build intermediates are ignored; editable sources and compiled PDFs are kept in the repository.
