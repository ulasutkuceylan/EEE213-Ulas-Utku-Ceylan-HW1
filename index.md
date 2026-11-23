---
layout: default
title: EEE213 Project — Home
---

# EEE213 — Scientific Programming

**Term Project — number 4 (chosen with instructor permission)**  
**Machine-learning topic:** k-Nearest Neighbors Regression  
**Numerical problem:** Solar-cell maximum power point, Newton–Raphson  
**Student repository:** [EEE213-Ulas-Utku-Ceylan-HW1](https://github.com/ulasutkuceylan/EEE213-Ulas-Utku-Ceylan-HW1)

## Abstract (English)

This project studies two different numerical tasks. First, a supervised k-nearest neighbors (k-NN) regressor estimates full-load combined-cycle power-plant output in MW from ambient temperature, exhaust vacuum, pressure and humidity. The dataset contains 9,568 records; the first 7,654 form the training set, and the last 1,914 are held out. Training-only cross-validation selects three neighbors and produces a test mean absolute error of 2.743 MW compared with a 14.723 MW mean baseline. Second, the maximum-power voltage of an ideal illuminated solar cell is calculated with Newton–Raphson and independently checked by derivative-free direct power maximization.

## Özet (Türkçe)

Projede iki sayısal çalışma bulunmaktadır. İlkinde, k-en yakın komşu (k-NN) regresyon yöntemi kullanılarak dört çevresel değişkenden kombine çevrim santralinin tam yükteki elektrik üretimi tahmin edilir. Toplam 9.568 kaydın ilk 7.654'ü eğitim, son 1.914'ü test içindir. Eğitim verisiyle yapılan çapraz doğrulama üç komşuyu seçer; test MAE değeri 2,743 MW, ortalama tahmin temel çizgisi ise 14,723 MW'tır. İkinci çalışmada ideal bir güneş hücresinin maksimum güç noktası Newton–Raphson ile bulunur ve farklı yöntemlerle doğrulanır.

## Project pages

1. [Numerical problem — model, derivation, Newton iterations, independent check](numerical.html)
2. [Data and model — data card, CV search, baseline, diagnostics](model.html)
3. [Presentation — 13 slides, PDF and timed speaker notes](presentation.html)
4. [Code and AI use — reproducibility and disclosure](code.html)

## Summary results

| Quantity | Verified reference result |
|---|---:|
| CCPP training / test | 7,654 / 1,914 rows |
| k-NN neighbors selected by 5-fold CV | 3 |
| Mean-baseline test MAE | 14.7232 MW |
| k-NN test MAE | **2.7431 MW** |
| Solar-cell maximum-power voltage | **0.718804 V** |
| Solar-cell maximum power | **3.434433 W** |

The solar-cell values refer to **stated illustrative assumptions**, not measured commercial-cell specifications. See the detailed pages for all assumptions and limitations.

**Sources:** [UCI CCPP dataset](https://doi.org/10.24432/C5002N) (CC BY 4.0), [scikit-learn Nearest Neighbors](https://scikit-learn.org/stable/modules/neighbors.html), EEE213 Weeks 9–13 lecture slides.
