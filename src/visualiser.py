# ================================================================
# src/visualiser.py — Chart generation for ShopSmart Retail EDA
# ================================================================
# Generates and saves 4 PNG charts that answer the README business
# questions. Saves to reports/plots/ so the team can review without
# needing to open a notebook.
# ================================================================

import sys
import pathlib

_root = pathlib.Path(__file__).resolve().parent
while not (_root / "config.py").exists() and _root != _root.parent:
    _root = _root.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import matplotlib
matplotlib.use("Agg")   # non-interactive backend — writes files, no pop-up window
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from config import REPORTS_DIR, logger

PLOTS_DIR = REPORTS_DIR / "plots"

sns.set_theme(style="whitegrid", palette="muted", font_scale=1.05)


class Visualiser:
    """
    Generates the 4 charts required by the README.

    Chart 1 — Revenue by category         (Q1: which category earns most?)
    Chart 2 — Order status breakdown      (Q2: where do cancellations sit?)
    Chart 3 — Customer segment comparison (Q1: which segment spends most?)
    Chart 4 — Anomaly scatter             (Q4: which orders are outliers?)

    Usage:
        vis = Visualiser(engine.df, detector.confirmed)
        vis.run_all()   # saves all 4 charts to reports/plots/
    """

    def __init__(self, df: pd.DataFrame, anomaly_df: pd.DataFrame = None):
        self.df         = df
        self.anomaly_df = anomaly_df if anomaly_df is not None else pd.DataFrame()
        PLOTS_DIR.mkdir(exist_ok=True)

    # ── CHART 1 ──────────────────────────────────────────────────────

    def revenue_by_category(self) -> pathlib.Path:
        """Horizontal bar chart: mean total_amount by product_category."""
        agg = (
            self.df.groupby("product_category")["total_amount"]
            .mean()
            .sort_values(ascending=True)
            .round(2)
        )

        fig, ax = plt.subplots(figsize=(9, 6))
        palette = sns.color_palette("Blues_r", len(agg))
        bars = ax.barh(agg.index, agg.values, color=palette, edgecolor="white")

        ax.set_xlabel("Mean Order Value (USD)", fontsize=12)
        ax.set_title("Q1 — Mean Revenue by Product Category", fontsize=14, fontweight="bold")

        for bar, val in zip(bars, agg.values):
            ax.text(val + 8, bar.get_y() + bar.get_height() / 2,
                    f"${val:,.0f}", va="center", fontsize=10)

        ax.set_xlim(0, agg.max() * 1.18)
        plt.tight_layout()
        path = PLOTS_DIR / "01_revenue_by_category.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info(f"[PLOT] Saved: {path.name}")
        return path

    # ── CHART 2 ──────────────────────────────────────────────────────

    def order_status_breakdown(self) -> pathlib.Path:
        """Bar chart: order count by status, cancellations highlighted in red."""
        counts      = self.df["order_status"].value_counts().sort_values(ascending=False)
        cancel_rate = counts.get("Cancelled", 0) / len(self.df) * 100

        colors = ["#e74c3c" if s == "Cancelled" else "#3498db" for s in counts.index]

        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(counts.index, counts.values, color=colors, edgecolor="white", width=0.6)

        ax.set_ylabel("Number of Orders", fontsize=12)
        ax.set_title(
            f"Q2 — Order Status Breakdown  (cancellation rate: {cancel_rate:.1f}%)",
            fontsize=13, fontweight="bold"
        )

        for bar, val in zip(bars, counts.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 80,
                    f"{val:,}", ha="center", fontsize=10)

        plt.tight_layout()
        path = PLOTS_DIR / "02_order_status_breakdown.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info(f"[PLOT] Saved: {path.name}")
        return path

    # ── CHART 3 ──────────────────────────────────────────────────────

    def customer_segment_comparison(self) -> pathlib.Path:
        """Bar chart: mean total_amount by customer_segment vs overall average."""
        agg          = (
            self.df.groupby("customer_segment")["total_amount"]
            .mean()
            .sort_values(ascending=False)
            .round(2)
        )
        overall_mean = self.df["total_amount"].mean()

        colors = ["#2ecc71" if v >= overall_mean else "#e74c3c" for v in agg.values]

        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.bar(agg.index, agg.values, color=colors, edgecolor="white", width=0.55)

        ax.axhline(overall_mean, color="navy", linestyle="--", linewidth=1.5,
                   label=f"Overall mean  ${overall_mean:,.0f}")
        ax.set_ylabel("Mean Order Value (USD)", fontsize=12)
        ax.set_title("Q1 — Customer Segment Comparison", fontsize=13, fontweight="bold")
        ax.legend(fontsize=10)

        for bar, val in zip(bars, agg.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                    f"${val:,.0f}", ha="center", fontsize=10)

        ax.set_ylim(0, agg.max() * 1.15)
        plt.tight_layout()
        path = PLOTS_DIR / "03_customer_segment_comparison.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info(f"[PLOT] Saved: {path.name}")
        return path

    # ── CHART 4 ──────────────────────────────────────────────────────

    def anomaly_scatter(self) -> pathlib.Path:
        """Scatter plot: total_amount with anomaly rows highlighted in red."""
        normal_df = self.df.copy()
        if len(self.anomaly_df) > 0:
            normal_df = normal_df[~normal_df.index.isin(self.anomaly_df.index)]

        sample = normal_df.sample(min(2000, len(normal_df)), random_state=42)

        fig, ax = plt.subplots(figsize=(11, 5))
        ax.scatter(sample.index, sample["total_amount"],
                   alpha=0.25, s=8, color="#3498db", label="Normal orders")

        if len(self.anomaly_df) > 0:
            ax.scatter(self.anomaly_df.index, self.anomaly_df["total_amount"],
                       alpha=0.85, s=35, color="#e74c3c", zorder=5,
                       label=f"Anomalies — {len(self.anomaly_df):,} rows (IQR + Z-score)")

        ax.set_xlabel("Row index", fontsize=12)
        ax.set_ylabel("Total Amount (USD)", fontsize=12)
        ax.set_title("Q4 — Anomaly Detection on Total Amount",
                     fontsize=13, fontweight="bold")
        ax.legend(fontsize=10)
        plt.tight_layout()
        path = PLOTS_DIR / "04_anomaly_scatter.png"
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        logger.info(f"[PLOT] Saved: {path.name}")
        return path

    # ── RUN ALL ───────────────────────────────────────────────────────

    def run_all(self) -> list:
        """Generate all 4 charts and return their file paths."""
        paths = [
            self.revenue_by_category(),
            self.order_status_breakdown(),
            self.customer_segment_comparison(),
            self.anomaly_scatter(),
        ]
        logger.info(f"[PLOT] All {len(paths)} charts saved → {PLOTS_DIR}")
        return paths
