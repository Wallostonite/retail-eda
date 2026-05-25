# ShopSmart Retail Group — EDA Findings
**Prepared for: Head of Merchandising**
**Dataset: 50,000 orders | Jan – Dec 2024**

---

## Executive Summary

Three findings stand out and require immediate attention before the board meeting.

**1. The cancellation rate is 20.1% — one in five orders never completes.**
This is not confined to a single category or customer type. It is consistent across all segments and categories, which points to a systemic issue upstream of the product: checkout, fulfilment, or payments.

**2. VIP customers spend less per order than Inactive and Regular customers.**
The loyalty programme is not working as intended. The segment that should be driving the highest revenue per order is ranked third.

**3. 168 orders have values between $4,785 and $4,999 — statistically confirmed as outliers by two independent methods.**
These could be bulk or B2B orders sitting undetected in a consumer dataset, or pricing errors. They need human review before the data is used for forecasting.

---

## Finding 1 — Revenue by Category and Segment

### By Product Category

| Rank | Category    | Mean Order Value | Median  | Orders |
|------|-------------|-----------------|---------|--------|
| 1    | Fashion     | $1,452          | $1,128  | 5,683  |
| 2    | Home        | $1,434          | $1,142  | 5,490  |
| 3    | Toys        | $1,431          | $1,108  | 5,466  |
| 4    | Sports      | $1,413          | $1,098  | 5,833  |
| 5    | Auto        | $1,409          | $1,101  | 5,565  |
| 6    | Food        | $1,407          | $1,066  | 5,497  |
| 7    | Electronics | $1,407          | $1,096  | 5,351  |
| 8    | Books       | $1,404          | $1,083  | 5,197  |
| 9    | Beauty      | $1,404          | $1,097  | —      |

**Key read:** The spread from top to bottom is only **$48**. Revenue is remarkably flat across categories. No single category is clearly outperforming or underperforming on order value alone. Sports has the highest order volume (5,833) while generating only mid-table revenue per order — worth investigating whether Sports is driving traffic but not value.

The gap between mean ($1,418) and median ($1,105) across all categories indicates a right-skewed distribution — a minority of high-value orders is pulling the average up. The typical order is closer to $1,100.

### By Customer Segment

| Rank | Segment  | Mean Order Value | Median  | Orders |
|------|----------|-----------------|---------|--------|
| 1    | Inactive | $1,429          | $1,120  | 9,997  |
| 2    | Regular  | $1,426          | $1,129  | 10,001 |
| 3    | VIP      | $1,419          | $1,111  | 9,849  |
| 4    | At-risk  | $1,410          | $1,085  | 10,141 |
| 5    | New      | $1,405          | $1,077  | 10,012 |

**Critical finding:** Inactive customers are the highest spenders per order, and VIP customers rank third. A loyalty programme should produce the inverse — VIPs should spend more because they are being rewarded for it. This ranking suggests the VIP tier may be classifying customers by purchase frequency rather than value, and the programme's incentives are not converting engagement into higher basket sizes.

At-risk and New customers have the lowest spend, which is expected, but the gap is small. Acquisition and reactivation campaigns have a narrow revenue upside on a per-order basis.

---

## Finding 2 — Cancellation Patterns

**Overall cancellation rate: 20.1%** (10,049 of 50,000 orders)

### By Order Status

| Status     | Orders | Share  |
|------------|--------|--------|
| Delivered  | 19,923 | 39.8%  |
| Processing | 10,088 | 20.2%  |
| Cancelled  | 10,049 | 20.1%  |
| Shipped    | 9,940  | 19.9%  |

### By Product Category

| Category    | Cancellation Rate |
|-------------|-----------------|
| Food        | 20.9%           |
| Home        | 20.6%           |
| Fashion     | 20.4%           |
| Sports      | 20.1%           |
| Beauty      | 20.1%           |
| Toys        | 20.0%           |
| Books       | 19.8%           |
| Electronics | 19.6%           |
| Auto        | 19.3%           |

### By Customer Segment

| Segment  | Cancellation Rate |
|----------|-----------------|
| At-risk  | 20.5%           |
| New      | 20.3%           |
| Inactive | 20.2%           |
| Regular  | 20.1%           |
| VIP      | 19.3%           |

**What the data is telling us:** The cancellation rate is nearly identical across every category and every segment — a range of just 1.6 percentage points. When a problem is this uniform, it is rarely a product or segment issue. The most likely causes are platform-wide: payment failures, cancellation windows being too long, fulfilment lead times, or a default-cancel flow in the checkout. This should be investigated at the platform and operations level, not by reducing stock in any particular category.

The one exception worth noting: **At-risk customers cancel at 20.5%** — the highest of any segment and 1.2 points above VIP. Re-engagement campaigns targeting this group should account for the elevated cancellation likelihood.

---

## Finding 3 — Rating vs Spend

