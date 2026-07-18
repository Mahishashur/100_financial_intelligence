import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_companies,
)

st.title("📑 Reports")

company_df = get_companies()

selected_company = st.selectbox(
    "🏢 Select Company",
    company_df["company_name"].sort_values()
)

company = company_df[
    company_df["company_name"] == selected_company
].iloc[0]

company_id = company["id"]

st.write("Company ID :", company_id)

# -------------------------------------------------
# Step 2 : Load All Datasets
# -------------------------------------------------

# Financial Ratios (CSV has no header)
financial_df = pd.read_csv(
    "data/processed/financial_ratios_clean.csv",
    header=None
)

financial_df.columns = [
    "id",
    "company_id",
    "year",
    "roe_percentage",
    "roce_percentage",
    "book_value",
    "face_value",
    "dividend_yield",
    "cash_conversion_cycle",
    "debtor_days",
    "inventory_days",
    "interest_coverage",
    "promoter_holding",
    "pledged_percentage",
    "pe_ratio",
]

# Remove duplicate records
financial_df = financial_df.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

# Other datasets
pnl_df = pd.read_csv(
    "data/processed/profitandloss_clean.csv"
)

balance_df = pd.read_csv(
    "data/processed/balancesheet_clean.csv"
)

sector_df = pd.read_csv(
    "data/processed/sectors_clean.csv"
)

# -------------------------------------------------
# Step 2 : Filter Company Data
# -------------------------------------------------

company_financial = (
    financial_df[
        financial_df["company_id"].str.upper()
        == company_id.upper()
    ]
    .copy()
)

company_pnl = (
    pnl_df[
        pnl_df["company_id"] == company_id
    ]
    .copy()
    .sort_values("year")
)

company_balance = (
    balance_df[
        balance_df["company_id"] == company_id
    ]
    .copy()
    .sort_values("year")
)

company_sector = (
    sector_df[
        sector_df["company_id"] == company_id
    ]
    .copy()
)

st.write("Financial :", len(company_financial))
st.write("P&L :", len(company_pnl))
st.write("Balance :", len(company_balance))
st.write("Sector :", len(company_sector))

# -------------------------------------------------
# Step 3 : Executive Summary
# -------------------------------------------------

latest_pnl = company_pnl.iloc[-1]
latest_balance = company_balance.iloc[-1]
latest_financial = company_financial.iloc[-1]
latest_sector = company_sector.iloc[0]

st.divider()

st.subheader("📋 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏭 Sector",
        latest_sector["broad_sector"]
    )

with col2:
    st.metric(
        "📊 ROE",
        f"{latest_financial['roe_percentage']}%"
    )

with col3:
    st.metric(
        "📈 ROCE",
        f"{latest_financial['roce_percentage']}%"
    )

with col4:
    st.metric(
        "💼 Market Cap",
        latest_sector["market_cap_category"]
    )
    
# -------------------------------------------------
# Step 4 : Financial Performance Summary
# -------------------------------------------------

st.divider()

st.subheader("📈 Financial Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Sales",
        f"{latest_pnl['sales']:,.0f}"
    )

with col2:
    st.metric(
        "📊 Operating Profit",
        f"{latest_pnl['operating_profit']:,.0f}"
    )

with col3:
    st.metric(
        "💵 Net Profit",
        f"{latest_pnl['net_profit']:,.0f}"
    )

with col4:
    st.metric(
        "🏦 Total Assets",
        f"{latest_balance['total_assets']:,.0f}"
    )
    
# -------------------------------------------------
# Step 5 : Key Financial Ratios
# -------------------------------------------------

st.divider()

st.subheader("📊 Key Financial Ratios")

# Safe Calculations
equity_base = (
    latest_balance["equity_capital"] +
    latest_balance["reserves"]
)

debt_to_equity = (
    latest_balance["borrowings"] / equity_base
    if equity_base > 0 else 0
)

net_profit_margin = (
    (latest_pnl["net_profit"] / latest_pnl["sales"]) * 100
    if latest_pnl["sales"] > 0 else 0
)

