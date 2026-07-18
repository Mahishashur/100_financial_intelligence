import pandas as pd
from pathlib import Path

# ----------------------------------------
# Project Paths
# ----------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# ----------------------------------------
# Load Datasets
# ----------------------------------------

financial_df = pd.read_csv(
    DATA_DIR / "financial_ratios_clean.csv",
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

companies_df = pd.read_csv(
    DATA_DIR / "companies_clean.csv"
)

sector_df = pd.read_csv(
    DATA_DIR / "sectors_clean.csv"
)

cashflow_df = pd.read_csv(
    DATA_DIR / "cashflow_clean.csv"
)

marketcap_df = pd.read_excel(
    BASE_DIR / "data" / "raw" / "market_cap.xlsx"
)