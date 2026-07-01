import sqlite3
import pandas as pd

from ratios import (

    calculate_npm,
    calculate_opm,
    calculate_roe,
    calculate_roce,
    calculate_roa,
    calculate_debt_to_equity,
    high_leverage_flag,
    calculate_interest_coverage,
    get_icr_label,
    calculate_net_debt,
    calculate_asset_turnover


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
p.other_income,
p.interest,

b.equity_capital,
b.reserves,
b.borrowings,
b.total_assets,
b.investments,

s.broad_sector

FROM profitandloss p

JOIN balancesheet b
ON p.company_id = b.company_id
AND p.year = b.year

JOIN sectors s
ON p.company_id = s.company_id
"""

df = pd.read_sql(query, conn)
print(df.head())
print("\nRows:", len(df))


df["net_profit_margin_pct"] = df.apply(
    lambda row: calculate_npm(
        row["sales"],
        row["net_profit"]
    ),axis=1
)


df["opm_calculated_pct"] = df.apply(
    lambda row: calculate_opm(
        row["sales"],
        row["operating_profit"]
    ),axis=1
)


df["roe_calculated_pct"] = df.apply(
    lambda row: calculate_roe(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"]
    ),axis=1
)


df["roce_calculated_pct"] = df.apply(
    lambda row: calculate_roce(
        row["operating_profit"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"]
    ),axis=1
)


df["roa_calculated_pct"] = df.apply(
    lambda row: calculate_roa(
        row["net_profit"],
        row["total_assets"]
    ),axis=1
)

print(df.head())
conn.close()

df["debt_to_equity"] = df.apply(

    lambda row: 
        
        calculate_debt_to_equity(

        row["borrowings"],
        row["equity_capital"],
        row["reserves"]
        
       ),axis=1

)


print("\nDEBT TO EQUITY")

print(

df[

[

"company_id",

"year",

"borrowings",

"equity_capital",

"reserves",

"debt_to_equity"

]

].head()

)


df["high_leverage_flag"] = df.apply(

    lambda row:

    high_leverage_flag(

        row["debt_to_equity"],

        row["broad_sector"]

    ),axis=1

)


print("\nHIGH LEVERAGE FLAG")

print(

df[

[
"company_id",
"broad_sector",
"debt_to_equity",
"high_leverage_flag"

]

].head(15)

)


df["interest_coverage"] = df.apply(

    lambda row:

    calculate_interest_coverage(

        row["operating_profit"],

        row["other_income"],

        row["interest"]

    ),axis=1
)


df["icr_label"] = df.apply(

    lambda row:

    get_icr_label(

        row["interest"]

    ),

    axis=1

)


print("\nINTEREST COVERAGE")

print(

df[

[
"company_id",
"year",
"operating_profit",
"other_income",
"interest",
"interest_coverage",
"icr_label"

]

].head(15)

)


df["net_debt"] = df.apply(

    lambda row:

    calculate_net_debt(

        row["borrowings"],

        row["investments"]

    ),axis=1

)


print("\nNET DEBT")

print(

df[

[
    "company_id",
    "year",
    "borrowings",
    "investments",
    "net_debt"
]

].head(15)

)


df["asset_turnover"] = df.apply(

    lambda row:

    calculate_asset_turnover(

        row["sales"],

        row["total_assets"]

    ),axis=1
)


print("\nASSET TURNOVER")

print(

df[

[
    "company_id",
    "year",
    "sales",
    "total_assets",
    "asset_turnover"
]

].head(15)

)


