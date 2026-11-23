"""Check that the course deliverables and reproducible numerical results exist.

Must be run after code/run_all.py's three computation scripts.
"""
from pathlib import Path
import json
import math
import zipfile

ROOT=Path(__file__).resolve().parents[1]
FILES=[
    'index.md','numerical.md','model.md','presentation.md','code.md','_config.yml',
    'lab/w09.py','lab/knn_project.py','code/numerical.py','data/ccpp.csv',
    'results.json','numerical_results.json','slides/EEE213_kNN_Regression_Presentation.pptx',
    'slides/EEE213_kNN_Regression_Presentation.pdf',
    'figures/model_comparison.png','figures/hyperparameter_search.png',
    'figures/learning_curve.png','figures/residuals_vs_temperature.png',
    'figures/permutation_importance.png','figures/solar_cell_iv_pv.png',
    'figures/solar_cell_newton_convergence.png','figures/eda_distributions.png',
    'figures/eda_scatter_at_pe.png',
]

def main():
    for f in FILES:
        p=ROOT/f
        if not p.is_file() or p.stat().st_size == 0:
            raise AssertionError('Missing or empty project file: '+f)
    index=(ROOT/'index.md').read_text(encoding='utf-8')
    for link in ['numerical.html','model.html','presentation.html','code.html']:
        if link not in index:
            raise AssertionError('Home page missing link: '+link)
    result=json.loads((ROOT/'results.json').read_text(encoding='utf-8'))
    numeric=json.loads((ROOT/'numerical_results.json').read_text(encoding='utf-8'))
    assert result['data_rows']==9568 and result['train_rows']==7654 and result['test_rows']==1914
    assert result['best_k']==3
    assert math.isclose(result['test_mae_knn'],2.743108672936259,abs_tol=1e-4)
    assert math.isclose(result['test_mae_baseline'],14.72315212075887,abs_tol=1e-4)
    assert math.isclose(numeric['Vmp_newton_V'],0.7188038973,abs_tol=1e-9)
    assert math.isclose(numeric['Pmp_W'],3.4344331522,abs_tol=1e-9)
    assert abs(numeric['final_residual_A'])<1e-10
    assert numeric['absolute_agreement_golden_V']<1e-7
    with zipfile.ZipFile(ROOT/'slides/EEE213_kNN_Regression_Presentation.pptx') as p:
        count=len([x for x in p.namelist() if x.startswith('ppt/slides/slide') and x.endswith('.xml')])
        assert 10 <= count <=15, f'Unexpected slide count {count}'
    print('VERIFICATION PASSED')
    print(f'  files_checked={len(FILES)}, slide_count={count}, four_site_links=present')
    print(f"  baseline_test_MAE={result['test_mae_baseline']:.6f} MW")
    print(f"  kNN_best_k={result['best_k']}, kNN_test_MAE={result['test_mae_knn']:.6f} MW")
    print(f"  solar_cell_Vmp={numeric['Vmp_newton_V']:.10f} V, Pmp={numeric['Pmp_W']:.10f} W")

if __name__=='__main__': main()
