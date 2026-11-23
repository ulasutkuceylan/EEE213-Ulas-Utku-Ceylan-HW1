---
layout: default
title: Method Presentation — k-NN Regression
---

# Week 10 — Four-minute method presentation

[Home](index.html) · [Numerical problem](numerical.html) · [Data and model](model.html) · [Code](code.html)

**Method #4:** k-Nearest Neighbors Regression.  
**Task:** Supervised regression of electrical output PE in MW.  
**Class format:** 4 minutes presentation + 1 minute questions (EEE213 Week 09).

## Presentation files

- [**13-slide editable PowerPoint**](slides/EEE213_kNN_Regression_Presentation.pptx)
- [**13-slide PDF**](slides/EEE213_kNN_Regression_Presentation.pdf)
- [**Four-minute English speaking script**](speaker_script_4min_EN.md)
- [Slide-by-slide English notes](speaker_notes_en.md)
- [Türkçe anlatım notları](speaker_notes_tr.md)

## Timed narrative

| Topic required by Week 09 | Time |
|---|---:|
| Task definition and predicted target | 0:30 |
| How k-NN works: nearest neighbors, scaling, prediction equation | 1:30 |
| Main hyperparameter k and CV search | 0:30 |
| Held-out test result versus baseline | 1:00 |
| One strength and one limitation | 0:30 |
| **Total** | **4:00** |

**Main equation** for unweighted k-NN regression:


$$
\widehat{PE}(x)=\frac{1}{k}\sum_{i\in N_k(x)} PE_i .
$$


**Quantitative result:** k = 3, CV MAE = 2.763 MW, held-out test MAE = 2.743 MW, mean-baseline test MAE = 14.723 MW. Values and illustrations are produced from [`lab/knn_project.py`](https://github.com/ulasutkuceylan/EEE213-Ulas-Utku-Ceylan-HW1/blob/main/lab/knn_project.py).

## Sources and disclosure

[1] T. Hastie, R. Tibshirani, and J. Friedman, *The Elements of Statistical Learning*, 2nd ed. Springer, 2009.

[2] scikit-learn developers, “Nearest Neighbors,” *scikit-learn User Guide*. https://scikit-learn.org/stable/modules/neighbors.html

AI assistance and verification are disclosed on the [code page](code.html).

> **Before presenting:** Rehearse the timing, check the PPTX/PDF links, and regenerate the test MAE from the code yourself.
