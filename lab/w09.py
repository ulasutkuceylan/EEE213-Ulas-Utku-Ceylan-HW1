"""EEE213 Week 09: data quality, exploratory analysis and model comparison.

Run from repository root:
    python lab/w09.py

The fixed course split keeps the first 7654 rows for training and 1914
for testing; exact duplicates are retained for comparison with the slides.
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import mean_absolute_error


def main():
    path = Path(__file__).resolve().parent.parent / "data" / "ccpp.csv"
    df = pd.read_csv(path)
    if list(df.columns) != ["AT", "V", "AP", "RH", "PE"]:
        raise ValueError("Unexpected column names or order")
    if len(df) != 9568:
        raise ValueError("Expected 9568 rows in the complete CCPP file")

    print(f"Rows: {len(df)}; columns: {len(df.columns)}")
    print(f"Missing cells: {int(df.isna().sum().sum())}; exact duplicate rows: {int(df.duplicated().sum())}")
    for name, unit in [("AT", "°C"), ("V", "cm Hg"), ("AP", "mbar"), ("RH", "%"), ("PE", "MW")]:
        print(f"{name} range: {df[name].min():.2f} to {df[name].max():.2f} {unit}")

    for name in ["AT", "PE"]:
        print(f"{name} mean/median/sample std: {df[name].mean():.2f} / {df[name].median():.2f} / {df[name].std():.2f}")

    correlations = df.corr(numeric_only=True)["PE"]
    print("Correlations with PE: " + ", ".join(f"{x}={correlations[x]:+.3f}" for x in ["AT", "V", "AP", "RH"]))

    split = int(0.8 * len(df))
    training = df.iloc[:split]
    test = df.iloc[split:]
    print(f"Training rows: {len(training)}; test rows: {len(test)}")
    overlap = pd.merge(test.drop_duplicates(), training.drop_duplicates(), how="inner", on=list(df.columns))
    print(f"Distinct test rows that match training rows: {len(overlap)}")

    baseline = training["PE"].mean()
    baseline_mae = mean_absolute_error(test["PE"], np.full(len(test), baseline))
    print(f"Baseline training mean: {baseline:.6f} MW; test MAE: {baseline_mae:.6f} MW")

    models = {}
    for feature in ["AT", "V"]:
        slope, intercept = np.polyfit(training[feature].to_numpy(), training["PE"].to_numpy(), 1)
        mae = mean_absolute_error(test["PE"], slope * test[feature] + intercept)
        models[feature] = (slope, intercept, mae)
        print(f"{feature} line: slope={slope:.6f}, intercept={intercept:.6f}, test MAE={mae:.6f} MW")

    first_test = test.iloc[0]
    slope, intercept, _ = models["V"]
    prediction = slope * first_test["V"] + intercept
    print(f"First test row: CSV line {split + 2}; V={first_test['V']:.2f} cm Hg; predicted PE={prediction:.6f} MW; true PE={first_test['PE']:.2f} MW; absolute error={abs(prediction-first_test['PE']):.6f} MW")
    print(f"Software: Python {sys.version.split()[0]}, NumPy {np.__version__}, pandas {pd.__version__}, scikit-learn {sklearn.__version__}")


if __name__ == "__main__":
    main()
