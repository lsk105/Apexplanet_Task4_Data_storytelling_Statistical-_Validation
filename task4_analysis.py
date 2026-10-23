"""ApexPlanet Task 4: Data storytelling and hypothesis testing.
Run from repository root: python src/task4_analysis.py
"""
from pathlib import Path
import math
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "cleaned_sales_dataset.csv"
OUT = ROOT / "outputs"
CHARTS = OUT / "charts"
OUT.mkdir(exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

def main():
    df = pd.read_csv(DATA, parse_dates=["Order_Date"])
    required = {"Total_Sales", "Gender", "Quantity", "Category", "Order_Date"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Required columns missing: {sorted(missing)}")

    df["Total_Sales"] = pd.to_numeric(df["Total_Sales"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Gender"] = df["Gender"].astype("string").str.strip()
    total_sales = df["Total_Sales"].sum()
    n_records = len(df)
    units = df["Quantity"].sum()

    pd.DataFrame([
        {"metric": "Total sales", "value": total_sales},
        {"metric": "Transaction records", "value": n_records},
        {"metric": "Units sold", "value": units},
        {"metric": "Average sales per record", "value": total_sales / n_records},
        {"metric": "Distinct categories", "value": df["Category"].nunique()},
    ]).to_csv(OUT / "headline_kpis.csv", index=False)

    male = df.loc[df["Gender"].eq("Male"), "Total_Sales"].dropna()
    female = df.loc[df["Gender"].eq("Female"), "Total_Sales"].dropna()
    if len(male) < 2 or len(female) < 2:
        raise ValueError("Not enough observations in one or both gender groups.")

    test = stats.ttest_ind(male, female, equal_var=False, alternative="two-sided")
    diff = male.mean() - female.mean()
    a = male.var(ddof=1) / len(male)
    b = female.var(ddof=1) / len(female)
    standard_error = math.sqrt(a + b)
    dof = (a + b) ** 2 / (a ** 2 / (len(male) - 1) + b ** 2 / (len(female) - 1))
    critical = stats.t.ppf(0.975, dof)
    ci_low, ci_high = diff - critical * standard_error, diff + critical * standard_error
    p_value = float(test.pvalue)
    decision = "Reject H0" if p_value < 0.05 else "Fail to reject H0"
    conclusion = ("Statistically significant difference at alpha = 0.05."
                  if p_value < 0.05 else
                  "Insufficient evidence of a statistically significant difference at alpha = 0.05.")

    summary = pd.DataFrame([
        {"group": "Male", "n_records": len(male), "mean_sales": male.mean(), "std_dev": male.std(ddof=1)},
        {"group": "Female", "n_records": len(female), "mean_sales": female.mean(), "std_dev": female.std(ddof=1)},
    ])
    summary.to_csv(OUT / "gender_group_summary.csv", index=False)
    pd.DataFrame([{
        "test": "Welch independent-samples t-test (two-sided)",
        "alpha": 0.05, "male_n": len(male), "female_n": len(female),
        "male_mean": male.mean(), "female_mean": female.mean(),
        "mean_difference_male_minus_female": diff,
        "t_statistic": float(test.statistic), "degrees_of_freedom_welch": dof,
        "p_value": p_value, "ci95_lower": ci_low, "ci95_upper": ci_high,
        "decision": decision, "conclusion": conclusion,
    }]).to_csv(OUT / "hypothesis_test_results.csv", index=False)

    monthly = (df.dropna(subset=["Order_Date"])
               .assign(Month=lambda x: x["Order_Date"].dt.to_period("M").astype(str))
               .groupby("Month", as_index=False)["Total_Sales"].sum())
    monthly.to_csv(OUT / "monthly_sales.csv", index=False)
    category = (df.groupby("Category", dropna=False)
                .agg(Records=("Total_Sales", "size"), Total_Sales=("Total_Sales", "sum"))
                .reset_index().sort_values("Total_Sales", ascending=False))
    category.to_csv(OUT / "category_sales.csv", index=False)

    plt.figure(figsize=(8, 5))
    plt.bar(summary["group"], summary["mean_sales"])
    plt.title("Mean Sales per Transaction Record by Gender")
    plt.ylabel("Mean Total_Sales")
    plt.xlabel("Gender group")
    plt.tight_layout()
    plt.savefig(CHARTS / "gender_mean_sales.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(monthly["Month"], monthly["Total_Sales"], marker="o")
    plt.title("Monthly Sales Trend")
    plt.ylabel("Total sales")
    plt.xlabel("Month")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(CHARTS / "monthly_sales_trend.png", dpi=160)
    plt.close()

    plot_category = category.sort_values("Total_Sales", ascending=True)
    plt.figure(figsize=(8, 5))
    plt.barh(plot_category["Category"].astype(str), plot_category["Total_Sales"])
    plt.title("Total Sales by Category")
    plt.xlabel("Total sales")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(CHARTS / "category_sales.png", dpi=160)
    plt.close()

    report = f"""# Task 4 — Analysis Results

## Headline metrics
- Total sales: ₹{total_sales:,.2f}
- Transaction records: {n_records:,}
- Units sold: {units:,.0f}
- Average sales per record: ₹{total_sales/n_records:,.2f}

## Hypothesis
- H₀: Male and female groups have equal population mean sales per transaction record.
- H₁: Their population mean sales per transaction record differs.
- Test: two-sided Welch independent-samples t-test; α = 0.05.

| Group | n | Mean sales per record | Standard deviation |
|---|---:|---:|---:|
| Male | {len(male)} | ₹{male.mean():,.2f} | ₹{male.std(ddof=1):,.2f} |
| Female | {len(female)} | ₹{female.mean():,.2f} | ₹{female.std(ddof=1):,.2f} |

- Mean difference (male − female): ₹{diff:,.2f}
- t-statistic: {float(test.statistic):.4f}
- Welch degrees of freedom: {dof:.2f}
- p-value: {p_value:.4f}
- 95% confidence interval: ₹{ci_low:,.2f} to ₹{ci_high:,.2f}
- Decision: **{decision}**
- Interpretation: {conclusion}

## Business interpretation
The result does not prove that group means are identical. It means the sample does not provide enough evidence of a difference at the 5% significance level. This is observational data and does not support causal claims. Consider product/category, city, and time mix before taking action.

## Files created
- `headline_kpis.csv`
- `gender_group_summary.csv`
- `hypothesis_test_results.csv`
- `monthly_sales.csv`
- `category_sales.csv`
- `charts/gender_mean_sales.png`
- `charts/monthly_sales_trend.png`
- `charts/category_sales.png`
"""
    (OUT / "analysis_report.md").write_text(report, encoding="utf-8")
    print(report)

if __name__ == "__main__":
    main()
