# LaTeX Vault in Obsidian

An Obsidian vault of LaTeX documents. Each `.tex` file is the editable source, and its compiled PDF sits next to it or in a `Quizzes` subfolder.

## Documents

| Document | Source | PDF |
|---|---|---|
| **SOTM Theory Proof**: shoot-on-the-move physics derivation for FRC | [SOTM Theory Proof.tex](SOTM%20Theory%20Proof/SOTM%20Theory%20Proof.tex) | [SOTM Theory Proof.pdf](SOTM%20Theory%20Proof/SOTM%20Theory%20Proof.pdf) |
| **Free Fall Post-Lab Quiz**, version A | [.tex](Free%20Fall%20Post-Lab%20Quiz/free_fall_post_lab_version_a.tex) | [.pdf](Free%20Fall%20Post-Lab%20Quiz/Quizzes/free_fall_post_lab_version_a.pdf) |
| Free Fall Post-Lab Quiz, version B | [.tex](Free%20Fall%20Post-Lab%20Quiz/free_fall_post_lab_version_b.tex) | [.pdf](Free%20Fall%20Post-Lab%20Quiz/Quizzes/free_fall_post_lab_version_b.pdf) |
| Free Fall Post-Lab Quiz, version C | [.tex](Free%20Fall%20Post-Lab%20Quiz/free_fall_post_lab_version_c.tex) | [.pdf](Free%20Fall%20Post-Lab%20Quiz/Quizzes/free_fall_post_lab_version_c.pdf) |
| Free Fall Post-Lab Quiz, version D | [.tex](Free%20Fall%20Post-Lab%20Quiz/free_fall_post_lab_version_d.tex) | [.pdf](Free%20Fall%20Post-Lab%20Quiz/Quizzes/free_fall_post_lab_version_d.pdf) |
| Free Fall Post-Lab Quiz, version E | [.tex](Free%20Fall%20Post-Lab%20Quiz/free_fall_post_lab_version_e.tex) | [.pdf](Free%20Fall%20Post-Lab%20Quiz/Quizzes/free_fall_post_lab_version_e.pdf) |
| **Movement Lab Quiz**, version A | [.tex](Movement%20Lab%20Quiz/movement_lab_version_a.tex) | [.pdf](Movement%20Lab%20Quiz/Quizzes/movement_lab_version_a.pdf) |
| Movement Lab Quiz, version B | [.tex](Movement%20Lab%20Quiz/movement_lab_version_b.tex) | [.pdf](Movement%20Lab%20Quiz/Quizzes/movement_lab_version_b.pdf) |
| Movement Lab Quiz, version C | [.tex](Movement%20Lab%20Quiz/movement_lab_version_c.tex) | [.pdf](Movement%20Lab%20Quiz/Quizzes/movement_lab_version_c.pdf) |

## Export to PDF

1. Install a LaTeX distribution such as MiKTeX or TeX Live, and make sure `pdflatex` is available.
2. In Obsidian, open `C:\Users\notso\Documents\Latex Vault`.
3. Press `Ctrl+P` and run **LaTeX: Build current file**. Alternatively, run **LaTeX: Choose file to build** and pick any `.tex` file.
4. The PDF is written next to its source. Build twice if you add cross-references or a table of contents.

The vault's **LaTeX Builder** plugin uses `pdflatex` by default. You can change the compiler and its arguments under **Settings → Community plugins → LaTeX Builder**.

Build intermediates (`.aux`, `.log` and similar) are ignored by Git. Only sources and compiled PDFs are kept in the repository.

## GitHub sync

Use the **Git Sync** plugin commands from the command palette:

- **Git: Pull latest vault changes**: fast-forward-only pull from `origin/main`.
- **Git: Commit and push vault changes**: stages all changes, makes a dated commit and pushes to `origin/main`.

## Not in this repository

- The multivariable-calculus homework was removed on 2026-11-27. Earlier versions remain in Git history.
- The multivariable-calculus textbook is stored locally in `Documents\Multivariable Calculus Textbook`, outside this repository.
