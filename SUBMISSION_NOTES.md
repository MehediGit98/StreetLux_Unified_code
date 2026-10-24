# StreetLux submission notes

Manuscript: `manuscript/StreetLux_Unified_Manuscript.docx`

Title: Travel mode and street geometry shape modelled melanopic daylight exposure on a tropical urban route

The paper presents one computational study: seven travel modes and six independent street interventions on a synthetic Dhaka-inspired route, with sequential and symmetric attribution of dose deficits. It contains an unstructured abstract, author–date citations, four tables, four colour figures and three native Word equations.

## Version note

Package version 0.2.1 corrects a solar-azimuth error in `sun.py` that was present in 0.2.0 and changes most reported numbers. The manuscript, tables, figures, saved results and verification records in this package all correspond to 0.2.1. See `CHANGELOG.md`.

## Author information to complete

Complete the author list, affiliations, corresponding email, author contributions, funding and competing-interest statements. Replace the marked declaration paragraph in the manuscript with verified statements. Add ORCID identifiers if required by the selected journal.

The AI-assistance disclosure describes code inspection and correction, numerical checks, writing, reference checks, formatting and figure-script preparation. Review it for accuracy before submission. Figures are deterministic plots and geometric illustrations generated from the code and study inputs.

## Scope of the evidence

Reproduction checks the numerical experiment. The study does not include a field survey, measured commuter exposures, a Radiance comparison, parameter uncertainty analysis, or a physiological outcome study. Preserve these distinctions when adapting the paper to a journal.

## Files for submission

Use the Word paper and this package as its matching reproducibility supplement. Separate figure artwork is in `figures/`. Review the chosen journal's current article category, reference style, artwork specifications and declaration requirements before uploading. No journal acceptance or submission status is implied.

## Editing the study

Edit `manuscript.md` and rebuild with `authoring/build_manuscript.py` for textual revisions. If inputs or numerical settings change, rerun the experiment and review every narrative result and interpretation alongside the computed tables. Complete the project licence before public release, while retaining the reference-data attribution and applicable data-owner terms.
