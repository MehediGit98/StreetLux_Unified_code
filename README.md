# StreetLux reproducibility package

Paper: **Travel mode and street geometry shape modelled melanopic daylight exposure on a tropical urban route**

This package supports one computational study of seven travel modes, six independent street interventions, and the attribution of dose deficits to duration and exposure rate. It contains the complete model, study inputs, results, four figures, four manuscript tables and editable Word-manuscript source. The numerical model version is 0.2.1; see `CHANGELOG.md` for the correction that distinguishes it from 0.2.0.

## Run on Windows PowerShell

Extract the ZIP and open PowerShell inside `StreetLux_Unified_Code`. Python 3.12 is the tested interpreter family.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe verify.py
.\.venv\Scripts\python.exe reproduce.py
```

## Run on Linux or macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python verify.py
.venv/bin/python reproduce.py
```

The runner writes fresh outputs to `reproduced/`. It checks all 3367 numerical fields in `modes.json` and `designs.json` against `results/`, using relative tolerance 1e-9 and absolute tolerance 1e-8. Runtime and local environment paths are excluded from the comparison. It also exports and checks six rows of sequential and symmetric decomposition data and redraws four figures as 300 dpi PNG, vector SVG and PDF. `verify.py` runs eleven regression checks, including solar-position tests against an independent implementation and canyon-geometry checks.

Retain `results/` as the study's reference results. To explore intentional parameter changes, edit the declared inputs and run `python reproduce.py --out exploratory_run --skip-comparison`. The decomposition export requires a positive dose deficit from walking for every comparison mode, as assumed by Table 3. Any revised experiment requires a review of the manuscript's fixed prose, numbers, captions and conclusions.

NumPy is the numerical-engine dependency; Matplotlib draws the figures. Dependency installation may require internet access. The experiments themselves use only bundled inputs and require no account, remote model or API. The exact verified environment is recorded in `verification/verification.json`.

## Rebuild the Word manuscript

The supplied paper is `manuscript/StreetLux_Unified_Manuscript.docx`. To rebuild it, install `requirements-manuscript.txt` into the same environment, then run:

```bash
python authoring/build_manuscript.py
```

Use your environment's Python executable (for example, `.venv/bin/python` or `.\.venv\Scripts\python.exe`). The builder combines `manuscript.md`, the saved result tables, the four figures and native Word equations. To use a fresh reproduction instead:

```bash
python authoring/build_manuscript.py --results reproduced --figures reproduced/figures --output reproduced/StreetLux_Unified_Manuscript.docx
```

The builder reads the table values from the selected result files; narrative values are editable text and do not update automatically when inputs change. `authoring/equations.docx` is bundled, so Pandoc is not needed to rebuild the paper. If editing the mathematical source, the optional command `pandoc authoring/equations.md -o authoring/equations.docx` regenerates its native equations. Manuscript PDF conversion is not part of the runner.

## Contents

| Path | Purpose |
| --- | --- |
| `source/streetlux/` | Numerical model and route input |
| `source/reference_data/` | Spectral tables, conversion script and attribution |
| `pipeline.py` | Full study settings and numerical exports |
| `results/` | Saved study results, time series, spectral provenance and Table 3 data |
| `make_decomposition.py` | Two sequential allocations and their symmetric average |
| `make_figures.py` and `figures/` | Figure script and publication artwork |
| `verify.py` and `compare_results.py` | Regression and numerical reproducibility checks |
| `manuscript.md` and `authoring/` | Editable prose, table builder and native equations |
| `manuscript/` | Rebuilt Word paper |
| `verification/` | Checks from the clean-package reproduction, plus `convergence_check.py` (angular and time-step convergence; run separately, takes a few minutes) and its `convergence.json` |
| `CHANGELOG.md` | Changes between package versions |
| `SUBMISSION_NOTES.md` | Author-completion fields and current study scope |
| `MANIFEST_SHA256.json` | File digests for the delivered package |

Figure numbers match the manuscript: street sections (1), mode exposure (2), dose decomposition (3), and street interventions (4).

## Scientific interpretation

These are deterministic comparisons using a synthetic Dhaka-inspired route and assumed weather, geometry, material spectra and enclosures. They are not measurements of commuters or predictions of physiological outcomes. All reported calculations load the bundled CIE action spectra and photopic table. The D65 numerical deviation of 0.0165% is an internal metrological check. It does not validate the optical model against field observations or a reference renderer. A direct beam reaches the eye in 9 of 67 baseline walking steps and 2 of 33 cycle-rickshaw steps (office canyon only) and in no motorised-vehicle step; direct sun is 28.7% of walking mEDI.

Dose equals mean travel-facing mEDI multiplied by trip duration. The two sequential allocations in Table 3 depend on factor order; their symmetric average is the two-factor Shapley allocation. These are mathematical allocations, not isolated causal effects of glazing or journey duration. `dose_decomposition.csv` uses positive deficits from walking; the model's `modes.json` decomposition fields use the equivalent signed differences.

## Data attribution and licence

See `source/reference_data/README.md` for data citations and verification scope. Data-owner terms apply to the reference datasets. The author should specify the intended project licence before public distribution; this package does not invent a licence or relicense third-party data.
