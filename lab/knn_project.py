"""EEE213: reproducible CCPP k-nearest-neighbours regression project.

Run from repository root:
    python lab/knn_project.py

Uses first 80% of rows for training, final 20% for held-out testing.
Hyperparameters are selected using training-only five-fold CV.
Exact duplicate rows retained to match the course comparison protocol.
"""
from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
import sklearn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score, learning_curve
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'ccpp.csv'
FIGURES = ROOT / 'figures'
FIGURES.mkdir(parents=True, exist_ok=True)
FEATURES = ['AT', 'V', 'AP', 'RH']
RANDOM_STATE = 0


def main():
    df = pd.read_csv(DATA)
    assert list(df.columns) == FEATURES + ['PE']
    assert len(df) == 9568
    split = int(0.8 * len(df))
    tr, te = df.iloc[:split], df.iloc[split:]
    Xtr, Xte = tr[FEATURES], te[FEATURES]
    ytr, yte = tr['PE'], te['PE']
    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    dummy = DummyRegressor(strategy='mean').fit(Xtr, ytr)
    dummy_mae = mean_absolute_error(yte, dummy.predict(Xte))
    at = LinearRegression().fit(tr[['AT']], ytr)
    at_mae = mean_absolute_error(yte, at.predict(te[['AT']]))
    v = LinearRegression().fit(tr[['V']], ytr)
    v_mae = mean_absolute_error(yte, v.predict(te[['V']]))
    line4 = LinearRegression().fit(Xtr, ytr)
    line4_mae = mean_absolute_error(yte, line4.predict(Xte))

    # Week 12: held-out test is never used for cross-validation.
    dummy_cv = -cross_val_score(DummyRegressor(strategy='mean'), Xtr, ytr, cv=cv,
                               scoring='neg_mean_absolute_error', n_jobs=1)
    linear_cv = -cross_val_score(LinearRegression(), Xtr, ytr, cv=cv,
                                scoring='neg_mean_absolute_error', n_jobs=1)

    pipe = make_pipeline(StandardScaler(), KNeighborsRegressor())
    ks = [1, 3, 5, 10, 20]
    search = GridSearchCV(
        pipe, {'kneighborsregressor__n_neighbors': ks},
        cv=cv, scoring='neg_mean_absolute_error', refit=True,
        n_jobs=1, return_train_score=True,
    )
    search.fit(Xtr, ytr)
    best = search.best_estimator_
    knn_prediction = best.predict(Xte)
    knn_mae = mean_absolute_error(yte, knn_prediction)
    knn_rmse = float(np.sqrt(mean_squared_error(yte, knn_prediction)))
    cvmaes = -search.cv_results_['mean_test_score']
    cvstds = search.cv_results_['std_test_score']

    print('DATASET')
    print(f'rows={len(df)}, columns={len(df.columns)}, duplicates={int(df.duplicated().sum())}, missing={int(df.isna().sum().sum())}')
    print(f'train_rows={len(tr)}, test_rows={len(te)}; duplicates kept')
    print('FEATURES: AT (°C), V (cm Hg), AP (mbar), RH (%); target: PE (MW)')
    print('KNN PIPELINE: StandardScaler() -> KNeighborsRegressor()')
    print('CV: 5-fold KFold(shuffle=True, random_state=0), training rows only')
    print(f'BASELINE 5-FOLD CV MAE: {dummy_cv.mean():.6f} +/- {dummy_cv.std(ddof=1):.6f} MW')
    print(f'4-FEATURE LINEAR 5-FOLD CV MAE: {linear_cv.mean():.6f} +/- {linear_cv.std(ddof=1):.6f} MW')
    print('GRID SEARCH:')
    for k, mae, sd in zip(ks, cvmaes, cvstds):
        print(f'  k={k:>2}: CV MAE={mae:.4f} MW ± {sd:.4f}')
    print(f'BEST k: {search.best_params_["kneighborsregressor__n_neighbors"]}')
    print(f'BEST CV MAE: {-search.best_score_:.6f} MW')
    print('HELD-OUT TEST ERRORS (MW):')
    print(f'  Baseline (training mean): {dummy_mae:.6f}')
    print(f'  Linear regression, AT only: {at_mae:.6f}')
    print(f'  Linear regression, V only: {v_mae:.6f}')
    print(f'  Linear regression, all four: {line4_mae:.6f}')
    print(f'  k-NN, all four: {knn_mae:.6f}')
    print(f'k-NN test RMSE: {knn_rmse:.6f} MW')
    first = te.iloc[0]
    print(f'FIRST TEST ROW: CSV line {split+2}, AT={first.AT:.2f}, V={first.V:.2f}, AP={first.AP:.2f}, RH={first.RH:.2f}, true_PE={first.PE:.2f}, knn_pred={knn_prediction[0]:.6f}, absolute_error={abs(first.PE-knn_prediction[0]):.6f}')

    perm = permutation_importance(best, Xte, yte, scoring='neg_mean_absolute_error',
                                  n_repeats=10, random_state=RANDOM_STATE, n_jobs=1)
    print('PERMUTATION IMPORTANCE (increase in held-out MAE, 10 shuffles):')
    for name, mean, sd in zip(FEATURES, perm.importances_mean, perm.importances_std):
        print(f'  {name}: {mean:.4f} ± {sd:.4f} MW')

    # Week 13: feature ablation; each pipeline is freshly fitted on TRAINING folds.
    ablation_cv = {}
    print('FEATURE ABLATION (k=3; 5-fold TRAINING-ONLY CV):')
    for removed in [None] + FEATURES:
        cols = [x for x in FEATURES if x != removed]
        scores = -cross_val_score(
            make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=3)),
            Xtr[cols], ytr, cv=cv, scoring='neg_mean_absolute_error', n_jobs=1)
        label = removed if removed is not None else 'none'
        ablation_cv[label] = {'mean':float(scores.mean()),'std_ddof1':float(scores.std(ddof=1))}
        print(f'  removed={label}: CV MAE={scores.mean():.6f} +/- {scores.std(ddof=1):.6f} MW')

    # CV learning curve on training rows; held-out test is not involved in tuning
    sizes, train_scores, valid_scores = learning_curve(
        best, Xtr, ytr, cv=cv, scoring='neg_mean_absolute_error',
        train_sizes=[0.10,0.25,0.50,0.75,1.0], n_jobs=1,
    )
    lc_tr = -train_scores.mean(axis=1)
    lc_cv = -valid_scores.mean(axis=1)
    print('CV LEARNING CURVE:')
    for n, t, vld in zip(sizes,lc_tr,lc_cv):
        print(f'  n={n}: train_MAE={t:.4f}, validation_MAE={vld:.4f} MW')
    print(f'SOFTWARE: Python {sys.version.split()[0]}; NumPy {np.__version__}; pandas {pd.__version__}; scikit-learn {sklearn.__version__}')

    plt.rcParams.update({'font.size': 11,'axes.spines.top':False,'axes.spines.right':False})
    def save_fig(name):
        plt.tight_layout(pad=1.0)
        plt.savefig(FIGURES/name, dpi=190, facecolor='white', bbox_inches='tight')
        plt.close()

    # Week 12 exploratory visualisations
    fig, axes = plt.subplots(1, 2, figsize=(9.2,3.6))
    axes[0].hist(df['AT'],bins=32,color='#4074be',edgecolor='white')
    axes[0].set(xlabel='Ambient temperature AT (°C)',ylabel='Number of rows',title='Temperature distribution')
    axes[1].hist(df['PE'],bins=32,color='#4074be',edgecolor='white')
    axes[1].set(xlabel='Power output PE (MW)',ylabel='Number of rows',title='Output distribution')
    fig.tight_layout()
    save_fig('eda_distributions.png')

    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    ax.scatter(df['AT'],df['PE'],s=7,alpha=0.22,c='#4074be',rasterized=True)
    ax.set(xlabel='Ambient temperature AT (°C)', ylabel='Power output PE (MW)',title='Observed temperature-output relationship')
    ax.grid(alpha=0.15)
    save_fig('eda_scatter_at_pe.png')

    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    ax.plot(ks, cvmaes, 'o-', color='#3759cb', linewidth=2.5, markersize=9)
    ax.set_xlabel('Number of neighbors (k)')
    ax.set_ylabel('5-fold CV MAE (MW)')
    ax.set_xticks(ks)
    ax.axvline(int(search.best_params_['kneighborsregressor__n_neighbors']), color='#d9a441',ls='--', alpha=0.8)
    ax.grid(axis='y', alpha=0.22)
    save_fig('hyperparameter_search.png')

    names = ['Baseline','AT line','V line','4-feature line','4-feature k-NN']
    vals = [dummy_mae,at_mae,v_mae,line4_mae,knn_mae]
    fig, ax = plt.subplots(figsize=(8.2,3.8))
    bars = ax.barh(names, vals, color=['#9da9ba','#a4b4da','#b0bfdd','#93b1c9','#365acf'])
    ax.invert_yaxis(); ax.set_xlabel('Held-out test MAE (MW)')
    ax.set_xlim(0,max(vals)*1.20)
    for bar,vv in zip(bars,vals):ax.text(vv+0.15, bar.get_y()+bar.get_height()/2, f'{vv:.2f}',va='center',fontweight='bold',color='#1b2a44')
    ax.grid(axis='x', alpha=0.22)
    save_fig('model_comparison.png')

    fig, ax = plt.subplots(figsize=(7.8,3.8))
    ax.plot(sizes, lc_tr, '-o', lw=2, color='#3159c9', label='Training MAE')
    ax.plot(sizes, lc_cv, '-s', lw=2, color='#db8c41', label='CV validation MAE')
    ax.set_xlabel('Number of fit rows in each CV fold')
    ax.set_ylabel('MAE (MW)')
    ax.legend(frameon=False);ax.grid(alpha=0.18)
    save_fig('learning_curve.png')

    residuals = yte.to_numpy()-knn_prediction
    fig, ax = plt.subplots(figsize=(7.8,3.8))
    ax.scatter(Xte['AT'], residuals, s=8, alpha=0.28, c='#4067d5', rasterized=True)
    ax.axhline(0, color='#c24d51', linewidth=1.5)
    ax.set_xlabel('Ambient temperature AT (°C)')
    ax.set_ylabel('Residual: true PE – predicted PE (MW)')
    ax.grid(alpha=0.16)
    save_fig('residuals_vs_temperature.png')

    fig, ax = plt.subplots(figsize=(7.7,3.5))
    ax.barh(FEATURES[::-1],perm.importances_mean[::-1],color='#4667cd')
    ax.set_xlabel('Increase in held-out MAE after shuffling (MW)')
    ax.grid(axis='x',alpha=0.20)
    save_fig('permutation_importance.png')

    report = {
        'data_rows':len(df),'train_rows':len(tr),'test_rows':len(te),'duplicates':int(df.duplicated().sum()),
        'cv_baseline_mean':float(dummy_cv.mean()),'cv_baseline_std_ddof1':float(dummy_cv.std(ddof=1)),
        'cv_linear_mean':float(linear_cv.mean()),'cv_linear_std_ddof1':float(linear_cv.std(ddof=1)),
        'ablation_cv_mae':ablation_cv,
        'cv_k':ks,'cv_mae':[float(x) for x in cvmaes],'cv_std':[float(x) for x in cvstds],
        'best_k':int(search.best_params_['kneighborsregressor__n_neighbors']),
        'best_cv_mae':float(-search.best_score_),'test_mae_knn':float(knn_mae),'test_rmse_knn':float(knn_rmse),
        'test_mae_baseline':float(dummy_mae),'test_mae_at_line':float(at_mae),
        'test_mae_v_line':float(v_mae),'test_mae_all_line':float(line4_mae),
        'first_test_file_line':int(split+2),'first_test_true_PE':float(first.PE),
        'first_test_prediction':float(knn_prediction[0]),'first_test_absolute_error':float(abs(first.PE-knn_prediction[0])),
        'permutation_importance_mae_increase':{name:float(v) for name,v in zip(FEATURES,perm.importances_mean)},
        'lc_sizes':[int(n) for n in sizes],'lc_train_mae':[float(x) for x in lc_tr],'lc_cv_mae':[float(x) for x in lc_cv],
    }
    (ROOT/'results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')

if __name__ == '__main__':
    main()
