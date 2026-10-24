"""Reproduce one study from bundled local source and official reference tables."""
from pathlib import Path
import argparse, csv, hashlib, json, platform, sys, time
import numpy as np

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'source'
sys.path.insert(0, str(SOURCE / 'streetlux'))

from streetlux.reference_data import load_publication_references
from streetlux import self_check, spectra, photometry
from streetlux.jsonio import dumps

def save(path, data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(dumps(data),encoding='utf-8')

def csvsave(path, rows):
    rows=list(rows)
    if not rows: return
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,keys); w.writeheader()
        for r in rows: w.writerow({k:json.dumps(v) if isinstance(v,(dict,list,tuple)) else v for k,v in r.items()})

def reproduce(out):
    study = "streetlux"
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    t0=time.time()
    ref=load_publication_references(SOURCE/'reference_data')
    assert spectra.provenance()['official_action_spectra']
    assert spectra.provenance()['official_solar_spectrum']
    check=self_check(); save(out/'metrology_checks.json',check)
    from streetlux.route import load_route
    from streetlux.scenarios import compare_modes, compare_designs
    from streetlux.report import write_html
    route=load_route(SOURCE/'streetlux/examples/dhaka_mirpur_motijheel.json')
    route.name='Dhaka-inspired five-section route, morning'
    save(out/'route.json',route.to_dict())
    for name, fn in [('modes',compare_modes),('designs',compare_designs)]:
        result=fn(route,n_headings=24,n_directions=768,step_seconds=60.0,objective='dose_weighted')
        save(out/(name+'.json'),result)
        write_html(result,out/(name+'.html'))
        csvsave(out/(name+'_summary.csv'),({'key':r['key'],'label':r['label'],
            **{k:v for k,v in r['summary'].items() if not isinstance(v,(dict,list))},
            'heading_ratio':r['summary']['heading_spread']['ratio_max_min'],
            'delta_vs_baseline_pct':r.get('delta_vs_baseline_pct'),
            'decomposition':r.get('decomposition')} for r in result['rows']))
        csvsave(out/(name+'_time_series.csv'),({'key':r['key'],**st} for r in result['rows'] for st in r['series']))
    save(out/'run_metadata.json',{'study':study,'package_version':'0.2.1','python':sys.version.split()[0],
        'numpy':np.__version__,'platform':platform.system(),'wall_clock_s':round(time.time()-t0,2),
        'parameters_source':'pipeline.py','reference_data':ref,
        'reference_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (SOURCE/'reference_data').glob('*.csv')}})
    print(study,'completed in',round(time.time()-t0,2),'s',flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=ROOT / 'reproduced')
    reproduce(parser.parse_args().out)
