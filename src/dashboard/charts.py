import streamlit as st
import plotly.express as px


def sector_chart(df):

    sector_count = (

        df

        .groupby("broad_sector")

        .size()

        .reset_index(name="Companies")

        .sort_values(
            "Companies",
            ascending=False
        )

    )

    fig = px.pie(

        sector_count,

        names="broad_sector",

        values="Companies",

        hole=0.55,

        title="Sector Distribution"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def top_roe_chart(df):

    top10 = (

        df

        .sort_values(
            "roe_calculated_pct",
            ascending=False
        )

        .head(10)

    )

    fig = px.bar(

        top10,

        x="roe_calculated_pct",

        y="company_id",

        orientation="h",

        title="Top 10 Companies by ROE"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    return top10

def revenue_chart(df, company_id):

    company_df = (
        df[df["company_id"] == company_id]
        .sort_values("year")
    )

    fig = px.line(
        company_df,
        x="year",
        y="sales",
        markers=True,
        title="Revenue Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
def profit_chart(df, company_id):

    company_df = (
        df[df["company_id"] == company_id]
        .sort_values("year")
    )

    fig = px.line(
        company_df,
        x="year",
        y="net_profit",
        markers=True,
        title="Net Profit Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    
def cashflow_chart(df, company_id):

    company_df = (
        df[df["company_id"] == company_id]
        .sort_values("year")
    )

    fig = px.line(
        company_df,
        x="year",
        y="net_cash_flow",
        markers=True,
        title="Net Cash Flow Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )