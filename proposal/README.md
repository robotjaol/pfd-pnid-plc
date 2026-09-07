# Proposal Build

The source follows the structure and two-column conventions of the supplied IEEE conference template. When the official `IEEEtran` package is installed, LaTeX uses it directly. A local article-class fallback preserves a compact two-column preview in reduced TeX environments; it does not replace the official class for conference submission.

```bash
pdflatex openlift-ded-proposal.tex
bibtex openlift-ded-proposal
pdflatex openlift-ded-proposal.tex
pdflatex openlift-ded-proposal.tex
```

Before submission to a venue, install the official IEEE template, confirm the venue page limit and author requirements, and repeat the build.
