# AQT submission source

`main.tex` contains the complete *Advanced Quantum Technologies* manuscript, the consolidated reference list, and the Supporting Information in one file. It uses the Wiley/AQT `USG` class from the journal template supplied for this submission.

Figures are reused directly from `../manuscript/figures/`.

To compile, place the non-font support files from the supplied Wiley template next to `main.tex` (`USG.cls`, `lettersp.sty`, `NJDnatbib.sty`, the Wiley logo, and the ORCID logo in `images/`), then run `pdflatex` three times. Template font files are not redistributed in this repository.

References begin after an explicit `\clearpage`; Supporting Information follows the references in the same PDF with `S`-prefixed section, figure, table, and equation numbering.
