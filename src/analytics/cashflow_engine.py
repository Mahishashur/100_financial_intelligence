from ratios import (
    calculate_free_cash_flow,
    calculate_cfo_quality,
    calculate_fcf_conversion,
    calculate_capex_intensity,
    calculate_ocf_margin,
    calculate_cash_conversion_ratio,
    calculate_cash_reinvestment_ratio
)


def add_cashflow_kpis(df):

    # Free Cash Flow
    df["free_cash_flow"] = df.apply(
        lambda row: calculate_free_cash_flow(
            row["operating_activity"],
            row["investing_activity"]
        ),
        axis=1
    )

    # CFO Quality
    df["cfo_quality"] = df.apply(
        lambda row: calculate_cfo_quality(
            row["operating_activity"],
            row["net_profit"]
        ),
        axis=1
    )

    # FCF Conversion
    df["fcf_conversion"] = df.apply(
        lambda row: calculate_fcf_conversion(
            row["free_cash_flow"],
            row["net_profit"]
        ),
        axis=1
    )

    # Capex Intensity
    df["capex_intensity"] = df.apply(
        lambda row: calculate_capex_intensity(
            row["investing_activity"],
            row["operating_activity"]
        ),
        axis=1
    )

    # OCF Margin
    df["ocf_margin"] = df.apply(
        lambda row: calculate_ocf_margin(
            row["operating_activity"],
            row["sales"]
        ),
        axis=1
    )

    # Cash Conversion Ratio
    df["cash_conversion_ratio"] = df.apply(
        lambda row: calculate_cash_conversion_ratio(
            row["operating_activity"],
            row["net_profit"]
        ),
        axis=1
    )

    # Cash Reinvestment Ratio
    df["cash_reinvestment_ratio"] = df.apply(
        lambda row: calculate_cash_reinvestment_ratio(
            row["operating_activity"],
            row["total_assets"]
        ),
        axis=1
    )

    return df