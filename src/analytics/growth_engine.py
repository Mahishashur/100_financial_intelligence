import pandas as pd
from cagr import calculate_cagr


def add_growth_kpis(df):

    growth_results = []

    companies = df["company_id"].unique()

    for company in companies:

        company_df = (
            df[df["company_id"] == company]
            .sort_values("year")
            .reset_index(drop=True)
        )

        result = {
            "company_id": company,
            "sales_cagr_5yr": None,
            "profit_cagr_5yr": None,
            "book_value_cagr_5yr": None,
            "reserve_cagr_5yr": None,
            "operating_profit_cagr_5yr": None,
        }

        if len(company_df) >= 6:

            # Sales CAGR
            value, _ = calculate_cagr(
                company_df.iloc[-6]["sales"],
                company_df.iloc[-1]["sales"],
                5
            )
            result["sales_cagr_5yr"] = value

            # Net Profit CAGR
            value, _ = calculate_cagr(
                company_df.iloc[-6]["net_profit"],
                company_df.iloc[-1]["net_profit"],
                5
            )
            result["profit_cagr_5yr"] = value

            # Book Value CAGR
            start_book = (
                company_df.iloc[-6]["equity_capital"] +
                company_df.iloc[-6]["reserves"]
            )

            end_book = (
                company_df.iloc[-1]["equity_capital"] +
                company_df.iloc[-1]["reserves"]
            )

            value, _ = calculate_cagr(
                start_book,
                end_book,
                5
            )
            result["book_value_cagr_5yr"] = value

            # Reserve CAGR
            value, _ = calculate_cagr(
                company_df.iloc[-6]["reserves"],
                company_df.iloc[-1]["reserves"],
                5
            )
            result["reserve_cagr_5yr"] = value

            # Operating Profit CAGR
            value, _ = calculate_cagr(
                company_df.iloc[-6]["operating_profit"],
                company_df.iloc[-1]["operating_profit"],
                5
            )
            result["operating_profit_cagr_5yr"] = value

        growth_results.append(result)

    growth_df = pd.DataFrame(growth_results)

    df = df.merge(
        growth_df,
        on="company_id",
        how="left"
    )

    return df