import streamlit as st

from utils.db import (
    get_financial_kpis,
    get_sectors
)

from metrics import show_kpi_cards

from charts import (
    sector_chart,
    top_roe_chart
)

from helpers import section


# -----------------------------
# Load Data
# -----------------------------

kpi_df = get_financial_kpis()
sector_df = get_sectors()


# -----------------------------
# Merge Data
# -----------------------------

dashboard_df = kpi_df.merge(
    sector_df,
    on="company_id",
    how="left"

)


# -----------------------------
# Page
# -----------------------------

st.title("🏠 Home Dashboard")

# -----------------------------
# KPI Cards
# -----------------------------

show_kpi_cards(kpi_df)

# -----------------------------
# Sector Chart
# -----------------------------

section("Sector Distribution")
sector_chart(dashboard_df)


# -----------------------------
# ROE Chart
# -----------------------------

section("Top 10 Companies by ROE")
top10 = top_roe_chart(kpi_df)


# -----------------------------
# Top Companies
# -----------------------------

section("Top 5 Companies")

st.dataframe(

    top10[[

            "company_id",
            "roe_calculated_pct",
            "roce_calculated_pct",
            "free_cash_flow"

        ]].head(),
    use_container_width=True

)