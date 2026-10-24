"""Angular and temporal convergence check for the StreetLux baseline runs.

Not part of reproduce.py (it takes a few minutes).  Run from the package root:
    python verification/convergence_check.py
Writes verification/convergence.json.  Uses the same route, headings, official
spectral tables and 60 s step as pipeline.py; only the number of sampled
directions (and, in one extra row, the time step) changes.
"""
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source'
sys.path.insert(0, str(SOURCE / 'streetlux'))
from streetlux.reference_data import load_publication_references
from streetlux.route import load_route
from streetlux.exposure import simulate

load_publication_references(SOURCE / 'reference_data')
route = load_route(SOURCE / 'streetlux/examples/dhaka_mirpur_motijheel.json')

CASES = [('walk', 'Walking'), ('cng', 'CNG auto-rickshaw'), ('car_film', 'Car with film')]
SETTINGS = [(768, 60.0), (3072, 60.0), (12288, 60.0), (768, 15.0)]
out = {'reference': 'n_directions=768, step_seconds=60 (pipeline.py settings)', 'rows': []}
for key, label in CASES:
    vals = []
    for n_dirs, step in SETTINGS:
        r = simulate(route, key, n_headings=24, n_directions=n_dirs, step_seconds=step)
        vals.append({'n_directions': n_dirs, 'step_seconds': step,
                     'mean_medi_travel_lx': r.mean_medi('travel'), 'dose_travel_lxh': r.dose_lxh('travel')})
    base = vals[0]['mean_medi_travel_lx']
    for v in vals:
        v['change_vs_reference_pct'] = 100.0 * (v['mean_medi_travel_lx'] / base - 1.0)
    out['rows'].append({'mode': key, 'label': label, 'runs': vals})
    print(label, [(v['n_directions'], v['step_seconds'], round(v['change_vs_reference_pct'], 2)) for v in vals], flush=True)
(ROOT / 'verification/convergence.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
