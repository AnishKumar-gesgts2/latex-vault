# LaTeX Vault in Obsidian

This repository is an Obsidian vault containing the multivariable-calculus work and physics/movement quiz materials. The `.tex` files are the editable source; the TikZ diagrams are part of the source and can be revised directly.

## Export to PDF

1. Install a LaTeX distribution such as MiKTeX or TeX Live, and make sure `pdflatex` is available.
2. In Obsidian, open `C:\Users\notso\Documents\Latex Vault`.
3. Use the command palette (`Ctrl+P`) and run **LaTeX: Build current file**, or run **LaTeX: Choose file to build** to select any `.tex` file in the vault.
4. The resulting PDF is written beside its source file. Run the command again if you later add cross-references.

The vault's **LaTeX Builder** plugin uses `pdflatex` by default. You can change the compiler and arguments in **Settings → Community plugins → LaTeX Builder**.

## GitHub sync

Use the command palette commands from the **Git Sync** plugin:

- **Git: Pull latest vault changes** pulls fast-forward-only updates from `origin/main`.
- **Git: Commit and push vault changes** stages all changes, creates a dated commit, and pushes to `origin/main`.
