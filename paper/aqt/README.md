# AQT submission source

`main.tex` contains the complete *Advanced Quantum Technologies* manuscript, the consolidated reference list, and the Supporting Information in one file.

The Wiley template support files needed for compilation are stored in `template_support.zip`. No font files are redistributed in this repository package. Figures are reused from `../manuscript/figures/`.

## Build

```bash
cd paper/aqt
unzip -o template_support.zip
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The manuscript uses the Wiley `USG` class from the supplied AQT template. References begin after an explicit `\clearpage`; Supporting Information follows the references in the same PDF with `S`-prefixed section, figure, table, and equation numbering.
