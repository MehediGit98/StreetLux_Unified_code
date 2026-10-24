"""Reproduce the StreetLux analysis, four figures and manuscript Table 3 data."""
from pathlib import Path
import argparse
import json
from pipeline import reproduce
from make_figures import main as figures
from make_decomposition import export, close
from compare_results import compare_results

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / 'reproduced')
    parser.add_argument('--skip-comparison', action='store_true',
                        help='For intentional input changes; review manuscript prose afterward')
    args = parser.parse_args()
    if args.out.resolve() == (ROOT / 'results').resolve():
        parser.error('Use a separate output directory so the saved study results remain available for comparison.')
    reproduce(args.out)
    rows = export(args.out, args.out)
    figures(args.out, args.out / 'figures')
    if not args.skip_comparison:
        count = compare_results(ROOT / 'results', args.out)
        expected = json.loads((ROOT / 'results/dose_decomposition.json').read_text(encoding='utf-8'))
        if len(rows) != len(expected):
            raise AssertionError('Decomposition row count differs')
        for actual, saved in zip(rows, expected):
            if actual.keys() != saved.keys():
                raise AssertionError('Decomposition columns differ')
            for key, value in saved.items():
                if isinstance(value, (int, float)):
                    close(actual[key], value, f"{saved['mode']}: {key}")
                elif actual[key] != value:
                    raise AssertionError(f'Decomposition label differs: {key}')
        print(f'PASS: {count} numeric fields match the saved results (rtol=1e-9, atol=1e-8).')
        print(f'PASS: all {len(rows)} sequential and symmetric decomposition rows match.')


if __name__ == '__main__':
    main()
