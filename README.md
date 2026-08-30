# Movement Lab quizzes in Obsidian

Open `movement_lab_version_a.tex` or `movement_lab_version_b.tex` in Obsidian using a text editor or a LaTeX plugin. The `.tex` files are the editable source; the TikZ diagrams are part of the source and can be revised directly.

## Export to PDF

1. Install a LaTeX distribution such as MiKTeX or TeX Live, and make sure `pdflatex` is available.
2. In Obsidian, open the vault containing `C:\Users\notso\Documents\Latex`.
3. Open the desired `.tex` file and run `pdflatex movement_lab_version_a.tex` (or the Version B filename) from a terminal opened in that folder. Run it twice if you later add cross-references.
4. The resulting PDF will be in the same folder. Open it in Obsidian or attach/embed it in a note.

If using the Obsidian community plugin **Obsidian LaTeX Suite**, enable its compile command and select the `.tex` file; it will compile the same source and place the PDF beside it.
