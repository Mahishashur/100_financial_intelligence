import pandas as pd


def calculate_peer_rankings(merged_df):

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

        peer_df[metric + "_percentile"] = (

            peer_df
            .groupby("peer_group_name")[metric]
            .rank(
                method="average",
                pct=True
            )

        )

    peer_df["debt_to_equity_percentile"] = (

        1 -

        peer_df
        .groupby("peer_group_name")["debt_to_equity"]
        .rank(
            method="average",
            pct=True
        )

    )

    return peer_df