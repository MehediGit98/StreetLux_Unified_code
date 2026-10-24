# Changelog

## 0.2.1 (2026-10-02)

### Fixed
- `source/streetlux/streetlux/sun.py`: `solar_position()` returned the correct solar altitude but an azimuth mirrored about the east-west axis (model azimuth = 180 deg minus the correct azimuth). The morning sun was therefore placed north-east instead of south-east and no direct beam reached the eye in the office canyon. Azimuth is now 180 deg minus acos(ca) before solar noon and 180 deg plus acos(ca) after (NOAA convention). It agrees with the independent `astral` 3.2 library to within 0.01 deg on ten reference cases (both hemispheres, morning and afternoon, summer and winter).
- `make_figures.py`: the x-axis limits of Figure 4 were fixed numbers; they now follow the data so that larger effects are not clipped.

### Added
- `verify.py`: six new tests (now eleven in total): solar position against ten reference cases, morning/afternoon sense of the azimuth, sun-side beam visibility in an east-west canyon, an open-sky limit, monotonic occlusion and mirrored-street invariance. On version 0.2.0 the solar-position and sun-side tests fail.
- `verification/convergence_check.py` and `verification/convergence.json`: mean mEDI for walking, CNG auto-rickshaw and car with film at 768, 3072 and 12288 sampled directions and at a 15 s time step.

### Changed results (768 directions, 60 s step, official tables)
| Quantity | 0.2.0 | 0.2.1 |
| --- | --- | --- |
| Walking mean mEDI (lx) | 3876.4 | 8769.5 |
| Walking dose (lx h) | 4281.3 | 9685.5 |
| Lowest mean mEDI | car with film, 264.5 | bus window seat, 332.4 |
| Lowest dose (lx h) | car with film, 65.7 | car with film, 94.1 |
| Walk vs filmed car, rate ratio | 14.65 | 23.16 |
| Walk vs filmed car, dose ratio | 65.12 | 102.95 |
| Whitewashed facades (% dose) | +143.4 | +65.9 |
| Height cap 18 m | +52.2 | +62.4 |
| Minimum width 18 m | +15.2 | +10.4 |
| Pale paving | +11.0 | +5.1 |
| Foliage 40% / 70% | -20.1 / -38.1 | -34.5 / -60.0 |
| Direct-beam steps, walking / rickshaw | 0 / 0 | 9 / 2 |

The ranking of the six interventions is unchanged. The clear-glazed car vs CNG dose reversal of 0.2.0 no longer occurs; two other pairs reverse (bronze-glazed car vs CNG; car with film vs bus).

### Updated to match
`results/`, `figures/`, `manuscript.md` and `manuscript/StreetLux_Unified_Manuscript.docx`, `verification/`, `MANIFEST_SHA256.json`, version strings (0.2.0 to 0.2.1) in `pyproject.toml`, `__init__.py`, `pipeline.py`, `README.md` files and the manuscript.

### Known limitations of this release
Angular convergence: from 768 to 12288 directions the corrected film-car mean mEDI changes by +5.7% (walking +1.5%, CNG +1.7%); see `verification/convergence.json`. The headline run still uses the original 768 directions.

## 0.2.0
Initial package (contains the solar-azimuth error described above; superseded).
