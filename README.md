# ShopSmart Retail — Exploratory Data Analysis

**Company:** ShopSmart Retail Group
**Role:** Data Analyst
**Dataset:** 50,000 orders | January – December 2024

---

## Project Overview

Revenue is inconsistent across product categories and the cancellation rate has been rising, but the business lacked the numbers to pinpoint where the problem sits. This project delivers a full exploratory data analysis of the ShopSmart order dataset, ranking category performance, quantifying cancellation patterns, testing the relationship between customer ratings and spend, and flagging statistically anomalous transactions for investigation.

---

## What Was Built

### `EDAEngine` — Core Analysis Class

| Method | Description |
|---|---|
| `load()` | Loads `data/processed-data.csv`, excludes ID columns, identifies numeric and categorical types |
| `profile()` | Reports shape, data types, null rates, duplicates, memory usage, and descriptive statistics |
| `group_analysis(group_col, value_col)` | Grouped mean / median / std with rank — used to compare categories and segments |
| `correlation()` | Pearson correlation matrix across all numeric pairs; filters to |r| > 0.3 |
| `time_trends()` | Month-over-month mean, rolling 3-month average, and percentage change |
| `report(save=True)` | Prints a structured text report and writes `reports/analysis_report.txt` |

### `AnomalyDetector` — Statistical Outlier Flagging

| Method | Description |
|---|---|
| `run(columns)` | IQR and Z-score methods run independently per column |
| `save_anomalies()` | Saves rows confirmed by both methods to `reports/anomalies.csv` |
| `summary()` | Returns per-column anomaly counts as a DataFrame |

Consensus approach: a row is confirmed only if both IQR **and** Z-score flag it, reducing false positives.

### `Visualiser` — Chart Generator

Five charts saved to `reports/plots/`:
1. Revenue by product category (bar chart)
2. Order status breakdown (count chart)
3. Customer segment revenue comparison (bar chart)
4. Rating vs total amount (scatter)
5. Anomaly scatter — flagged vs normal transactions

### Jupyter Notebook

`notebooks/retail_analysis.ipynb` — interactive version of all five charts with inline analysis.

---

## Key Findings

| Question | Finding |
|---|---|
| Revenue by category | Spread from top to bottom category is only $48 — revenue is flat across all nine categories |
| Revenue by segment | VIP customers spend **less** per order than Inactive customers — the loyalty programme is not converting engagement into basket size |
| Cancellation rate | **20.1%** of all orders cancelled; rate is uniform across every category and segment (range: 1.6 pp) — a systemic platform issue, not a product issue |
| Rating vs spend | Pearson r = **−0.007** — effectively no relationship |
| Anomalous transactions | **168 orders** confirmed as outliers ($4,785–$4,999); all cluster just below $5,000, suggesting a system price cap or B2B orders in a consumer dataset |

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python run.py

# Run unit tests
python tests/test_eda.py
```

---

## Project Structure

```
retail-eda/
├── data/
│   └── processed-data.csv        # 50,000 orders, cleaned
├── reports/
│   ├── analysis_report.txt       # Full EDA text report
│   ├── anomalies.csv             # 168 flagged transactions
│   └── plots/                    # 5 PNG charts
├── notebooks/
│   └── retail_analysis.ipynb     # Interactive analysis
├── src/
│   ├── eda_engine.py             # EDAEngine class
│   ├── anomaly_detector.py       # AnomalyDetector class
│   └── visualiser.py             # Visualiser class
├── tests/
│   └── test_eda.py               # 11 unit tests
├── config.py
└── run.py                        # Pipeline entry point
```

---

## Dataset Reference

| Column | Type | Description |
|---|---|---|
| `order_id` | int | Unique order identifier |
| `order_date` | date | Date of order |
| `total_amount` | float | Order value in USD (4.67 – 4,999) |
| `order_status` | category | Delivered / Shipped / Processing / Cancelled |
| `customer_segment` | category | VIP / Regular / New / At-risk / Inactive |
| `product_category` | category | Beauty / Sports / Fashion / Auto / Food / Home / Toys / Electronics |
| `product_price` | float | Listed unit price |
| `seller_category` | category | Seller's primary product category |
| `rating` | float | Customer review score (1–5) |

---

## Tests

11 unit tests covering profile accuracy, group analysis ranking, correlation threshold enforcement, anomaly consensus logic, and data immutability.

```bash
python tests/test_eda.py
# All tests passed ✓
```

---

## Outputs

| File | Description |
|---|---|
| `reports/analysis_report.txt` | Full structured EDA report |
| `reports/anomalies.csv` | 168 statistically confirmed outlier transactions |
| `reports/plots/` | 5 PNG charts |
| `notebooks/retail_analysis.ipynb` | Interactive notebook |
| `BUSINESS.md` | Board-ready presentation of findings |
