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

# ----------------------------------------
# Load Market Cap File
# ----------------------------------------

market_cap_files = list((BASE_DIR / "data" / "raw").rglob("*.xlsx"))

print("\nAvailable Excel Files:")
for file in market_cap_files:
    print(file.name)

market_cap_path = None

for file in market_cap_files:
    if "market" in file.stem.lower() and "cap" in file.stem.lower():
        market_cap_path = file
        break

if market_cap_path is None:
    raise FileNotFoundError(
        "market_cap.xlsx not found anywhere inside data/raw"
    )

print(f"\nUsing Market Cap File : {market_cap_path}")

marketcap_df = pd.read_excel(market_cap_path)

print("-"*50)
print(companies_df.columns.tolist())

print(sector_df.columns.tolist())

print(cashflow_df.columns.tolist())

# ----------------------------------------
# Keep Latest Financial Year
# ----------------------------------------

# =====================================================
# Keep only companies present in master company list
# =====================================================

companies_df["id"] = (
    companies_df["id"]
    .astype(str)
    .str.upper()
    .str.strip()
)

financial_df["company_id"] = (
    financial_df["company_id"]
    .astype(str)
    .str.upper()
    .str.strip()
)

valid_ids = set(companies_df["id"])

financial_df = financial_df[
    financial_df["company_id"].isin(valid_ids)
].copy()

financial_latest = (
    financial_df
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
)

