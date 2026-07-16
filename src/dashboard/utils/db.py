import streamlit as st
import pandas as pd


# -----------------------------
# Financial KPIs
# -----------------------------
@st.cache_data(ttl=600)
def get_financial_kpis():

    return pd.read_csv(
        "data/output/financial_kpis.csv"
    )


# -----------------------------
# Company Profiles
# -----------------------------
@st.cache_data(ttl=600)
def get_companies():

    return pd.read_excel(
        "data/raw/core/companies.xlsx",
        header=1
    )


# -----------------------------
# Sector Master
# -----------------------------
@st.cache_data(ttl=600)
def get_sectors():

    return pd.read_excel(
        "data/raw/supplementary/sectors.xlsx"
    )


# -----------------------------
# Peer Groups
# -----------------------------
@st.cache_data(ttl=600)
def get_peer_groups():

    return pd.read_excel(
        "data/raw/supplementary/peer_groups_generate.xlsx"
    )


# -----------------------------
# Market Cap
# -----------------------------
@st.cache_data(ttl=600)
def get_market_cap():

    return pd.read_excel(
        "data/raw/supplementary/market_cap.xlsx"
    )
    
@st.cache_data(ttl=600)
def get_profit_loss():

    return pd.read_excel(

        "data/raw/core/profitandloss.xlsx",

        header=1

    )
    
@st.cache_data(ttl=600)
def get_balance_sheet():

    return pd.read_excel(

        "data/raw/core/balancesheet.xlsx",

        header=1

    )
    
@st.cache_data(ttl=600)
def get_cashflow():

    return pd.read_excel(
        "data/raw/core/cashflow.xlsx",
        header=1
    )
    
@st.cache_data(ttl=600)
def get_pros_cons():

    return pd.read_excel(
        "data/raw/core/prosandcons.xlsx",
        header=1
    )
    
@st.cache_data(ttl=600)
def get_pros_cons():

    return pd.read_excel(
        "data/raw/core/prosandcons.xlsx",
        header=1
    )