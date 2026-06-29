import sqlite3
import pandas as pd

from ratios import (

    calculate_npm,
    calculate_opm,
    calculate_roe,
    calculate_roce,
    calculate_roa

)


conn = sqlite3.connect("nifty100.db")

print("=" * 60)
print("CONNECTED TO DATABASE")
print("=" * 60)


query = """
SELECT

p.company_id,
p.year,

p.sales,
p.net_profit,
p.operating_profit,
p.opm_percentage,

b.equity_capital,
b.reserves,
b.borrowings,
b.total_assets

FROM profitandloss p

JOIN balancesheet b

ON p.company_id = b.company_id
AND p.year = b.year
"""

df = pd.read_sql(query, conn)
print(df.head())
print("\nRows:", len(df))


df["net_profit_margin_pct"] = df.apply(
    lambda row: calculate_npm(
        row["sales"],
        row["net_profit"]
    ),
    axis=1
)


df["opm_calculated_pct"] = df.apply(
    lambda row: calculate_opm(
        row["sales"],
        row["operating_profit"]
    ),
    axis=1
)


df["roe_calculated_pct"] = df.apply(
    lambda row: calculate_roe(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)


df["roce_calculated_pct"] = df.apply(
    lambda row: calculate_roce(
        row["operating_profit"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"]
    ),
    axis=1
)


df["roa_calculated_pct"] = df.apply(
    lambda row: calculate_roa(
        row["net_profit"],
        row["total_assets"]
    ),
    axis=1
)

print(df.head())
conn.close()