asset_turnover = (
    latest_pnl["sales"] / latest_balance["total_assets"]
    if latest_balance["total_assets"] > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏦 Debt / Equity",
        f"{debt_to_equity:.2f}"
    )

with col2:
    st.metric(
        "📈 ROE",
        f"{latest_financial['roe_percentage']:.2f}%"
    )

with col3:
    st.metric(
        "📊 Net Profit Margin",
        f"{net_profit_margin:.2f}%"
    )

with col4:
    st.metric(
        "🔄 Asset Turnover",
        f"{asset_turnover:.2f}x"
    )
    
# -------------------------------------------------
# Step 6 : Business Performance Charts
# -------------------------------------------------

st.divider()

st.subheader("📈 Business Performance")

chart_df = company_pnl[
    [
        "year",
        "sales",
        "operating_profit",
        "net_profit"
    ]
].copy()

fig = px.line(
    chart_df,
    x="year",
    y=[
        "sales",
        "operating_profit",
        "net_profit"
    ],
    markers=True,
    title=f"{selected_company} Financial Trends"
)

fig.update_layout(
    height=500,
    hovermode="x unified",
    xaxis_title="Financial Year",
    yaxis_title="Amount",
    legend_title="Metrics"
)

fig.update_traces(
    line=dict(width=3),
    marker=dict(size=7)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Step 7 : Executive Insights
# -------------------------------------------------

st.divider()

st.subheader("💡 Executive Insights")

# Sales Growth
sales_growth = company_pnl.iloc[-1]["sales"] - company_pnl.iloc[-2]["sales"]

# Profit Growth
profit_growth = (
    company_pnl.iloc[-1]["net_profit"] -
    company_pnl.iloc[-2]["net_profit"]
)

# Debt Status
equity = latest_balance["equity_capital"] + latest_balance["reserves"]

de_ratio = (
    latest_balance["borrowings"] / equity
    if equity > 0 else 0
)

if de_ratio < 0.5:
    debt_status = "🟢 Low Debt"
elif de_ratio < 1:
    debt_status = "🟡 Moderate Debt"
else:
    debt_status = "🔴 High Debt"

sales_status = (
    "📈 Sales Increased"
    if sales_growth > 0
    else "📉 Sales Decreased"
)

profit_status = (
    "💰 Profit Increased"
    if profit_growth > 0
    else "📉 Profit Decreased"
)

overall = (
    "🟢 Strong Financial Position"
    if latest_financial["roe_percentage"] >= 15
    else "🟡 Average Financial Position"
)

st.success(f"• {sales_status}")
st.success(f"• {profit_status}")
st.info(f"• {debt_status}")
st.info(f"• Market Cap : {latest_sector['market_cap_category']}")
st.success(f"• {overall}")

# -------------------------------------------------
# Step 8 : Download Report
# -------------------------------------------------

st.divider()

st.subheader("📥 Download Executive Report")

report_df = pd.DataFrame({
    "Metric": [
        "Company",
        "Sector",
        "Market Cap",
        "Sales",
        "Operating Profit",
        "Net Profit",
        "Total Assets",
        "ROE (%)",
        "ROCE (%)",
        "Debt to Equity",
        "Net Profit Margin (%)",
        "Asset Turnover"
    ],
    "Value": [
        selected_company,
        latest_sector["broad_sector"],
        latest_sector["market_cap_category"],
        latest_pnl["sales"],
        latest_pnl["operating_profit"],
        latest_pnl["net_profit"],
        latest_balance["total_assets"],
        round(latest_financial["roe_percentage"], 2),
        round(latest_financial["roce_percentage"], 2),
        round(debt_to_equity, 2),
        round(net_profit_margin, 2),
        round(asset_turnover, 2)
    ]
})

st.dataframe(
    report_df,
    use_container_width=True,
    hide_index=True
)

csv = report_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Executive Report (CSV)",
    data=csv,
    file_name=f"{selected_company}_Executive_Report.csv",
    mime="text/csv"
)