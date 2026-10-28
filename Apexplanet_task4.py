
# ============================================================
# APEXPLANET TASK 4: HYPOTHESIS TESTING
# Business question: Do average sales differ by gender?
# Statistical test: Welch's independent two-sample t-test
# ============================================================

# STEP 1: Import libraries

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats



# STEP 2: Define file paths

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_DIR / "data" / "cleaned_sales_dataset.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


# STEP 3: Load the dataset

df = pd.read_csv("cleaned_sales_dataset.csv")

# Remove accidental spaces from column names
df.columns = df.columns.str.strip()

print("Dataset loaded successfully!")
print("Number of rows:", len(df))
print("\nAvailable columns:")
print(df.columns.tolist())


# STEP 4: Check required columns

required_columns = ["Gender", "Total_Sales"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(
            f"Required column '{column}' was not found. "
            f"Available columns: {df.columns.tolist()}"
        )


# STEP 5: Clean the columns used for testing

df["Gender"] = (
    df["Gender"]
    .astype("string")
    .str.strip()
    .str.title()
)

df["Total_Sales"] = pd.to_numeric(
    df["Total_Sales"],
    errors="coerce"
)

# Keep only Male/Female records with valid sales values
test_data = df[
    df["Gender"].isin(["Male", "Female"])
    & df["Total_Sales"].notna()
].copy()

male_sales = test_data.loc[
    test_data["Gender"] == "Male", "Total_Sales"
].to_numpy(dtype=float)

female_sales = test_data.loc[
    test_data["Gender"] == "Female", "Total_Sales"
].to_numpy(dtype=float)

if len(male_sales) < 2 or len(female_sales) < 2:
    raise ValueError(
        "At least two valid sales records are required "
        "in each gender group."
    )

if not np.isfinite(male_sales).all() or not np.isfinite(female_sales).all():
    raise ValueError("Sales data contains infinite values.")


# STEP 6: Calculate descriptive statistics

male_n = len(male_sales)
female_n = len(female_sales)

male_mean = np.mean(male_sales)
female_mean = np.mean(female_sales)

male_std = np.std(male_sales, ddof=1)
female_std = np.std(female_sales, ddof=1)

mean_difference = male_mean - female_mean

print("\n--- DESCRIPTIVE STATISTICS ---")

print(f"Male observations: {male_n}")
print(f"Female observations: {female_n}")

print(f"Male average sales: Rs. {male_mean:,.2f}")
print(f"Female average sales: Rs. {female_mean:,.2f}")

print(f"Male standard deviation: Rs. {male_std:,.2f}")
print(f"Female standard deviation: Rs. {female_std:,.2f}")

print(f"Mean difference (Male - Female): Rs. {mean_difference:,.2f}")


# STEP 7: Define the hypotheses

# H0: Mean male sales = mean female sales
# H1: Mean male sales != mean female sales

alpha = 0.05
confidence_level = 0.95

print("\n--- HYPOTHESIS ---")
print("H0: Average sales are equal between the two groups.")
print("H1: Average sales differ between the two groups.")
print("Significance level:", alpha)


# STEP 8: Perform Welch's independent two-sample t-test

t_statistic, p_value = stats.ttest_ind(
    male_sales,
    female_sales,
    equal_var=False,
    alternative="two-sided"
)

print("\n--- T-TEST RESULTS ---")
print(f"T-statistic: {t_statistic:.4f}")
print(f"P-value: {p_value:.4f}")


# STEP 9: Calculate Welch degrees of freedom

male_variance = np.var(male_sales, ddof=1)
female_variance = np.var(female_sales, ddof=1)

male_component = male_variance / male_n
female_component = female_variance / female_n

standard_error = np.sqrt(
    male_component + female_component
)

degrees_of_freedom = (
    (male_component + female_component) ** 2
    /
    (
        male_component ** 2 / (male_n - 1)
        +
        female_component ** 2 / (female_n - 1)
    )
)

# STEP 10: Calculate the 95% confidence interval

critical_t = stats.t.ppf(
    1 - (1 - confidence_level) / 2,
    degrees_of_freedom
)

margin_of_error = critical_t * standard_error

ci_lower = mean_difference - margin_of_error
ci_upper = mean_difference + margin_of_error

print("\n--- CONFIDENCE INTERVAL ---")
print(f"Degrees of freedom: {degrees_of_freedom:.2f}")
print(f"Standard error: Rs. {standard_error:,.2f}")
print(f"95% CI lower bound: Rs. {ci_lower:,.2f}")
print(f"95% CI upper bound: Rs. {ci_upper:,.2f}")


# STEP 11: Make the statistical decision

if p_value < alpha:
    decision = "Reject the null hypothesis"
    conclusion = (
        "There is statistically significant evidence "
        "that average sales differ between Male and Female groups."
    )
else:
    decision = "Fail to reject the null hypothesis"
    conclusion = (
        "There is insufficient evidence to conclude that "
        "average sales differ between Male and Female groups."
    )

print("\n--- FINAL CONCLUSION ---")
print("Decision:", decision)
print("Interpretation:", conclusion)


# STEP 12: Save the results as CSV files

group_summary = pd.DataFrame({
    "Gender": ["Male", "Female"],
    "Observations": [male_n, female_n],
    "Mean_Sales": [male_mean, female_mean],
    "Standard_Deviation": [male_std, female_std]
})

test_results = pd.DataFrame([{
    "Test": "Welch independent two-sample t-test",
    "Null_Hypothesis": "Male and Female mean sales are equal",
    "Alternative_Hypothesis": "Male and Female mean sales differ",
    "Alpha": alpha,
    "Male_Observations": male_n,
    "Female_Observations": female_n,
    "Male_Mean": male_mean,
    "Female_Mean": female_mean,
    "Mean_Difference_Male_Minus_Female": mean_difference,
    "T_Statistic": t_statistic,
    "Degrees_of_Freedom": degrees_of_freedom,
    "P_Value": p_value,
    "Confidence_Level": confidence_level,
    "CI_Lower": ci_lower,
    "CI_Upper": ci_upper,
    "Decision": decision,
    "Conclusion": conclusion
}])

group_summary.to_csv(
    OUTPUT_DIR / "gender_group_summary.csv",
    index=False
)

test_results.to_csv(
    OUTPUT_DIR / "hypothesis_test_results.csv",
    index=False
)

print("\nCSV results saved in:", OUTPUT_DIR)


# STEP 13: Create a bar chart of average sales

plt.figure(figsize=(8, 5))

plt.bar(
    ["Male", "Female"],
    [male_mean, female_mean]
)

plt.title("Average Sales by Gender")
plt.xlabel("Gender")
plt.ylabel("Average Total Sales (Rs.)")

plt.tight_layout()

chart_path = CHART_DIR / "gender_mean_sales.png"
plt.savefig(chart_path, dpi=300)
plt.close()

print("Chart saved at:", chart_path)
print("\nHypothesis testing completed successfully!")
