# EEE213 — k-Nearest Neighbors Regression

## Four-minute English presentation script (approximate timing)

**Important:** Rehearse aloud with a timer. The words below are a practice script, not evidence of personal verification. The 13-slide file is designed to be presented briskly, combining neighboring slides where appropriate.

### 0:00–0:30 — Definition and task (slides 1–3)

Good morning. My topic is k-nearest neighbors regression, or k-NN. I will use it to predict the net electrical output of a combined-cycle power plant. Because electrical output is a continuous quantity in megawatts, this is a regression problem. The four inputs are ambient temperature, exhaust vacuum, atmospheric pressure and relative humidity. The dataset contains 9,568 hourly records from full-load operation.

### 0:30–2:00 — How it learns (slides 4–7)

The central idea of k-NN is simple: similar operating conditions often correspond to similar power output. Unlike linear regression, this method does not learn a set of slope coefficients. Instead, it stores the training examples. For a new observation, it calculates the distance to those examples, chooses the k nearest ones, and averages their measured power outputs. For example, if the three nearest neighbors produced 450, 454 and 456 megawatts, the prediction would be 453.33 megawatts.

There is an important practical detail. Our predictors have different units and numerical ranges, so Euclidean distance can be misleading without scaling. I use StandardScaler inside a scikit-learn pipeline. This pipeline is fitted within each cross-validation fold, preventing validation information from leaking into preprocessing. I keep the first 7,654 rows for training and the final 1,914 for testing. The test set is not used to choose k.

### 2:00–2:30 — Hyperparameters (slide 8)

The main hyperparameter is k, the number of neighbors. With a very small k the model may follow noise and overfit. With a large k predictions become smoother, but may underfit. I tested k values of 1, 3, 5, 10 and 20. Using five-fold cross-validation on training data only, k equals 3 gave the lowest average validation MAE, about 2.76 megawatts.

### 2:30–3:30 — Results on our data (slides 9–11)

For evaluation I used mean absolute error, or MAE, measured in megawatts. The baseline always predicts the average training output and has a test MAE of 14.72 megawatts. Four-feature linear regression achieves 3.66 megawatts. Our k-NN model with k equal to 3 achieves 2.74 megawatts on the held-out test rows, so its MAE is about 81 percent below the baseline. A specific example is the first test record, where the measured power is 483.12 megawatts and the k-NN prediction is 484.34 megawatts. I also inspected the learning curve and residuals to understand how errors behave.

### 3:30–4:00 — Strength, limitation and close (slides 12–13)

A strength of k-NN is that it can describe nonlinear patterns without prescribing a fixed equation. One limitation is sensitivity to feature scaling, the choice of k and the representativeness of training data. This dataset also contains exact duplicates, including some shared between training and test, so the result may be optimistic. The measurements cover full-load operation only. My code, data source, plots, references and AI-use disclosure are available in the project repository. Thank you.
