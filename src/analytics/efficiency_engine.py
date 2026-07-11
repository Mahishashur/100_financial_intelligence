from ratios import (
    calculate_asset_turnover,
    calculate_capital_employed_turnover,
    calculate_net_asset_turnover
)


def add_efficiency_kpis(df):

    # Asset Turnover
    df["asset_turnover"] = df.apply(
        lambda row: calculate_asset_turnover(
            row["sales"],
            row["total_assets"]
        ),
        axis=1
    )

    # Capital Employed Turnover
    df["capital_employed_turnover"] = df.apply(
        lambda row: calculate_capital_employed_turnover(
            row["sales"],
            row["equity_capital"],
            row["reserves"],
            row["borrowings"]
        ),
        axis=1
    )

    # Net Asset Turnover
    df["net_asset_turnover"] = df.apply(
        lambda row: calculate_net_asset_turnover(
            row["sales"],
            row["total_assets"],
            row["investments"]
        ),
        axis=1
    )

    return df