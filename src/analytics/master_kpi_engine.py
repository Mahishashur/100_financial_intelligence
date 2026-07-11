import sqlite3
import pandas as pd
from profitability_engine import add_profitability_kpis
from leverage_engine import add_leverage_kpis
from cashflow_engine import add_cashflow_kpis
from efficiency_engine import add_efficiency_kpis
from growth_engine import add_growth_kpis
from capital_engine import add_capital_kpis

from ratios import (
    calculate_npm,
    calculate_opm,
    calculate_roe,
    calculate_roce,
    calculate_roa,
    calculate_debt_to_equity,
    calculate_interest_coverage,
    calculate_asset_turnover,
    calculate_free_cash_flow,
    calculate_ocf_margin,
    calculate_net_debt,
    calculate_financial_leverage,
    calculate_debt_ratio
)

conn = sqlite3.connect("data/output/financial.db")
query = """
SELECT

p.company_id,
p.year,

p.sales,
p.operating_profit,
p.net_profit,
p.other_income,
p.interest,
p.dividend_payout,

b.equity_capital,
b.reserves,
b.borrowings,
b.investments,
b.total_liabilities,
b.other_liabilities,
b.total_assets,
b.fixed_assets,

c.operating_activity,
c.investing_activity,
c.financing_activity

FROM profitandloss p

LEFT JOIN balancesheet b
ON p.company_id = b.company_id
AND p.year = b.year

LEFT JOIN cashflow c
ON p.company_id = c.company_id
AND p.year = c.year

ORDER BY
p.company_id,
p.year
"""

master_df = pd.read_sql(query, conn)

print(master_df.shape)
print(master_df.head())


master_df["npm"] = master_df.apply(
    lambda row: calculate_npm(
        row["net_profit"],
        row["sales"]
    ),
    axis=1
)
master_df = add_profitability_kpis(master_df)

master_df["opm"] = master_df.apply(
    lambda row: calculate_opm(
        row["operating_profit"],
        row["sales"]
    ),
    axis=1
)

master_df["debt_to_equity"] = master_df.apply(
    lambda row: calculate_debt_to_equity(
        row["borrowings"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)


print(
    master_df[
        [
            "company_id",
            "year",
            "npm",
            "opm",
            "debt_to_equity"
        ]
    ].head(20)
)


master_df.to_csv(
    "data/output/financial_kpis.csv",
    index=False
)

print("financial_kpis.csv exported successfully!")


master_df["roe"] = master_df.apply(
    lambda row: calculate_roe(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)

master_df["roa"] = master_df.apply(
    lambda row: calculate_roa(
        row["net_profit"],
        row["total_assets"]
    ),
    axis=1
)

master_df["interest_coverage"] = master_df.apply(
    lambda row: calculate_interest_coverage(
        row["operating_profit"],
        row["other_income"],
        row["interest"]
    ),
    axis=1
)


master_df["free_cash_flow"] = master_df.apply(
    lambda row: calculate_free_cash_flow(
        row["operating_activity"],
        row["investing_activity"]
    ),
    axis=1
)

master_df["ocf_margin"] = master_df.apply(
    lambda row: calculate_ocf_margin(
        row["operating_activity"],
        row["sales"]
    ),
    axis=1
)

print(
    master_df[
        [
            "company_id",
            "year",
            "npm",
            "opm",
            "roe",
            "roa",
            "debt_to_equity",
            "interest_coverage",
            "free_cash_flow",
            "ocf_margin"
        ]
    ].head(20)
)

master_df.to_csv(
    "data/output/financial_kpis.csv",
    index=False
)

print("financial_kpis.csv exported successfully")

master_df["roce"] = master_df.apply(
    lambda row: calculate_roce(
        row["operating_profit"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"]
    ),
    axis=1
)

master_df["asset_turnover"] = master_df.apply(
    lambda row: calculate_asset_turnover(
        row["sales"],
        row["total_assets"]
    ),
    axis=1
)

master_df["net_debt"] = master_df.apply(
    lambda row: calculate_net_debt(
        row["borrowings"],
        row["investments"]
    ),
    axis=1
)

master_df["financial_leverage"] = master_df.apply(
    lambda row: calculate_financial_leverage(
        row["total_assets"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)

master_df["debt_ratio"] = master_df.apply(
    lambda row: calculate_debt_ratio(
        row["borrowings"],
        row["total_assets"]
    ),
    axis=1
)

print(
    master_df[
        [
            "company_id",
            "year",
            "roce",
            "asset_turnover",
            "net_debt",
            "financial_leverage",
            "debt_ratio"
        ]
    ].head(15)
)

master_df = add_profitability_kpis(master_df)
master_df = add_leverage_kpis(master_df)
print(
    master_df[
        [
            "company_id",
            "year",
            "debt_to_equity",
            "interest_coverage",
            "net_debt",
            "financial_leverage",
            "debt_ratio"
        ]
    ].head(15)
)
master_df = add_cashflow_kpis(master_df)
print(
    master_df[
        [
            "company_id",
            "year",
            "free_cash_flow",
            "cfo_quality",
            "fcf_conversion",
            "capex_intensity",
            "ocf_margin",
            "cash_conversion_ratio",
            "cash_reinvestment_ratio"
        ]
    ].head(15)
)

master_df = add_efficiency_kpis(master_df)
print(
    master_df[
        [
            "company_id",
            "year",
            "asset_turnover",
            "capital_employed_turnover",
            "net_asset_turnover"
        ]
    ].head(15)
)


master_df = add_growth_kpis(master_df)
print(master_df[
        [
            "company_id",
            "sales_cagr_5yr",
            "profit_cagr_5yr",
            "book_value_cagr_5yr",
            "reserve_cagr_5yr",
            "operating_profit_cagr_5yr"
        ]
    ].head(15)
)

master_df = add_capital_kpis(master_df)
master_df.to_csv(
    "data/output/financial_kpis.csv",
    index=False
)

print("\nFinancial KPI Dataset Created Successfully!")

print(master_df.head())

print(master_df.shape)

master_df.to_csv(
    "data/output/financial_kpis.csv",
    index=False
)