---
layout: default
title: Reproducible Code and AI Use
---

# Code, reproducibility and responsible AI use

[Home](index.html) · [Numerical problem](numerical.html) · [Data and model](model.html) · [Presentation](presentation.html)

## One reproducibility command

From the **repository root** (the folder containing `data/`, `lab/`, and `code/`), use an **isolated Python 3.13 virtual environment** so that the previously used Week 09 environment stays unchanged:

```powershell
py -3.13 -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
& ".\.venv\Scripts\python.exe" code/run_all.py
```

PowerShell `.ps1` activation is **not needed**. Alternatively, with an already active and equipped environment, run `python code/run_all.py`.

`code/run_all.py` invokes `lab/w09.py`, `lab/knn_project.py`, `code/numerical.py` and the output validator with the currently selected interpreter. All headline numbers and figures can be reproduced.

## Source files

| File | Reproducible output |
|---|---|
| [`lab/w09.py`](https://github.com/ulasutkuceylan/EEE213-Ulas-Utku-Ceylan-HW1/blob/main/lab/w09.py) | Week 09 data checks, statistics, baseline, AT and V linear models |
| [`lab/knn_project.py`](https://github.com/ulasutkuceylan/EEE213-Ulas-Utku-Ceylan-HW1/blob/main/lab/knn_project.py) | 5-fold CV, grid search, MAE/RMSE, baseline and linear comparison, learning curve, residuals, permutation importance and ablation |
| [`code/numerical.py`](https://github.com/ulasutkuceylan/EEE213-Ulas-Utku-Ceylan-HW1/blob/main/code/numerical.py) | Solar-cell Newton iteration, analytical derivative, finite difference and independent golden-section/grid checks |
| [`code/run_all.py`](https://github.com/ulasutkuceylan/EEE213-Ulas-Utku-Ceylan-HW1/blob/main/code/run_all.py) | Run all three scripts from one command |
| [`data/ccpp.csv`](https://github.com/ulasutkuceylan/EEE213-Ulas-Utku-Ceylan-HW1/blob/main/data/ccpp.csv) | Complete dataset with 9,568 rows |
| [`data/README.md`](data/README.md) | Dataset source, licence, conversion and limitations |
| [`requirements.txt`](https://github.com/ulasutkuceylan/EEE213-Ulas-Utku-Ceylan-HW1/blob/main/requirements.txt) | Reference package versions |
| [`results.json`](results.json) | Machine-readable k-NN results |
| [`numerical_results.json`](numerical_results.json) | Machine-readable Newton and independent-check results |

Reference console output: [`knn_console_output.txt`](knn_console_output.txt), [`numerical_console_output.txt`](numerical_console_output.txt) and [`console_output_w09.txt`](console_output_w09.txt).

## Software used to verify this reference package

Python 3.13.5; NumPy 2.3.5; pandas 2.2.3; scikit-learn 1.8.0; Matplotlib 3.10.8. Your earlier Week 09 output used Python 3.13.1, NumPy 2.1.1, pandas 2.2.3 and scikit-learn 1.9.1. These are **two separate environments**; preserve the real versions of the environment you use for the submitted runs.

## AI-use statement — explicit and verifiable

**Tool and date:** OpenAI ChatGPT, November 21–22, 2026.

**Purpose:** Drafting and structuring presentation material, project website, Python code, explanations, English/Turkish text, troubleshooting and methods for checks.

**What was used:** k-NN pipeline structure, parameter-search procedure, graphs, numerical solar-cell model, Newton derivation draft, reproducibility instructions and formatted documentation.

**Verification already performed:** The assistant ran `lab/knn_project.py` against the included CSV and compared the MAE figures with EEE213 reference values. The assistant also executed `code/numerical.py`, checked Newton residual and derivative by finite differences, and confirmed maximum power independently by power-only golden-section optimization and a dense voltage grid. The listed scripts and logs record these checks.

**Student verification still required:** The student should re-run the full command on their own machine, inspect the assumptions and computations, confirm the Week 09 draw number, cite sources, and explain the methods without relying only on this generated text. These steps are **not claimed as completed by the student**.

**Limitations:** An LLM may generate incorrect mathematics or code. All numerical claims are tied to a reproducible program and should be independently reviewed.

## References

[1] P. Tüfekci and H. Kaya, “Combined Cycle Power Plant,” *UCI Machine Learning Repository*, 2014, doi:10.24432/C5002N, CC BY 4.0.  
[2] Scikit-learn developers, “1.6. Nearest Neighbors,” https://scikit-learn.org/stable/modules/neighbors.html.  
[3] Scikit-learn developers, “Tuning the hyper-parameters of an estimator,” https://scikit-learn.org/stable/modules/grid_search.html.  
[4] T. Hastie, R. Tibshirani, and J. Friedman, *The Elements of Statistical Learning*, 2nd ed. Springer, 2009.  
[5] EEE213, *Scientific Programming*, Weeks 9–13 lecture slides, İzmir Kâtip Çelebi University, Fall 2026.