# Latest cashflow
cashflow_latest = (
    cashflow_df
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

print("\nLatest Financial Records :", len(financial_latest))
print("Latest Cashflow Records :", len(cashflow_latest))

# ----------------------------------------
# Merge Master Data
# ----------------------------------------

valuation_df = (
    financial_latest
    .merge(
        companies_df,
        left_on="company_id",
        right_on="id",
        how="left"
    )
    .merge(
        sector_df[
            [
                "company_id",
                "broad_sector"
            ]
        ],
        on="company_id",
        how="left"
    )
)

print("Merged Records :", len(valuation_df))

# =====================================================
# Clean Company Name
# =====================================================

valuation_df["company_name"] = (
    valuation_df["company_name"]
    .fillna("Unknown Company")
    .astype(str)
    .str.replace("\n", "", regex=False)
    .str.strip()
)

# ----------------------------------------
# Prepare Market Cap Data
# ----------------------------------------

print("\nMarket Cap Columns:")
print(marketcap_df.columns.tolist())

# Standardize column names
marketcap_df.columns = (
    marketcap_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nStandardized Market Cap Columns:")
print(marketcap_df.columns.tolist())

# ----------------------------------------
# Merge Market Cap & Cash Flow
# ----------------------------------------

# Keep latest market cap record
marketcap_latest = (
    marketcap_df
    .sort_values("year")
    .groupby("company_id", as_index=False)
    .last()
)

valuation_df = (
    valuation_df
    .merge(
        cashflow_latest[
            [
                "company_id",
                "net_cash_flow"
            ]
        ],
        on="company_id",
        how="left"
    )
    .merge(
        marketcap_latest[
            [
                "company_id",
                "market_cap_crore",
                "pe_ratio",
                "pb_ratio",
                "ev_ebitda"
            ]
        ],
        on="company_id",
        how="left"
    )
)


print("Final Records :", len(valuation_df))


# ----------------------------------------
# Calculate FCF Yield
# ----------------------------------------

valuation_df["fcf_yield_pct"] = (
    valuation_df["net_cash_flow"]
    / valuation_df["market_cap_crore"]
) * 100

valuation_df["fcf_yield_pct"] = (
    valuation_df["fcf_yield_pct"]
    .fillna(0)
    .round(2)
)

print("\nSample Output")

print(
    valuation_df[
        [
            "company_id",
            "market_cap_crore",
            "net_cash_flow",
            "fcf_yield_pct"
        ]
    ].head()
)

# ----------------------------------------
# Standardize Duplicate Columns
# ----------------------------------------

valuation_df = valuation_df.rename(
    columns={
        "pe_ratio_y": "pe_ratio",
        "book_value_y": "book_value",
        "face_value_y": "face_value",
        "roe_percentage_x": "roe_percentage",
        "roce_percentage_x": "roce_percentage",
    }
)

# Remove unused duplicate columns
valuation_df = valuation_df.drop(
    columns=[
        "pe_ratio_x",
        "book_value_x",
        "face_value_x",
        "roe_percentage_y",
        "roce_percentage_y",
    ],
    errors="ignore"
)

# ==========================================================
# Sector Median PE Analysis
# ==========================================================

# Required Columns:
# company_name
# broad_sector
# pe_ratio

# Remove duplicate companies (keep latest)
valuation_df = (
    valuation_df
    .drop_duplicates(subset="company_id", keep="last")
    .copy()
)

# Convert PE Ratio to numeric
valuation_df["pe_ratio"] = pd.to_numeric(
    valuation_df["pe_ratio"],
    errors="coerce"
)

# Ignore companies where PE is missing
sector_pe_source = valuation_df.dropna(
    subset=["broad_sector", "pe_ratio"]
)

# Calculate Sector Median PE
sector_median = (
    sector_pe_source
    .groupby("broad_sector", as_index=False)
    .agg(
        sector_median_pe=("pe_ratio", "median"),
        company_count=("company_id", "count")
    )
)

# Merge sector median back
valuation_df = valuation_df.merge(
    sector_median,
    on="broad_sector",
    how="left"
)

# ==========================================================
# Premium / Discount vs Sector
# ==========================================================

valuation_df["pe_vs_sector_median_pct"] = (
    (
        valuation_df["pe_ratio"] -
        valuation_df["sector_median_pe"]
    )
    /
    valuation_df["sector_median_pe"]
) * 100

valuation_df["pe_vs_sector_median_pct"] = (
    valuation_df["pe_vs_sector_median_pct"]
    .round(2)
)

# ==========================================================
# Valuation Flag
# ==========================================================

def valuation_flag(row):

    pe = row["pe_ratio"]
    sector = row["sector_median_pe"]

    if pd.isna(pe):
        return "Unknown"

    if pd.isna(sector):
        return "Unknown"

    premium = (
        (pe - sector)
        / sector
    ) * 100

    if premium >= 50:
        return "Caution"

    elif premium <= -30:
        return "Discount"

    else:
        return "Fair"


valuation_df["flag"] = valuation_df.apply(
    valuation_flag,
    axis=1
)

# ==========================================================
# Final Summary
# ==========================================================

valuation_summary = valuation_df[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "fcf_yield_pct",
        "sector_median_pe",
        "company_count",
        "pe_vs_sector_median_pct",
        "flag",
    ]
].rename(
    columns={
        "broad_sector": "sector",
        "sector_median_pe": "sector_median_pe",
    }
)

# Sort by Sector then Company
valuation_summary = valuation_summary.sort_values(
    ["sector", "company_name"],
    na_position="last"
).reset_index(drop=True)

# ==========================================================
# Export
# ==========================================================

valuation_summary.to_excel(
    OUTPUT_DIR / "valuation_summary.xlsx",
    index=False
)

valuation_summary.query(
    "flag in ['Caution','Discount']"
).to_csv(
    OUTPUT_DIR / "valuation_flags.csv",
    index=False
)

# ==========================================================
# Console Output
# ==========================================================

print("\n" + "="*60)
print("VALUATION ANALYSIS COMPLETED")
print("="*60)

print(f"\nTotal Companies        : {len(valuation_summary)}")

print("\nFlag Distribution")
print(
    valuation_summary["flag"]
    .value_counts(dropna=False)
)

print("\nSector Median PE")
print(
    sector_median.sort_values("sector_median_pe")
)

print("\nTop 10 Premium Companies")
print(
    valuation_summary.sort_values(
        "pe_vs_sector_median_pct",
        ascending=False
    )[
        [
            "company_name",
            "sector",
            "pe_ratio",
            "sector_median_pe",
            "pe_vs_sector_median_pct",
        ]
    ].head(10)
)

print("\nTop 10 Discount Companies")
print(
    valuation_summary.sort_values(
        "pe_vs_sector_median_pct"
    )[
        [
            "company_name",
            "sector",
            "pe_ratio",
            "sector_median_pe",
            "pe_vs_sector_median_pct",
        ]
    ].head(10)
)

print("\nOutput Files Created")
print("- valuation_summary.xlsx")
print("- valuation_flags.csv")