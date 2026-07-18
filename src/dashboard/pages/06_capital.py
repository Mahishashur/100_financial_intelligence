import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_companies,
)

st.title("💰 Capital Structure Analysis")

company_df = get_companies()

st.write("Companies :", len(company_df))

# -------------------------------------------------
# Company Selection
# -------------------------------------------------

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
# Load Balance Sheet Data
# -------------------------------------------------

balance_df = pd.read_csv(
    "data/processed/balancesheet_clean.csv"
)

company_balance = (
    balance_df[
        balance_df["company_id"] == company_id
    ]
    .copy()
    .sort_values("year")
)

st.write("Balance Sheet Records :", len(company_balance))

st.dataframe(
    company_balance.head(),
    use_container_width=True
)

# -------------------------------------------------
# Step 3 : Capital Structure Summary
# -------------------------------------------------

latest = company_balance.iloc[-1]

st.divider()

st.subheader("💰 Capital Structure Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏛 Equity Capital",
        f"{latest['equity_capital']:,.0f}"
    )

with col2:
    st.metric(
        "🏦 Reserves",
        f"{latest['reserves']:,.0f}"
    )

with col3:
    st.metric(
        "💳 Borrowings",
        f"{latest['borrowings']:,.0f}"
    )

with col4:
    total_capital = (
    latest["equity_capital"]
    + latest["reserves"]
    + latest["borrowings"]
)

    st.metric(
        "💼 Total Capital",
        f"{total_capital:,.0f}"
    )
    
# -------------------------------------------------
# Step 4 : Capital Structure Trend
# -------------------------------------------------

st.divider()

st.subheader("📈 Capital Structure Trend")

trend_df = company_balance[
    [
        "year",
        "equity_capital",
        "reserves",
        "borrowings",
    ]
].copy()

trend_df = trend_df.melt(
    id_vars="year",
    value_vars=[
        "equity_capital",
        "reserves",
        "borrowings",
    ],
    var_name="Component",
    value_name="Amount"
)

fig = px.line(
    trend_df,
    x="year",
    y="Amount",
    color="Component",
    markers=True,
    title=f"{selected_company} Capital Structure Trend"
)

fig.update_traces(
    line=dict(width=3),
    marker=dict(size=8)
)

fig.update_layout(
    height=500,
    hovermode="x unified",
    xaxis_title="Financial Year",
    yaxis_title="Amount"
)

st.plotly_chart(
    fig,
    use_container_width=True
)    

# -------------------------------------------------
# Step 5 : Capital Composition
# -------------------------------------------------

st.divider()

st.subheader("🥧 Capital Composition")

composition_df = pd.DataFrame({
    "Component": [
        "Equity Capital",
        "Reserves",
        "Borrowings"
    ],
    "Amount": [
        latest["equity_capital"],
        latest["reserves"],
        latest["borrowings"]
    ]
})

fig = px.pie(
    composition_df,
    names="Component",
    values="Amount",
    hole=0.55,
    title=f"{selected_company} Capital Composition"
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig.update_layout(
    height=450
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Step 6 : Capital Sources vs Asset Allocation
# -------------------------------------------------

st.divider()

st.subheader("⚖️ Capital Sources vs Asset Allocation")

left_col, right_col = st.columns(2)

with left_col:

    capital_df = pd.DataFrame({
        "Capital Source": [
            "Equity",
            "Reserves",
            "Borrowings",
            "Other Liabilities"
        ],
        "Amount": [
            latest["equity_capital"],
            latest["reserves"],
            latest["borrowings"],
            latest["other_liabilities"]
        ]
    })

    fig1 = px.pie(
        capital_df,
        names="Capital Source",
        values="Amount",
        hole=0.55,
        title="Capital Sources"
    )

    st.plotly_chart(fig1, use_container_width=True)

with right_col:

    asset_df = pd.DataFrame({
        "Asset Type": [
            "Fixed Assets",
            "CWIP",
            "Investments",
            "Other Assets"
        ],
        "Amount": [
            latest["fixed_assets"],
            latest["cwip"],
            latest["investments"],
            latest["other_asset"]
        ]
    })

    fig2 = px.pie(
        asset_df,
        names="Asset Type",
        values="Amount",
        hole=0.55,
        title="Asset Allocation"
    )

    st.plotly_chart(fig2, use_container_width=True)
    
    # -------------------------------------------------
# Step 7 : Capital Structure Ratios
# -------------------------------------------------

st.divider()

st.subheader("📊 Capital Structure Ratios")

# Safe calculations
equity_base = latest["equity_capital"] + latest["reserves"]

debt_to_equity = (
    latest["borrowings"] / equity_base
    if equity_base > 0 else 0
)

borrowing_ratio = (
    latest["borrowings"] / latest["total_liabilities"]
    if latest["total_liabilities"] > 0 else 0
)

asset_coverage = (
    latest["total_assets"] / latest["borrowings"]
    if latest["borrowings"] > 0 else 0
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🏦 Debt / Equity",
        f"{debt_to_equity:.2f}"
    )

with col2:
    st.metric(
        "💳 Borrowing Ratio",
        f"{borrowing_ratio:.2%}"
    )

with col3:
    st.metric(
        "🏢 Asset Coverage",
        f"{asset_coverage:.2f}x"
    )
    
# -------------------------------------------------
# Step 8 : Capital Structure Insights
# -------------------------------------------------

st.divider()

st.subheader("💡 Capital Structure Insights")

# Largest Capital Source
capital_sources = {
    "Equity Capital": latest["equity_capital"],
    "Reserves": latest["reserves"],
    "Borrowings": latest["borrowings"],
    "Other Liabilities": latest["other_liabilities"],
}

largest_source = max(capital_sources, key=capital_sources.get)

# Debt Level Insight
if debt_to_equity < 0.5:
    st.success(
        f"✅ The company has a healthy capital structure with a low Debt-to-Equity ratio ({debt_to_equity:.2f})."
    )
elif debt_to_equity < 1:
    st.info(
        f"ℹ️ The company has a moderate Debt-to-Equity ratio ({debt_to_equity:.2f})."
    )
else:
    st.warning(
        f"⚠️ The company has a high Debt-to-Equity ratio ({debt_to_equity:.2f})."
    )

# Capital Source Insight
st.info(
    f"🏦 The largest source of capital is **{largest_source}**."
)

# Borrowing Insight
st.info(
    f"💳 Borrowings contribute **{borrowing_ratio:.2%}** of total liabilities."
)

# Asset Coverage Insight
if asset_coverage >= 2:
    st.success(
        f"🏢 Assets cover borrowings by **{asset_coverage:.2f}x**, indicating strong financial stability."
    )
else:
    st.warning(
        f"⚠️ Asset coverage is **{asset_coverage:.2f}x**, which should be monitored."
    )