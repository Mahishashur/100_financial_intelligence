import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np

# Load financial KPI dataset

kpi_df = pd.read_csv(
    "data/output/financial_kpis.csv"
)

# Load peer groups

peer_df = pd.read_excel(
    "data/raw/supplementary/peer_groups_generate.xlsx"
)

# Merge

merged_df = kpi_df.merge(peer_df,
    on="company_id",
    how="left"

)

print("\nFinancial KPI Rows :", len(kpi_df))
print("Peer Group Rows    :", len(peer_df))
print("Merged Rows        :", len(merged_df))

peer_df = merged_df.dropna(
    subset=["peer_group_name"]
).copy()


metrics = [

    "roe_calculated_pct",

    "roce_calculated_pct",

    "net_profit_margin_pct",

    "free_cash_flow",

    "profit_cagr_5yr",

    "sales_cagr_5yr",

    "interest_coverage",

    "asset_turnover"

]


for metric in metrics:

    peer_df[metric + "_percentile"] = (peer_df
        .groupby("peer_group_name")[metric]
        .rank(
            method="average",pct=True)
    )


# Debt to Equity
# Lower is Better

peer_df["debt_to_equity_percentile"] = (1 -peer_df
    .groupby("peer_group_name")["debt_to_equity"]
    .rank(
        method="average",
        pct=True )

)

print("\nPeer Ranking Sample\n")
print(

    peer_df[[
            "company_id",
            "peer_group_name",
            "roe_calculated_pct_percentile",
            "roce_calculated_pct_percentile",
            "net_profit_margin_pct_percentile",
            "debt_to_equity_percentile"
        ]].head(20)
)

# Save to SQLite

conn = sqlite3.connect( "data/output/financial.db")
peer_df.to_sql("peer_percentiles",conn,if_exists="replace",
    index=False
)
conn.close()
print("\npeer_percentiles table created successfully.")

# Export peer comparison Excel

with pd.ExcelWriter(
    "output/peer_comparison.xlsx",
    engine="openpyxl"
) as writer:

    for group in sorted(
        peer_df["peer_group_name"].dropna().unique()
    ):

        sheet = peer_df[
            peer_df["peer_group_name"] == group
        ]

        sheet.to_excel(
            writer,
            sheet_name=group[:31],
            index=False
        )

print("\npeer_comparison.xlsx created successfully.")

# Radar chart function

def create_radar_chart(company_df):

    metrics = [
        "roe_calculated_pct",
        "roce_calculated_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow",
        "profit_cagr_5yr",
        "sales_cagr_5yr",
        "composite_quality_score"
    ]

    values = company_df.iloc[0][metrics].fillna(0).tolist()
    values += values[:1]

    angles = np.linspace(0,2 * np.pi,len(metrics),endpoint=False
    ).tolist()

    angles += angles[:1]
    fig = plt.figure(figsize=(6,6))
    ax = plt.subplot(111, polar=True)
    
    ax.plot(angles,values,linewidth=2)

    ax.fill(angles,values,alpha=0.25)

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(metrics)

    plt.title(company_df.iloc[0]["company_id"])

    filepath = os.path.join(
        "reports",
        "radar_charts",
        f'{company_df.iloc[0]["company_id"]}_radar.png'

    )

    print(filepath)
    plt.savefig(

        filepath,
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()

# Generate charts

for company in peer_df["company_id"].unique():

    company_df = peer_df[
        peer_df["company_id"] == company
    ].tail(1)
    create_radar_chart(company_df)
print("\nRadar charts created successfully.")


all_companies = set(kpi_df["company_id"].unique())

mapped_companies = set(peer_df["company_id"].unique())

missing = sorted(all_companies - mapped_companies)

print("Missing Companies :", len(missing))

for company in missing:
    print(company)
