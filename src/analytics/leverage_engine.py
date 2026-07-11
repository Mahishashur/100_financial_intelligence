from ratios import (
    calculate_debt_to_equity,
    calculate_interest_coverage,
    calculate_net_debt,
    calculate_financial_leverage,
    calculate_debt_ratio
)


def add_leverage_kpis(df):

    # Debt to Equity
    df["debt_to_equity"] = df.apply(
        lambda row: calculate_debt_to_equity(
            row["borrowings"],
            row["equity_capital"],
            row["reserves"]
        ),
        axis=1
    )

    # Interest Coverage
    df["interest_coverage"] = df.apply(
        lambda row: calculate_interest_coverage(
            row["operating_profit"],
            row["other_income"],
            row["interest"]
        ),
        axis=1
    )

    # Net Debt
    df["net_debt"] = df.apply(
        lambda row: calculate_net_debt(
            row["borrowings"],
            row["operating_activity"]
        ),
        axis=1
    )

    # Financial Leverage
    df["financial_leverage"] = df.apply(
        lambda row: calculate_financial_leverage(
            row["total_assets"],
            row["equity_capital"],
            row["reserves"]
        ),
        axis=1
    )

    # Debt Ratio
    df["debt_ratio"] = df.apply(
        lambda row: calculate_debt_ratio(
            row["borrowings"],
            row["total_assets"]
        ),
        axis=1
    )

    return df