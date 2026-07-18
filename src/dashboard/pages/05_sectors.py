import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_companies,
    get_sectors,
)

st.title("🏭 Sector Analysis")

company_df = get_companies()
sector_df = get_sectors()

st.write("Companies :", len(company_df))
st.write("Sector :", len(sector_df))

# -------------------------------------------------
# Sector Selection
# -------------------------------------------------

sector_list = sorted(
    sector_df["broad_sector"].dropna().unique().tolist()
)

selected_sector = st.selectbox(
    "🏭 Select Sector",
    sector_list
)

st.write("Selected Sector :", selected_sector)

# -------------------------------------------------
# Companies in Selected Sector
# -------------------------------------------------

sector_companies = sector_df[
    sector_df["broad_sector"] == selected_sector
].copy()

sector_companies = sector_companies.merge(
    company_df,
    left_on="company_id",
    right_on="id",
    how="left"
)

st.divider()

st.subheader(f"🏢 Companies in {selected_sector}")

st.write("Total Companies :", len(sector_companies))

st.dataframe(
    sector_companies[
        [
            "company_name",
            "market_cap_category",
            "sub_sector",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

# -------------------------------------------------
# Step 4 : Sector Summary
# -------------------------------------------------

st.divider()

st.subheader("📊 Sector Summary")

total_companies = len(sector_companies)

large_cap = (
    sector_companies["market_cap_category"] == "Large Cap"
).sum()

mid_cap = (
    sector_companies["market_cap_category"] == "Mid Cap"
).sum()

sub_sectors = sector_companies["sub_sector"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏢 Companies",
        total_companies
    )

with col2:
    st.metric(
        "🥇 Large Cap",
        large_cap
    )

with col3:
    st.metric(
        "🥈 Mid Cap",
        mid_cap
    )

with col4:
    st.metric(
        "🏭 Sub Sectors",
        sub_sectors
    )
    
# -------------------------------------------------
# Step 5 : Market Cap Distribution
# -------------------------------------------------

st.divider()

st.subheader("📊 Market Cap Distribution")

market_cap_df = (
    sector_companies["market_cap_category"]
    .value_counts()
    .reset_index()
)

market_cap_df.columns = [
    "Market Cap",
    "Companies"
]

fig = px.pie(
    market_cap_df,
    names="Market Cap",
    values="Companies",
    hole=0.55,
    title=f"{selected_sector} Market Cap Distribution"
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
# Step 7 : Sector Performance
# -------------------------------------------------

st.divider()

st.subheader("📈 Sector Performance Comparison")

performance_df = sector_companies[
    [
        "company_name",
        "market_cap_category",
        "roe_percentage",
        "roce_percentage",
        "book_value",
        "face_value",
    ]
].copy()

performance_df = performance_df.sort_values(
    by="roe_percentage",
    ascending=False
)

st.dataframe(
    performance_df,
    use_container_width=True,
    hide_index=True,
)

# -------------------------------------------------
# Step 8 : ROE vs ROCE Scatter Plot
# -------------------------------------------------

st.divider()

st.subheader("🎯 ROE vs ROCE Analysis")

fig = px.scatter(
    performance_df,
    x="roe_percentage",
    y="roce_percentage",
    color="market_cap_category",
    hover_name="company_name",
    size="book_value",
    title=f"{selected_sector} : ROE vs ROCE",
    labels={
        "roe_percentage": "ROE (%)",
        "roce_percentage": "ROCE (%)",
        "market_cap_category": "Market Cap"
    }
)

fig.update_layout(
    height=550,
    xaxis_title="Return on Equity (ROE %)",
    yaxis_title="Return on Capital Employed (ROCE %)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------
# Step 9 : Sector Leaderboard
# -------------------------------------------------

st.divider()

st.subheader("🏆 Top Performers in Sector")

leaderboard_df = (
    performance_df
    .sort_values(
        by="roe_percentage",
        ascending=False
    )
    .head(5)
    .reset_index(drop=True)
)

leaderboard_df.insert(
    0,
    "Rank",
    ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][:len(leaderboard_df)]
)

st.dataframe(
    leaderboard_df[
        [
            "Rank",
            "company_name",
            "roe_percentage",
            "roce_percentage",
            "market_cap_category",
        ]
    ],
    use_container_width=True,
    hide_index=True,
)

# -------------------------------------------------
# Step 10 : Sector Insights
# -------------------------------------------------

st.divider()

st.subheader("💡 Sector Insights")

avg_roe = performance_df["roe_percentage"].mean()
avg_roce = performance_df["roce_percentage"].mean()

top_company = performance_df.loc[
    performance_df["roe_percentage"].idxmax()
]

dominant_market_cap = (
    sector_companies["market_cap_category"]
    .mode()
    .iloc[0]
)

st.success(
    f"🏢 This sector contains **{total_companies}** companies across **{sub_sectors}** sub-sectors."
)

st.info(
    f"🥇 **{top_company['company_name']}** has the highest ROE (**{top_company['roe_percentage']:.2f}%**)."
)

st.info(
    f"📊 Average ROE of the sector is **{avg_roe:.2f}%**."
)

st.info(
    f"📈 Average ROCE of the sector is **{avg_roce:.2f}%**."
)

st.success(
    f"🏆 **{dominant_market_cap}** companies dominate this sector."
)