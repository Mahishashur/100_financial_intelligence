import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from utils.db import (
    get_companies,
    get_financial_kpis,
)

st.title("📈 Trend Analysis")

# Load Data
company_df = get_companies()
kpi_df = get_financial_kpis()

# Company Selection

st.divider()

selected_company = st.selectbox(
    "Select Company",
    company_df["company_name"].sort_values()
)

company = company_df[
    company_df["company_name"] == selected_company
].iloc[0]

company_id = str(company["id"]).strip().upper()

# Step 3 : Company Financial Data

# Normalize company_id
kpi_df["company_id"] = (
    kpi_df["company_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Filter selected company
company_kpi_df = kpi_df[
    kpi_df["company_id"] == company_id
].copy()

# Sort by year
company_kpi_df = company_kpi_df.sort_values("year")

# Step 4 : Profit & Loss Trend Data

pnl_df = pd.read_csv(
    "data/processed/profitandloss_clean.csv"
)

# Normalize company_id
pnl_df["company_id"] = (
    pnl_df["company_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Filter selected company
company_pnl_df = pnl_df[
    pnl_df["company_id"] == company_id
].copy()

# Sort by year
company_pnl_df = company_pnl_df.sort_values("year")

# No Data Check


if company_pnl_df.empty:
    st.warning("No historical financial data available for this company.")
    st.stop()

# Sales Trend

st.divider()

st.subheader("📈 Sales Trend")

chart_df = company_pnl_df.copy()

fig = px.line(
    chart_df,
    x="year",
    y="sales",
    markers=True,
    title=f"{selected_company} Sales Trend",
    labels={
        "year": "Financial Year",
        "sales": "Sales"
    }
)

fig.update_traces(
    line=dict(width=3),
    marker=dict(size=8)
)

fig.update_layout(
    height=450,
    xaxis_title="Financial Year",
    yaxis_title="Sales",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Financial Performance Comparison

st.divider()

st.subheader("📊 Financial Performance Comparison")

comparison_df = company_pnl_df[
    [
        "year",
        "sales",
        "operating_profit",
        "net_profit"
    ]
].copy()

comparison_df = comparison_df.melt(
    id_vars="year",
    value_vars=[
        "sales",
        "operating_profit",
        "net_profit"
    ],
    var_name="Metric",
    value_name="Value"
)

fig = px.line(
    comparison_df,
    x="year",
    y="Value",
    color="Metric",
    markers=True,
    title=f"{selected_company} Financial Performance",
)

fig.update_layout(
    height=500,
    hovermode="x unified",
    legend_title="Financial Metrics",
    xaxis_title="Financial Year",
    yaxis_title="Amount"
)

fig.update_traces(
    line=dict(width=3),
    marker=dict(size=8)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Step 7 : Financial Summary

latest = company_pnl_df.iloc[-1]

st.divider()

st.subheader("📊 Financial Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Sales",
        f"{latest['sales']:,.0f}"
    )

with col2:
    st.metric(
        "📈 Operating Profit",
        f"{latest['operating_profit']:,.0f}"
    )

with col3:
    st.metric(
        "💵 Net Profit",
        f"{latest['net_profit']:,.0f}"
    )

with col4:
    st.metric(
        "📊 OPM %",
        f"{latest['opm_percentage']:.2f}%"
    )
    
# Growth Analysis

st.divider()

st.subheader("📈 Growth Analysis")

first = company_pnl_df.iloc[0]
latest = company_pnl_df.iloc[-1]

# Growth Calculations
sales_growth = (
    (latest["sales"] - first["sales"])
    / first["sales"]
) * 100

operating_growth = (
    (latest["operating_profit"] - first["operating_profit"])
    / first["operating_profit"]
) * 100

profit_growth = (
    (latest["net_profit"] - first["net_profit"])
    / first["net_profit"]
) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📊 Sales Growth",
        f"{sales_growth:.1f}%"
    )

with col2:
    st.metric(
        "📈 Operating Profit Growth",
        f"{operating_growth:.1f}%"
    )

with col3:
    st.metric(
        "💰 Net Profit Growth",
        f"{profit_growth:.1f}%"
    )
    
# Key Financial Insights

st.divider()

st.subheader("💡 Key Financial Insights")

# Highest & Lowest Sales
highest_sales = company_pnl_df.loc[
    company_pnl_df["sales"].idxmax()
]

lowest_sales = company_pnl_df.loc[
    company_pnl_df["sales"].idxmin()
]

# Highest Net Profit
highest_profit = company_pnl_df.loc[
    company_pnl_df["net_profit"].idxmax()
]

# Sales Insight
if sales_growth > 0:
    st.success(
        f"Sales increased by {sales_growth:.1f}% during the available period."
    )
else:
    st.warning(
        f"Sales declined by {abs(sales_growth):.1f}% during the available period."
    )

# Profit Insight
if profit_growth > sales_growth:
    st.success(
        "Net Profit grew faster than Sales, indicating improved profitability."
    )
else:
    st.info(
        "Sales growth outpaced Net Profit growth."
    )

# Highest Sales
st.info(
    f"Highest Sales recorded in {highest_sales['year']} "
    f"({highest_sales['sales']:,.0f})."
)

# Highest Net Profit
st.info(
    f"Highest Net Profit recorded in {highest_profit['year']} "
    f"({highest_profit['net_profit']:,.0f})."
)

# Lowest Sales
st.warning(
    f"Lowest Sales recorded in {lowest_sales['year']} "
    f"({lowest_sales['sales']:,.0f})."
)

# Step 10 : Operating Profit Margin Trend

st.divider()

st.subheader("📉 Operating Profit Margin (OPM %) Trend")

fig = px.line(
    company_pnl_df,
    x="year",
    y="opm_percentage",
    markers=True,
    title=f"{selected_company} OPM % Trend",
)

fig.update_traces(
    line=dict(width=3),
    marker=dict(size=8)
)

fig.update_layout(
    height=450,
    hovermode="x unified",
    xaxis_title="Financial Year",
    yaxis_title="OPM (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Year-over-Year Growth Table

st.divider()

st.subheader("📋 Year-over-Year Growth")

yoy_df = company_pnl_df[
    [
        "year",
        "sales",
        "operating_profit",
        "net_profit"
    ]
].copy()

# Calculate YoY Growth (%)
yoy_df["Sales Growth (%)"] = (
    yoy_df["sales"].pct_change() * 100
).round(2)

yoy_df["Operating Profit Growth (%)"] = (
    yoy_df["operating_profit"].pct_change() * 100
).round(2)

yoy_df["Net Profit Growth (%)"] = (
    yoy_df["net_profit"].pct_change() * 100
).round(2)

st.dataframe(
    yoy_df,
    use_container_width=True,
    hide_index=True
)

# CAGR Analysis

st.divider()

st.subheader("📊 CAGR Analysis")

years = len(company_pnl_df) - 1

# Safe CAGR Function
def calculate_cagr(start, end, years):
    if start <= 0 or years <= 0:
        return None
    return ((end / start) ** (1 / years) - 1) * 100

sales_cagr = calculate_cagr(
    first["sales"],
    latest["sales"],
    years
)

operating_cagr = calculate_cagr(
    first["operating_profit"],
    latest["operating_profit"],
    years
)

profit_cagr = calculate_cagr(
    first["net_profit"],
    latest["net_profit"],
    years
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📈 Sales CAGR",
        f"{sales_cagr:.2f}%"
    )

with col2:
    st.metric(
        "💼 Operating Profit CAGR",
        f"{operating_cagr:.2f}%"
    )

with col3:
    st.metric(
        "💰 Net Profit CAGR",
        f"{profit_cagr:.2f}%"
    )
    
# Step 13 : Download Trend Report

st.divider()
st.subheader("📥 Download Trend Report")


def generate_excel():
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        # Summary Sheet
        summary_df = pd.DataFrame({
            "Metric": [
                "Sales",
                "Operating Profit",
                "Net Profit",
                "OPM %",
                "Sales CAGR",
                "Operating Profit CAGR",
                "Net Profit CAGR",
            ],
            "Value": [
                latest["sales"],
                latest["operating_profit"],
                latest["net_profit"],
                latest["opm_percentage"],
                round(sales_cagr, 2),
                round(operating_cagr, 2),
                round(profit_cagr, 2),
            ],
        })

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False,
        )

        company_pnl_df.to_excel(
            writer,
            sheet_name="Historical Data",
            index=False,
        )

        yoy_df.to_excel(
            writer,
            sheet_name="YoY Growth",
            index=False,
        )

    output.seek(0)
    return output.getvalue()


excel_data = generate_excel()

st.download_button(
    label="📥 Download Trend Report",
    data=excel_data,
    file_name=f"{selected_company}_Trend_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
