import os
import numpy as np
import matplotlib.pyplot as plt


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

    angles = np.linspace(
        0,
        2 * np.pi,
        len(metrics),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    fig = plt.figure(figsize=(6, 6))

    ax = plt.subplot(111, polar=True)

    ax.plot(
        angles,
        values,
        linewidth=2
    )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(metrics)

    plt.title(
        company_df.iloc[0]["company_id"]
    )

    filepath = os.path.join(

        "reports",

        "radar_charts",

        f'{company_df.iloc[0]["company_id"]}_radar.png'

    )

    plt.savefig(
        filepath,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

def generate_radar_charts(peer_df):

    os.makedirs(
        "reports/radar_charts",
        exist_ok=True
    )

    for company in peer_df["company_id"].unique():

        company_df = peer_df[
            peer_df["company_id"] == company
        ].tail(1)

        create_radar_chart(company_df)

    print("\n✓ Radar charts created successfully.")