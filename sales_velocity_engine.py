"""
B2B Sales Velocity & Rep Quota Performance Engine
Author: Puneet Goswami
Description: Models B2B CRM pipeline stages, calculates mathematical Sales Velocity,
             and benchmarks rep-level quota achievement distributions.
"""

import numpy as np
import pandas as pd


def generate_crm_deals(n_deals: int = 5000) -> pd.DataFrame:
    """Simulates 6 months of enterprise B2B sales pipeline deals."""
    np.random.seed(42)

    rep_names = ["Alex Rivera", "David Chen", "Sarah Jenkins", "Michael Ross", "Priya Patel", "Marcus Vance"]
    territories = ["North America - West", "North America - East", "EMEA", "APAC"]
    stages = ["Discovery", "Demo / Evaluation", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]

    deal_reps = np.random.choice(rep_names, size=n_deals)
    deal_territory = np.random.choice(territories, size=n_deals, p=[0.40, 0.30, 0.20, 0.10])
    
    # Contract Value (ACV) lognormal distribution (Typical enterprise deal: $15k - $120k)
    deal_values = np.round(np.random.lognormal(mean=10.2, sigma=0.6, size=n_deals), -2)

    # Deal stage progression
    assigned_stage = np.random.choice(stages, size=n_deals, p=[0.20, 0.22, 0.18, 0.12, 0.16, 0.12])
    
    # Sales cycle length in days
    cycle_lengths = np.random.normal(loc=55, scale=20, size=n_deals).clip(10, 180).astype(int)

    return pd.DataFrame({
        "deal_id": [f"OPP-{10000 + i}" for i in range(n_deals)],
        "sales_rep": deal_reps,
        "territory": deal_territory,
        "deal_amount_usd": deal_values,
        "stage": assigned_stage,
        "cycle_days": cycle_lengths,
        "is_won": (assigned_stage == "Closed Won").astype(int)
    })


def compute_pipeline_metrics(df: pd.DataFrame):
    """Calculates sales velocity formula and quota pacing by representative."""
    quarterly_quota_per_rep = 450000.0  # $450k quarterly quota benchmark

    print("==========================================================================")
    print("B2B SALES PIPELINE VELOCITY & EXECUTIVE REVOPS SCORECARD")
    print("==========================================================================")

    # 1. Pipeline Stage Conversion Funnel
    stage_counts = df["stage"].value_counts()
    print("\n--- Current Pipeline Stage Distribution ---")
    for st, count in stage_counts.items():
        pct = (count / len(df)) * 100
        vol_usd = df[df["stage"] == st]["deal_amount_usd"].sum()
        print(f" - {st:20s}: {count:5d} deals ({pct:4.1f}%) | Pipeline: ${vol_usd:,.2f}")

    # 2. Rep-by-Rep Performance & Velocity Equation
    rep_groups = df.groupby("sales_rep")
    summary_rows = []

    for rep, group in rep_groups:
        opps = len(group)
        closed_deals = group[group["stage"].isin(["Closed Won", "Closed Lost"])]
        won_deals = group[group["stage"] == "Closed Won"]
        
        win_rate = (len(won_deals) / len(closed_deals)) if len(closed_deals) > 0 else 0.0
        avg_acv = won_deals["deal_amount_usd"].mean() if len(won_deals) > 0 else 0.0
        avg_cycle = won_deals["cycle_days"].mean() if len(won_deals) > 0 else 1.0
        closed_won_revenue = won_deals["deal_amount_usd"].sum()

        # Canonical Sales Velocity = (Opps * Win Rate * ACV) / Avg Cycle Days
        daily_velocity = (opps * win_rate * avg_acv) / avg_cycle if avg_cycle > 0 else 0.0
        quota_pct = (closed_won_revenue / quarterly_quota_per_rep) * 100

        summary_rows.append({
            "Sales_Rep": rep,
            "Total_Opps": opps,
            "Win_Rate_%": round(win_rate * 100, 1),
            "Avg_ACV_USD": round(avg_acv, 2),
            "Avg_Cycle_Days": round(avg_cycle, 1),
            "Closed_Won_USD": round(closed_won_revenue, 2),
            "Quota_Attainment_%": round(quota_pct, 1),
            "Daily_Velocity_USD": round(daily_velocity, 2)
        })

    summary_df = pd.DataFrame(summary_rows).sort_values("Daily_Velocity_USD", ascending=False)
    
    print("\n--- Sales Representative Velocity Scorecard ---")
    print(summary_df.to_string(index=False))

    team_velocity = summary_df["Daily_Velocity_USD"].sum()
    print(f"\nAggregate Team Pipeline Velocity: ${team_velocity:,.2f} / day")
    print(f"Projected Monthly Revenue Run-Rate: ${team_velocity * 30:,.2f} / month")


if __name__ == "__main__":
    deals = generate_crm_deals(5000)
    print(f"Loaded {len(deals):,} CRM pipeline opportunity records. Analyzing pipeline velocity...\n")
    compute_pipeline_metrics(deals)