import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_companies,
    get_financial_kpis,
    get_peer_percentiles,
)

# Page Config

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="🤝",
    layout="wide"
)

st.title("🤝 Peer Comparison")

# Load Data

company_df = get_companies()
kpi_df = get_financial_kpis()
peer_df = get_peer_percentiles()

# Step 2 : Company Selection

st.subheader("Company Selection")

# Company List
companies = sorted(
    company_df["company_name"]
    .dropna()
    .unique()
)

selected_company = st.selectbox(
    "Select Company",
    companies
)

# Find selected company
company = company_df[
    company_df["company_name"] == selected_company
]

if company.empty:
    st.error("Company not found.")
    st.stop()

company = company.iloc[0]

company_id = str(company["id"]).strip().upper()

# Debug
st.write("Selected Company :", selected_company)
st.write("Company ID :", company_id)

st.write("Company Details")
st.dataframe(
    pd.DataFrame([company])
)

# Step 3 : Peer Information

st.subheader("Peer Information")

# Clean Company IDs
peer_df["company_id"] = (
    peer_df["company_id"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# Match selected company
peer = peer_df[
    peer_df["company_id"] == company_id
]


if not peer.empty:

    st.success("Company found in Peer Dataset")

    st.dataframe(
        peer[
            [
                "company_id",
                "peer_group_name",
                "is_benchmark"
            ]
        ]
    )

else:

    st.error("Company not found in Peer Dataset")

    st.write("First 10 Company IDs")

    st.dataframe(
        peer_df[
            ["company_id"]
        ].head(10)
    )
    
# Step 4 : Peer Group Companies

st.subheader("Peer Group Companies")

# Selected company's peer group
peer = peer.iloc[0]

peer_group = peer["peer_group_name"]

st.write("Peer Group :", peer_group)

# All companies in same peer group
peer_group_df = peer_df[
    peer_df["peer_group_name"] == peer_group
].copy()

st.write("Companies in this Peer Group :", len(peer_group_df))

st.dataframe(
    peer_group_df[[
            "company_id",
            "peer_group_name",
            "is_benchmark"
        ]]
)

# Financial Data of Peer Companies
peer_company_ids = peer_group_df["company_id"].tolist()

# Financial data of all peer companies
peer_kpi_df = kpi_df[
    kpi_df["company_id"].isin(peer_company_ids)
].copy()

# Step 5 : Peer Comparison Header

st.divider()

st.subheader("📊 Peer Comparison Summary")

# Benchmark Company
benchmark_df = peer_group_df[
    peer_group_df["is_benchmark"] == True
]

if not benchmark_df.empty:
    benchmark_company = benchmark_df.iloc[0]["company_id"]
else:
    benchmark_company = "Not Available"

# Top Summary Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Selected Company",
        company_id
    )

with col2:
    st.metric(
        "Peer Group",
        peer_group
    )

with col3:
    st.metric(
        "Benchmark",
        benchmark_company
    )

with col4:
    st.metric(
        "Total Peers",
        len(peer_group_df)
    )

# Step 6 : Peer KPI Comparison Table

st.divider()

st.subheader("📈 Peer KPI Comparison")

comparison_df = peer_kpi_df[[
        "company_id",
        "sales",
        "net_profit",
        "roe_calculated_pct",
        "roce_calculated_pct",
        "net_profit_margin_pct",
        "free_cash_flow",
        "composite_quality_score"
    ]].copy()

comparison_df = comparison_df.rename(columns={
        "company_id": "Company",
        "sales": "Sales",
        "net_profit": "Net Profit",
        "roe_calculated_pct": "ROE (%)",
        "roce_calculated_pct": "ROCE (%)",
        "net_profit_margin_pct": "NPM (%)",
        "free_cash_flow": "Free Cash Flow",
        "composite_quality_score": "Quality Score"
    }
)

comparison_df = comparison_df.sort_values(
    by="Quality Score",
    ascending=False,
    na_position="last"
)

st.dataframe(
    comparison_df,
    use_container_width=True,
    hide_index=True
)

# Step 7 : Top Performers

st.divider()

st.subheader("🏆 Top Performers")

# Highest Sales
top_sales = peer_kpi_df.loc[
    peer_kpi_df["sales"].idxmax()
]

# Highest Net Profit
top_profit = peer_kpi_df.loc[
    peer_kpi_df["net_profit"].idxmax()
]

# Highest ROE
top_roe = peer_kpi_df.loc[
    peer_kpi_df["roe_calculated_pct"].idxmax()
]

# Highest ROCE
top_roce = peer_kpi_df.loc[
    peer_kpi_df["roce_calculated_pct"].idxmax()
]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Highest Sales",
        top_sales["company_id"],
        f'{top_sales["sales"]:,}'
    )

