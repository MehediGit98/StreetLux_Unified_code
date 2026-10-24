"""Export the positive dose-deficit allocations used in manuscript Table 3.

Inputs are the saved mode-mean mEDI and duration, not rounded table values.
The sequential contributions sum to the same deficit under either ordering.
Their averages are checked against the solver's signed symmetric allocation.
"""
from pathlib import Path
import argparse
import csv
import json
import math

ROOT = Path(__file__).resolve().parent
MODE_LABELS = {
    'rickshaw': 'Cycle rickshaw',
    'car_clear': 'Clear-glazed car',
    'car_tinted': 'Bronze-glazed car',
    'cng': 'CNG auto-rickshaw',
    'car_film': 'Car with film',
    'bus': 'Bus window seat',
}


def close(actual, expected, label):
    if not math.isclose(actual, expected, rel_tol=1e-9, abs_tol=1e-8):
        raise ValueError(f'{label}: {actual} != {expected}')


def calculate(modes):
    source = {row['key']: row for row in modes['rows']}
    base = source['walk']['summary']
    r0 = base['mean_medi_travel_lx']
    t0 = base['duration_min'] / 60
    close(r0 * t0, base['dose_travel_lxh'], 'Walking dose')
    rows = []
    for key, label in MODE_LABELS.items():
        s = source[key]['summary']
        r = s['mean_medi_travel_lx']
        t = s['duration_min'] / 60
        gap = r0 * t0 - r * t
        if gap <= 0:
            raise ValueError(f'{key}: Table 3 requires a positive deficit from walking')
        a_t, a_r = r0 * (t0 - t), t * (r0 - r)
        b_t, b_r = r * (t0 - t), t0 * (r0 - r)
        s_t, s_r = (a_t + b_t) / 2, (a_r + b_r) / 2
        close(r * t, s['dose_travel_lxh'], f'{key}: dose')
        for name, total in [('duration first', a_t + a_r),
                            ('rate first', b_t + b_r),
                            ('symmetric', s_t + s_r)]:
            close(total, gap, f'{key}: {name} sum')
        signed = source[key]['decomposition']
        close(gap, -signed['gap_lxh'], f'{key}: signed deficit')
        close(s_t, -signed['gap_from_duration_lxh'], f'{key}: duration contribution')
        close(s_r, -signed['gap_from_exposure_rate_lxh'], f'{key}: rate contribution')
        close(s_t / gap, signed['duration_share_of_gap'], f'{key}: duration share')
        rows.append({
            'mode': key, 'label': label,
            'reference_rate_lx': r0, 'reference_duration_h': t0,
            'rate_lx': r, 'duration_h': t, 'gap_lxh': gap,
            'duration_first_duration_lxh': a_t,
            'duration_first_rate_lxh': a_r,
            'rate_first_duration_lxh': b_t,
            'rate_first_rate_lxh': b_r,
            'symmetric_duration_lxh': s_t,
            'symmetric_rate_lxh': s_r,
            'duration_first_pct': 100 * a_t / gap,
            'rate_first_pct': 100 * b_t / gap,
            'symmetric_duration_pct': 100 * s_t / gap,
            'symmetric_rate_pct': 100 * s_r / gap,
        })
    return rows


def export(data, out):
    rows = calculate(json.loads((Path(data) / 'modes.json').read_text(encoding='utf-8')))
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'dose_decomposition.json').write_text(
        json.dumps(rows, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')
    with (out / 'dose_decomposition.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=ROOT / 'results')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    rows = export(args.data, args.out or args.data)
    print(f'Exported {len(rows)} decomposition rows with allocation checks passed.')
