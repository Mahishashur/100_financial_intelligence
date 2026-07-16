import streamlit as st

from utils.db import (
    get_companies,
    get_sectors
)

from profile_utils import (
    company_selector,
    company_card
)

from utils.db import (
    get_companies,
    get_sectors,
    get_profit_loss,
    get_cashflow,
    get_pros_cons
)

from charts import (
    revenue_chart,
    profit_chart,
    cashflow_chart
)

st.title("🏢 Company Profile")

company_df = get_companies()
company_df = get_companies()

sector_df = get_sectors()
profit_df = get_profit_loss()

cash_df = get_cashflow()
pros_df = get_pros_cons()

selected_company = company_selector(
    company_df
)

company = company_df[
    company_df["id"] == selected_company
].iloc[0]

sector = sector_df[
    sector_df["company_id"] == selected_company
].iloc[0]

pros = pros_df[
    pros_df["company_id"] == selected_company
]

if not pros.empty:

    pros = pros.iloc[0]

    left, right = st.columns(2)

    with left:
        st.success("Pros")
        st.write(pros["pros"])

    with right:
        st.error("Cons")
        st.write(pros["cons"])

else:

    st.info("Pros & Cons not available.")

company_card(
    company,sector
)

st.divider()

st.subheader("📈 Revenue Trend")

revenue_chart(
    profit_df,
    selected_company
)

st.divider()

st.subheader("✅ Pros & ❌ Cons")

left, right = st.columns(2)

with left:

    st.success("Pros")

    st.write(pros["pros"])

with right:

    st.error("Cons")

    st.write(pros["cons"])

st.subheader("💰 Net Profit Trend")

profit_chart(
    profit_df,
    selected_company
)

st.divider()

st.subheader("💵 Cash Flow Trend")

cashflow_chart(
    cash_df,
    selected_company
)