with col2:
    st.metric(
        "Highest Profit",
        top_profit["company_id"],
        f'{top_profit["net_profit"]:,}'
    )

with col3:
    st.metric(
        "Highest ROE",
        top_roe["company_id"],
        f'{top_roe["roe_calculated_pct"]:.2f}%'
    )

with col4:
    st.metric(
        "Highest ROCE",
        top_roce["company_id"],
        f'{top_roce["roce_calculated_pct"]:.2f}%'
    )

# Step 8 : Selected Company vs Peer Average

st.divider()

st.subheader("📊 Selected Company vs Peer Average")

metrics = [
    ("sales", "Sales"),
    ("net_profit", "Net Profit"),
    ("roe_calculated_pct", "ROE (%)"),
    ("roce_calculated_pct", "ROCE (%)"),
    ("net_profit_margin_pct", "NPM (%)"),
    ("free_cash_flow", "Free Cash Flow"),
    ("composite_quality_score", "Quality Score"),
]

# Selected company financial data
selected_company_data = peer_kpi_df[
    peer_kpi_df["company_id"] == company_id
].iloc[0]

comparison_rows = []

for column, label in metrics:

    company_value = selected_company_data[column]

    peer_average = peer_kpi_df[column].mean()

    difference = company_value - peer_average

    if difference >= 0:
        status = "Above Average"
    else:
        status = "Below Average"

    comparison_rows.append({
        "Metric": label,
        "Company": round(company_value, 2),
        "Peer Average": round(peer_average, 2),
        "Difference": round(difference, 2),
        "Status": status
    })

comparison_summary = pd.DataFrame(comparison_rows)

st.dataframe(
    comparison_summary,
    use_container_width=True,
    hide_index=True
)

# Step 9 : Percentile Performance

st.divider()

st.subheader("📊 Percentile Performance")

percentile_metrics = {
    "roe_calculated_pct_percentile": "ROE",
    "roce_calculated_pct_percentile": "ROCE",
    "net_profit_margin_pct_percentile": "NPM",
    "free_cash_flow_percentile": "FCF",
    "sales_cagr_5yr_percentile": "Sales CAGR",
    "profit_cagr_5yr_percentile": "Profit CAGR"
}

cols = st.columns(3)

for i, (column, label) in enumerate(percentile_metrics.items()):

    value = peer[column]

    if pd.isna(value):
        display = "N/A"
    else:
        display = f"{value*100:.1f}%"

    with cols[i % 3]:
        st.metric(
            label,
            display
        )

# Step 10 : Interactive ROE Comparison

st.divider()

st.subheader("📈 ROE Comparison")

chart_df = peer_kpi_df[
    [
        "company_id",
        "roe_calculated_pct"
    ]
].sort_values(
    by="roe_calculated_pct",
    ascending=False
)

