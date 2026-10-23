# ApexPlanet Data Analytics Internship – Task 4
## Data Storytelling & Statistical Validation

## 📌 Project Overview

This project is part of my Data Analytics Internship at ApexPlanet. The objective is to transform the results of previous data analytics tasks into a meaningful business story and use statistical hypothesis testing to validate a business question.

The project combines data analysis, business intelligence, statistical testing, visualization, and actionable recommendations to support data-driven decision-making.

## 🎯 Project Objectives

- Summarize key findings from previous data analytics tasks.
- Communicate business insights through data storytelling.
- Analyze sales performance and customer segments.
- Formulate a testable business hypothesis.
- Perform statistical hypothesis testing using Python.
- Interpret p-values and 95% confidence intervals.
- Present findings through charts, reports, and a PowerPoint presentation.
- Recommend business actions based on analytical evidence.

## 🗂️ Dataset Description

The project uses a cleaned sales transaction dataset prepared during the earlier internship tasks.

**Dataset summary:**
- Total transaction records: 1,000
- Total sales: approximately ₹139.40 million
- Total units sold: 5,435
- Analysis period: 2025

**Important columns:**

| Column | Description |
|---|---|
| `Transaction_ID` | Unique transaction record identifier |
| `Order_ID` | Order identifier from the source data |
| `Order_Date` | Date of the transaction |
| `Gender` | Customer gender |
| `City` | Customer city |
| `Product` | Purchased product |
| `Category` | Product category |
| `Quantity` | Number of units purchased |
| `Unit_Price` | Price per unit |
| `Total_Sales` | Total sales amount for the record |

## 🛠️ Tools and Technologies

- **Python** – Data analysis and statistical testing
- **Pandas** – Data manipulation and aggregation
- **SciPy** – Statistical hypothesis testing
- **Matplotlib** – Data visualization
- **Microsoft Power BI** – Interactive dashboarding in the previous task
- **Microsoft PowerPoint** – Business presentation and storytelling
- **GitHub** – Project documentation and version control

## 🔄 Project Workflow

### 1. Business Understanding

The main objective is to understand sales performance, explore customer and product patterns, and communicate findings that can support business decisions.

### 2. Data Analysis and Business Storytelling

The cleaned sales dataset was analyzed to summarize key performance indicators and explore sales patterns.

Key metrics include:
- Total Sales
- Transaction Records
- Total Units Sold
- Average Sales per Transaction Record
- Category-wise Sales
- Monthly Sales Trends

The analysis helps organize raw sales data into meaningful business information.

### 3. Hypothesis Formulation

**Business question:**

Do average sales per transaction record differ between male and female customers?

**Null Hypothesis (H₀):**

The population mean sales per transaction record are equal for male and female groups.

**Alternative Hypothesis (H₁):**

The population mean sales per transaction record differ between male and female groups.

### 4. Statistical Hypothesis Testing

A **Welch independent-samples t-test** was selected to compare the mean sales of two independent groups without assuming equal population variances.

**Test configuration:**
- Statistical test: Welch's independent-samples t-test
- Test type: Two-tailed
- Significance level (α): 0.05
- Confidence level: 95%
- Outcome variable: `Total_Sales`
- Grouping variable: `Gender`

The p-value and 95% confidence interval were used to evaluate the evidence for a difference in average sales.

### 5. Hypothesis Testing Results

| Metric | Male | Female |
|---|---:|---:|
| Transaction records | 511 | 489 |
| Mean sales per record | ₹141,807.34 | ₹136,883.21 |

**Statistical results:**

- Mean difference (Male − Female): ₹4,924.13
- t-statistic: 0.6826
- Degrees of freedom: 997.98
- p-value: 0.4950
- 95% confidence interval: −₹9,231.58 to ₹19,079.85

**Interpretation:**

The p-value of 0.4950 is greater than the significance level of 0.05. The 95% confidence interval also includes zero.

Therefore, we **fail to reject the null hypothesis**. The analysis does not provide sufficient statistical evidence of a difference in mean sales per transaction record between the two groups.

This does not prove that the group means are exactly equal. The result applies to the supplied dataset and should not be interpreted as evidence that gender causes sales outcomes.

### 6. Data Visualization

The Python analysis generates visualizations to support the business story:

- Mean sales per transaction record by gender
- Monthly sales trend
- Total sales by product category

These charts help communicate the findings clearly and make patterns easier to explore.

### 7. Business Insights and Recommendations

Based on the analysis, the following actions are recommended:

1. Monitor total sales, units sold, and average sales per record regularly.
2. Investigate category-wise and city-wise sales performance.
3. Review monthly sales trends to support inventory and sales planning.
4. Avoid gender-based marketing decisions based on this test alone.
5. Validate future business hypotheses with appropriate statistical methods.
6. Use a properly designed randomized A/B test when evaluating the impact of a new campaign or website change.

## 📂 Project Structure

```text
ApexPlanet-Task4-Data-Storytelling-Statistical-Validation/
│
├── data/
│   └── cleaned_sales_dataset.csv
│
├── src/
│   └── task4_analysis.py
│
├── outputs/
│   ├── headline_kpis.csv
│   ├── gender_group_summary.csv
│   ├── hypothesis_test_results.csv
│   ├── monthly_sales.csv
│   ├── category_sales.csv
│   ├── analysis_report.md
│   └── charts/
│       ├── gender_mean_sales.png
│       ├── monthly_sales_trend.png
│       └── category_sales.png
│
├── presentation/
│   └── ApexPlanet_Task4_Data_Storytelling_Statistical_Validation.pptx
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ▶️ How to Run the Project

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ApexPlanet-Task4-Data-Storytelling-Statistical-Validation
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the analysis

```bash
python src/task4_analysis.py
```

The script generates KPI summaries, hypothesis test results, monthly and category sales tables, a Markdown report, and charts inside the `outputs/` folder.

## 📚 Key Learnings

- Translating analytical results into a business narrative.
- Formulating null and alternative hypotheses.
- Performing a Welch t-test using Python and SciPy.
- Interpreting p-values and confidence intervals.
- Distinguishing statistical significance from practical business importance.
- Creating charts to communicate findings.
- Converting analytical evidence into business recommendations.

## ⚠️ Limitations

- The analysis is based on the supplied sales transaction dataset.
- Transaction records should not automatically be treated as unique customers or unique orders.
- The gender comparison is observational and does not establish causation.
- Other factors, including product category, city, and purchase mix, may influence the observed results.
- Statistical conclusions should be considered alongside business context and additional analysis.

## ✅ Conclusion

This project demonstrates how data analysis and statistical validation can be combined to support business decision-making. By analyzing sales metrics, visualizing trends, performing hypothesis testing, and communicating the results, the project provides a practical example of the data analytics workflow.

The key lesson is that business decisions should be based not only on visible differences in charts or averages but also on statistical evidence, uncertainty, and the wider business context.

## 👨‍💻 Author

**Santosh Kumar Lakkoju**

Aspiring Data Analyst | Python | SQL Server | Excel | Power BI

**Project:** ApexPlanet Data Analytics Internship – Task 4  
**Focus:** Data Storytelling, Statistical Hypothesis Testing, and Business Insights