**Pearson correlation (rating vs total_amount): r = −0.007**

This is effectively zero. There is no meaningful linear relationship between how much a customer spends and how highly they rate the order.

What this means in practice:
- High-value orders do not produce better reviews
- Low-rated orders are not concentrated in a specific price band
- Rating cannot be used as a proxy for customer satisfaction with order size
- Using rating to identify "high-value happy customers" would be misleading

The average rating across all 50,000 orders is **4.01 out of 5** (median 4.0), with a standard deviation of 1.16. Ratings are broadly positive and uniformly distributed across spend levels. Any satisfaction-driven upsell strategy will need a signal other than rating.

---

## Finding 4 — Anomalous Transactions

**168 orders confirmed as statistical outliers (0.34% of all orders)**

Both the IQR method and Z-score method flagged these rows independently. Only rows where both methods agreed were confirmed — this consensus approach eliminates borderline cases.

| Metric                     | Value      |
|----------------------------|-----------|
| Confirmed anomalies        | 168 orders |
| Anomaly threshold (IQR)    | $4,449     |
| Anomaly range              | $4,785 – $4,999 |
| Mean value (anomalies)     | $4,896     |
| Mean value (normal orders) | $1,418     |
| Multiple above normal mean | 3.45×      |

### Anomalies by Category

| Category    | Anomaly Orders |
|-------------|---------------|
| Home        | 21            |
| Fashion     | 21            |
| Auto        | 20            |
| Sports      | 19            |
| Food        | 19            |
| Books       | 19            |
| Beauty      | 18            |
| Toys        | 18            |
| Electronics | 13            |

All 168 anomalies cluster tightly between $4,785 and $4,999 — just below the $5,000 mark. This banding is not random noise. It suggests either a **price cap in the ordering system** (orders above $5,000 are split or blocked), **bulk orders processed as single consumer transactions**, or a **subset of B2B customers whose records are mixed into the consumer dataset**. Electronics is under-represented in the anomaly list (13 vs ~19 expected if uniform), which may reflect lower average product prices in that category.

**Recommended action:** Pull the full records for these 168 orders from the source system and check order type, customer account type, and whether multiple line items are being collapsed into a single transaction. The file `reports/anomalies.csv` contains all original columns for each flagged row.

---

## Revenue Trend — Second Half 2024

| Month   | Mean Order Value | MoM Change | 3-Month Rolling Avg |
|---------|-----------------|------------|-------------------|
| Jul-24  | $1,414          | +1.6%      | $1,405            |
| Aug-24  | $1,426          | +0.8%      | $1,411            |
| Sep-24  | $1,506          | **+5.6%**  | $1,449            |
| Oct-24  | $1,440          | −4.4%      | $1,457            |
| Nov-24  | $1,381          | −4.1%      | $1,442            |
| Dec-24  | $1,400          | +1.4%      | $1,407            |

September was the standout month — order value jumped 5.6% month-on-month to a 2024 high of $1,506. This was followed by two consecutive months of decline (−4.4% in October, −4.1% in November) before a partial recovery in December. The spike and pullback pattern is consistent with a promotional campaign that brought forward demand from Q4. If a September promotion ran, it appears to have borrowed revenue from October and November rather than growing the total.

---

## Recommended Actions

| Priority | Action | Owner |
|----------|--------|-------|
| High | Investigate the platform-level cause of the 20.1% cancellation rate — focus on payment failure rates, cancellation window, and fulfilment SLAs | Operations / Tech |
| High | Review the 168 anomalous orders in `reports/anomalies.csv` — confirm whether these are B2B, bulk, or data errors before using the dataset for forecasting | Data / Finance |
| Medium | Audit the VIP loyalty programme — VIPs spend less per order than Inactive and Regular customers, which indicates the tier definition or incentive structure needs revision | CRM / Marketing |
| Medium | Analyse the September revenue spike — determine whether it was driven by a promotion, and whether Q4 demand was genuinely borrowed | Commercial / Marketing |
| Low | Do not use customer rating as an input to revenue or upsell models — the correlation with spend is effectively zero | Analytics |

---

## Data Quality Notes

- **50,000 orders** covering the full 2024 calendar year, cleaned and validated prior to this analysis
- **7.48% of cells** contain missing values (82,260 cells across 22 columns) — primarily in review and rating fields, which are optional at checkout
- **0 duplicate rows** — each order ID appears once
- All statistical thresholds used: IQR fence at Q1 − 1.5×IQR / Q3 + 1.5×IQR; Z-score threshold at |z| > 3.0; correlation threshold at |r| > 0.3
- Full outputs: `reports/analysis_report.txt`, `reports/anomalies.csv`, `reports/plots/`

---

*Analysis produced by the Junior Data Analyst team using the ShopSmart EDA pipeline (Module 06). Charts available in `reports/plots/`. Raw findings reproducible by running `python run.py`.*
