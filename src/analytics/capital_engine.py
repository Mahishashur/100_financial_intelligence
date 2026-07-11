from ratios import (
    calculate_investment_ratio,
    calculate_fixed_asset_ratio,
    calculate_reserve_to_equity_ratio,
    calculate_retention_ratio
)


def add_capital_kpis(df):

    # Investment Ratio
    df["investment_ratio"] = df.apply(
        lambda row: calculate_investment_ratio(
            row["investments"],
            row["total_assets"]
        ),
        axis=1
    )

    # Fixed Asset Ratio
    df["fixed_asset_ratio"] = df.apply(
        lambda row: calculate_fixed_asset_ratio(
            row["fixed_assets"],
            row["total_assets"]
        ),
        axis=1
    )

    # Reserve to Equity Ratio
    df["reserve_to_equity_ratio"] = df.apply(
        lambda row: calculate_reserve_to_equity_ratio(
            row["reserves"],
            row["equity_capital"]
        ),
        axis=1
    )

    # Retention Ratio
    df["retention_ratio"] = df.apply(
        lambda row: calculate_retention_ratio(
            row["dividend_payout"]
        ),
        axis=1
    )

    return df