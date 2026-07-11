from ratios import (

    calculate_npm,
    calculate_opm,
    calculate_roe,
    calculate_roce,
    calculate_roa

)


def add_profitability_kpis(df):

    df["net_profit_margin_pct"] = df.apply(

        lambda row:

        calculate_npm(

            row["sales"],
            row["net_profit"]

        ),axis=1
    )

    df["opm_calculated_pct"] = df.apply(

        lambda row:

        calculate_opm(

            row["sales"],
            row["operating_profit"]

        ),axis=1
    )

    df["roe_calculated_pct"] = df.apply(

        lambda row:

        calculate_roe(

            row["net_profit"],
            row["equity_capital"],
            row["reserves"]

        ),axis=1
    )

    df["roce_calculated_pct"] = df.apply(

        lambda row:

        calculate_roce(

            row["operating_profit"],
            row["equity_capital"],
            row["reserves"],
            row["borrowings"]

        ),axis=1
    )

    df["roa_calculated_pct"] = df.apply(

        lambda row:

        calculate_roa(

            row["net_profit"],
            row["total_assets"]

        ),axis=1

    )
    return df