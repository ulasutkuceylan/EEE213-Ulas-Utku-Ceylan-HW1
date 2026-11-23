# EEE213 k-NN Regression — English speaking notes

1. **Title:** Today I present k-nearest neighbors regression for predicting full-load power-plant output.
2. **Task:** Inputs are ambient temperature, exhaust vacuum, pressure and relative humidity. The output is a continuous value in MW, so this is regression.
3. **Data:** The UCI dataset has 9,568 hourly observations, four predictors and one target, measured during full-load operation.
4. **Checks:** There are no missing entries and 41 exact duplicate rows. I kept them for the prescribed comparison. The split is the first 7,654 rows for training and the last 1,914 for testing.
5. **Mechanism:** k-NN predicts by averaging the outputs of the nearest training examples in feature space.
6. **Scaling:** Inputs have different scales, so I fit StandardScaler inside the pipeline, separately within each training fold.
7. **Protocol:** I selected the number of neighbors using five-fold cross-validation on training data only.
8. **Grid search:** I tried k values 1, 3, 5, 10 and 20. The best was k equals 3 with a CV MAE of 2.763 MW.
9. **Results:** The held-out test MAE is 2.74 MW for k-NN, compared with 14.72 for the baseline and 3.66 for four-variable linear regression.
10. **Prediction:** For the first test record, measured output is 483.12 MW and k-NN predicts 484.34 MW, giving an absolute error of 1.22 MW.
11. **Diagnostics:** The validation error falls as the number of training observations grows. The residual plot shows error patterns over ambient temperature.
12. **Limitations:** Temperature is most important for this fitted model. Permutation importance does not prove causation. Duplicate overlap and full-load-only data limit generalisation.
13. **Reproducibility:** My Python script prints every key result and regenerates the figures. The code, slides, references and AI-use statement are included in the GitHub repository.