fig = px.bar(
    chart_df,
    x="company_id",
    y="roe_calculated_pct",
    color="roe_calculated_pct",
    text="roe_calculated_pct",
    labels={
        "company_id": "Company",
        "roe_calculated_pct": "ROE (%)"
    },
    title="ROE Comparison Across Peer Group"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="ROE (%)",
    height=500,
    showlegend=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Step 12 : Peer Ranking

st.divider()

st.subheader("🏅 Peer Ranking")

ranking_df = peer_kpi_df[
    [
        "company_id",
        "sales",
        "net_profit",
        "roe_calculated_pct",
        "roce_calculated_pct",
        "composite_quality_score"
    ]
].copy()

# Rank by Quality Score
ranking_df["Rank"] = (
    ranking_df["composite_quality_score"]
    .rank(
        ascending=False,
        method="dense"
    )
)

ranking_df = ranking_df.sort_values(
    by="Rank"
)

ranking_df = ranking_df.rename(
    columns={
        "company_id": "Company",
        "sales": "Sales",
        "net_profit": "Net Profit",
        "roe_calculated_pct": "ROE (%)",
        "roce_calculated_pct": "ROCE (%)",
        "composite_quality_score": "Quality Score"
    }
)

# Rank first
ranking_df = ranking_df[
    [
        "Rank",
        "Company",
        "Sales",
        "Net Profit",
        "ROE (%)",
        "ROCE (%)",
        "Quality Score"
    ]
]

def highlight_selected(row):
    if row["Company"] == company_id:
        return [  "background-color:#14532d;color:white;font-weight:bold"] * len(row)
    return [""] * len(row)

st.dataframe(
    ranking_df.style.apply(
        highlight_selected,
        axis=1
    ),
    use_container_width=True
)

# Step 13 : Radar Chart

st.divider()

st.subheader("🕸 Financial Radar Chart")

from pathlib import Path

radar_path = Path(
    f"reports/radar_charts/{company_id}_radar.png"
)

if radar_path.exists():

    left, right = st.columns([1, 1])

    with left:

        st.image(
        str(radar_path),
        width=480
    )

    with right:

        st.subheader("Insights")

        st.success("ROE is above peer average")

        st.success("Quality Score is above peer average")

        st.warning("Sales is below peer average")

        st.warning("Free Cash Flow is below peer average")

else:

    st.warning(
        f"Radar chart not found for {company_id}"
    )
    
# Step 14 : Key Insights

st.divider()

st.subheader("💡 Key Insights")

# Selected company data
company_data = peer_kpi_df[
    peer_kpi_df["company_id"] == company_id
].iloc[0]

# Peer averages
avg_roe = peer_kpi_df["roe_calculated_pct"].mean()
avg_roce = peer_kpi_df["roce_calculated_pct"].mean()
avg_profit = peer_kpi_df["net_profit"].mean()
avg_sales = peer_kpi_df["sales"].mean()

# ROE
if company_data["roe_calculated_pct"] >= avg_roe:
    st.success(
        f"ROE is above peer average ({avg_roe:.2f}%)"
    )
else:
    st.warning(
        f"ROE is below peer average ({avg_roe:.2f}%)"
    )

# ROCE
if company_data["roce_calculated_pct"] >= avg_roce:
    st.success(
        f"ROCE is above peer average ({avg_roce:.2f}%)"
    )
else:
    st.warning(
        f"ROCE is below peer average ({avg_roce:.2f}%)"
    )

# Net Profit
if company_data["net_profit"] >= avg_profit:
    st.success(
        "Net Profit is above peer average."
    )
else:
    st.warning(
        "Net Profit is below peer average."
    )

# Sales
if company_data["sales"] >= avg_sales:
    st.success(
        "Sales is above peer average."
    )
else:
    st.warning(
        "Sales is below peer average."
    )

# Quality Score Rank
rank = (
    peer_kpi_df["composite_quality_score"]
    .rank(
        ascending=False,
        method="dense"
    )
)

company_rank = int(
    rank[
        peer_kpi_df["company_id"] == company_id
    ].iloc[0]
)

st.info(
    f"Overall Quality Score Rank : #{company_rank} out of {len(peer_kpi_df)} peers"
)

# Step 15 : Download Report

st.divider()

st.subheader("📥 Download Report")

# Ranking table ko CSV me convert karo
csv = ranking_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Peer Comparison Report",
    data=csv,
    file_name=f"{company_id}_peer_comparison_report.csv",
    mime="text/csv",
    use_container_width=True,
)