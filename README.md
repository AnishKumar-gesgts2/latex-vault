# LaTeX Vault in Obsidian

This repository is an Obsidian vault containing physics/movement quiz materials, the FRC shoot-on-the-move theory proof, and a multivariable-calculus textbook reference. The `.tex` files are the editable source; the TikZ diagrams are part of the source and can be revised directly.

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

## Shoot-on-the-move theory proof

[SOTM Theory Proof](SOTM%20Theory%20Proof/SOTM%20Theory%20Proof.pdf) is the compiled shoot-on-the-move (SOTM) derivation for FRC. Its LaTeX source is in the Second Brain under `Coding Output/Latex/SOTM-Documentation`.

The multivariable-calculus homework (Chapters 13–15) was removed from this vault on 2026-11-27. It is archived outside the vault in `Documents/Latex Vault Archive - Multivariable HW 2026-11-27` and remains in this repository's Git history.

### Textbook and Git LFS

`Multi Textbook/*.pdf` is tracked through Git LFS. Install Git LFS before cloning or pulling this repository, then run `git lfs pull` if the textbook initially appears as a short pointer file. The uploaded textbook was verified by downloading its LFS object in a separate checkout and comparing its SHA-256 hash with the local PDF.

Build a document with `pdflatex` twice to update its table of contents. Build intermediates are ignored; editable sources and compiled PDFs are kept in the repository.
