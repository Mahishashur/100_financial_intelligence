import streamlit as st

st.set_page_config(

    page_title="Nifty 100 Financial Intelligence",

    page_icon="📈",

    layout="wide",

    initial_sidebar_state="expanded"

)

st.title("📈 Nifty 100 Financial Intelligence Dashboard")

st.markdown(
"""
Welcome 👋

This dashboard contains:

- Home Dashboard
- Company Profile
- Financial Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation
- Reports

Select a page from the left sidebar.
"""
)

st.success("Dashboard Loaded Successfully ✅")