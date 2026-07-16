import streamlit as st


def show_kpi_cards(df):

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    col1.metric(
        "Companies",
        len(df)
    )

    col2.metric(
        "Average ROE",
        round(
            df["roe_calculated_pct"].mean(),
            2
        )
    )

    col3.metric(
        "Average ROCE",
        round(
            df["roce_calculated_pct"].mean(),
            2
        )
    )

    col4.metric(
        "Highest ROE",
        round(
            df["roe_calculated_pct"].max(),
            2
        )
    )

    col5.metric(
        "Lowest Debt / Equity",
        round(
            df["debt_to_equity"].min(),
            2
        )
    )

    col6.metric(
        "Highest Free Cash Flow",
        round(
            df["free_cash_flow"].max(),
            2
        )
    )