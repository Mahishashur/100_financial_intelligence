import sqlite3
import pandas as pd

from ratios import (
    high_leverage_flag,
    calculate_interest_coverage,
    get_icr_label,
    calculate_net_debt,
    calculate_asset_turnover,
    calculate_free_cash_flow,
    calculate_cfo_quality,
    calculate_fcf_conversion,
    calculate_capex_intensity,
    calculate_ocf_margin,
    calculate_cash_conversion_ratio,
    calculate_cash_reinvestment_ratio,
    calculate_retention_ratio,
    calculate_financial_leverage,
    calculate_debt_ratio,
    calculate_capital_employed_turnover,
    calculate_net_asset_turnover,
    calculate_investment_ratio,
    calculate_fixed_asset_ratio,
     calculate_reserve_to_equity_ratio
)

from profitability_engine import profitability_analysis

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

df = profitability_analysis(df)
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

]].head(15)

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
    ),axis=1
)


print("\nINTEREST COVERAGE")
print(df[[
"company_id",
"year",
"operating_profit",
"other_income",
"interest",
"interest_coverage",
"icr_label"

]].head(15)

)


df["net_debt"] = df.apply(

    lambda row:

    calculate_net_debt(
        row["borrowings"],
        row["investments"]
    ),axis=1
)


print("\nNET DEBT")
print(df[[
    "company_id",
    "year",
    "borrowings",
    "investments",
    "net_debt"
]].head(15)
)


df["asset_turnover"] = df.apply(

    lambda row:

    calculate_asset_turnover(
        row["sales"],
        row["total_assets"]

    ),axis=1
)


print("\nASSET TURNOVER")
print(df[[
    "company_id",
    "year",
    "sales",
    "total_assets",
    "asset_turnover"
]].head(15)
)


# Revenue CAGR data

conn = sqlite3.connect("nifty100.db")

query = """
SELECT

company_id,
year,
sales

FROM profitandloss

ORDER BY
company_id,
year
"""

cagr_df = pd.read_sql(query, conn)

print("\nREVENUE DATA")

print(cagr_df.head(15))



abb = cagr_df[
    cagr_df["company_id"] == "ABB"
]

print("\nABB SALES HISTORY")
print(abb)


start_sales = abb.iloc[-6]["sales"]

end_sales = abb.iloc[-1]["sales"]

print(start_sales)

print(end_sales)


from cagr import calculate_cagr

value, flag = calculate_cagr(
    start_sales,end_sales,5

)

print("\nABB 5 YEAR CAGR")

print("Value :", value)

print("Flag :", flag)

# Remove TTM

abb = abb[
    abb["year"] != "TTM"
]

print("\nABB WITHOUT TTM")
print(abb)


start_sales = abb.iloc[-6]["sales"]
end_sales = abb.iloc[-1]["sales"]
print(start_sales)
print(end_sales)


value, flag = calculate_cagr(
start_sales,end_sales,5
)

print("\nABB 5 YEAR CAGR")

print(value)

print(flag)

# Revenue CAGR for all companies

results = []

companies = cagr_df["company_id"].unique()

for company in companies:

    company_df = cagr_df[
        cagr_df["company_id"] == company
    ]

    company_df = company_df[
        company_df["year"] != "TTM"
    ]

    if len(company_df) < 6:

        results.append({
            "company_id": company,
            "revenue_cagr_5yr": None,
            "flag": "INSUFFICIENT"
        })

        continue

    start_sales = company_df.iloc[-6]["sales"]
    end_sales = company_df.iloc[-1]["sales"]

    value, flag = calculate_cagr(
        start_sales,
        end_sales,
        5
    )

    results.append({
        "company_id": company,
        "revenue_cagr_5yr": value,
        "flag": flag
    })


result_df = pd.DataFrame(results)
    
    
result_df = pd.DataFrame(results)

print("\nREVENUE CAGR RESULTS")

print(result_df.head(10))

print("\nTotal Rows :", len(result_df))

# PAT data

query = """
SELECT

company_id,
year,
net_profit

FROM profitandloss

ORDER BY
company_id,
year
"""

pat_df = pd.read_sql(query, conn)

print("\nPAT DATA")

print(pat_df.head())

# PAT CAGR for all companies

pat_results = []

companies = pat_df["company_id"].unique()

for company in companies:

    company_df = pat_df[
        pat_df["company_id"] == company
    ]

    # Remove TTM
    company_df = company_df[
        company_df["year"] != "TTM"
    ]

    # Less than 6 years of data
    if len(company_df) < 6:

        pat_results.append({

            "company_id": company,

            "pat_cagr_5yr": None,

            "flag": "INSUFFICIENT"

        })

        continue

    start_pat = company_df.iloc[-6]["net_profit"]

    end_pat = company_df.iloc[-1]["net_profit"]

    value, flag = calculate_cagr(

        start_pat,

        end_pat,5

    )

    pat_results.append({

        "company_id": company,

        "pat_cagr_5yr": value,

        "flag": flag

    })
    
    
    pat_result_df = pd.DataFrame(pat_results)

print("\nPAT CAGR RESULTS")

print(pat_result_df.head(10))

print("\nTotal Rows :", len(pat_result_df))

# EPS Data

query = """
SELECT

company_id,
year,
eps

FROM profitandloss

ORDER BY
company_id,
year
"""

eps_df = pd.read_sql(query, conn)

print("\nEPS DATA")

print(eps_df.head())

# EPS CAGR

eps_results = []

companies = eps_df["company_id"].unique()

for company in companies:

    company_df = eps_df[
        eps_df["company_id"] == company
    ]

    company_df = company_df[
        company_df["year"] != "TTM"
    ]

    if len(company_df) < 6:

        eps_results.append({

            "company_id": company,

            "eps_cagr_5yr": None,

            "flag": "INSUFFICIENT"

        })

        continue

    start_eps = company_df.iloc[-6]["eps"]

    end_eps = company_df.iloc[-1]["eps"]

    value, flag = calculate_cagr(

        start_eps,

        end_eps,

        5

    )

    eps_results.append({

        "company_id": company,

        "eps_cagr_5yr": value,

        "flag": flag

    })
    

eps_result_df = pd.DataFrame(eps_results)

print("\nEPS CAGR RESULTS")

print(eps_result_df.head(10))

print("\nRows :", len(eps_result_df))

# Merge all CAGR results

result_df = result_df.rename(columns={
    "flag": "revenue_flag"
})

pat_result_df = pat_result_df.rename(columns={
    "flag": "pat_flag"
})

eps_result_df = eps_result_df.rename(columns={
    "flag": "eps_flag"
})


growth_df = result_df.merge(

    pat_result_df,

    on="company_id",

    how="left"

)

growth_df = growth_df.merge(

    eps_result_df,

    on="company_id",

    how="left"

)

print("\nGROWTH DATA")

print(growth_df.head())

print("\nRows :", len(growth_df))

growth_df.to_csv(

    "output/growth_metrics.csv",

    index=False

)

print("\nGrowth Metrics Saved")
print("\nMissing Values")

print(growth_df.isnull().sum())

# Cashflow data

query = """
SELECT

company_id,
year,
operating_activity,
investing_activity,
financing_activity

FROM cashflow

ORDER BY
company_id,
year
"""

cash_df = pd.read_sql(query, conn)

print("\nCASHFLOW DATA")

print(cash_df.head())


cash_df["free_cash_flow"] = cash_df.apply(

    lambda row:

    calculate_free_cash_flow(

        row["operating_activity"],

        row["investing_activity"]

    ),axis=1

)


print("\nFREE CASH FLOW")
print(cash_df[[

    "company_id",

    "year",

    "operating_activity",

    "investing_activity",

    "free_cash_flow"

]].head(15)

)


print("\nTotal Cashflow Rows :", len(cash_df))

print("\nDuplicate Company-Year:")

duplicates = cash_df[
    cash_df.duplicated(
        subset=["company_id", "year"],
        keep=False
    )
]

print(duplicates.head(20))
print(cash_df.columns.tolist())


query = """
SELECT *
FROM cashflow
WHERE company_id = 'ABB'
ORDER BY year
"""

abb_cf = pd.read_sql(query, conn)

print("\nABB CASHFLOW")

print(abb_cf)

query = """
SELECT
COUNT(*) AS total_rows,
COUNT(DISTINCT company_id || year) AS unique_company_year
FROM cashflow
"""

check_df = pd.read_sql(query, conn)

print(check_df)


query = """
SELECT
company_id,
year,
COUNT(*) AS cnt

FROM cashflow

GROUP BY company_id, year

HAVING COUNT(*) > 1

ORDER BY company_id, year
"""

dup_df = pd.read_sql(query, conn)

print("\nDUPLICATE COMPANY-YEAR")

print(dup_df)


query = """
SELECT COUNT(*)
FROM cashflow
"""

print(pd.read_sql(query, conn))


query = """
SELECT COUNT(*)
FROM cashflow
WHERE company_id='ABB'
"""

print(pd.read_sql(query, conn))

cash_raw = pd.read_excel(
    "data/raw/core/cashflow.xlsx",
    header=1
)

cash_raw.columns = (
    cash_raw.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

abb = cash_raw[cash_raw["company_id"] == "ABB"]


print(abb[[
            "year",
            "operating_activity",
            "investing_activity",
            "financing_activity",
            "net_cash_flow"
        ]]
)

# CFO quality

query = """
SELECT

c.company_id,
c.year,

c.operating_activity,

p.net_profit

FROM cashflow c

JOIN profitandloss p

ON c.company_id = p.company_id

AND c.year = p.year
"""

df = pd.read_sql(query, conn)
df["cfo_quality"] = df.apply(

    lambda row:

    calculate_cfo_quality(

        row["operating_activity"],

        row["net_profit"]

    ),axis=1
)

print("\nCFO QUALITY")

print(df[[
            "company_id",
            "year",
            "operating_activity",
            "net_profit",
            "cfo_quality"
        ]].head(15)
)


# FCF conversion

query = """
SELECT

c.company_id,
c.year,

c.operating_activity,
c.investing_activity,

p.net_profit

FROM cashflow c

JOIN profitandloss p

ON c.company_id = p.company_id

AND c.year = p.year
"""

df = pd.read_sql(query, conn)

df["free_cash_flow"] = df.apply(

    lambda row:

    calculate_free_cash_flow(

        row["operating_activity"],

        row["investing_activity"]

    ),axis=1
)

df["fcf_conversion"] = df.apply(

    lambda row:

    calculate_fcf_conversion(

        row["free_cash_flow"],

        row["net_profit"]

    ),axis=1
)

print("\nFCF CONVERSION")

print(df[[
    "company_id",
    "year",
    "free_cash_flow",
    "net_profit",
    "fcf_conversion"
]].head(15)

)

# CapEx intensity

query = """
SELECT

company_id,
year,

operating_activity,
investing_activity

FROM cashflow
"""

df = pd.read_sql(query, conn)
df["capex_intensity"] = df.apply(

    lambda row:

    calculate_capex_intensity(

        row["operating_activity"],

        row["investing_activity"]

    ),axis=1
)

print("\nCAPEX INTENSITY")

print(df[[
    "company_id",
    "year",
    "operating_activity",
    "investing_activity",
    "capex_intensity"
]].head(15)
)

# OCF margin

query = """
SELECT

c.company_id,
c.year,

c.operating_activity,

p.sales

FROM cashflow c

JOIN profitandloss p

ON c.company_id = p.company_id

AND c.year = p.year
"""
df = pd.read_sql(query, conn)
df["ocf_margin"] = df.apply(

    lambda row:

    calculate_ocf_margin(

        row["operating_activity"],

        row["sales"]

    ),axis=1
)

print("\nOCF MARGIN")

print(df[[
    "company_id",
    "year",
    "sales",
    "operating_activity",
    "ocf_margin"
]].head(15)
)

# Cash conversion ratio

query = """
SELECT

c.company_id,
c.year,

c.operating_activity,

p.operating_profit

FROM cashflow c

JOIN profitandloss p

ON c.company_id = p.company_id

AND c.year = p.year
"""
df = pd.read_sql(query, conn)
df["cash_conversion_ratio"] = df.apply(

    lambda row:

    calculate_cash_conversion_ratio(

        row["operating_activity"],

        row["operating_profit"]

    ),axis=1
)

print("\nCASH CONVERSION RATIO")

print(df[[
    "company_id",
    "year",
    "operating_profit",
    "operating_activity",
    "cash_conversion_ratio"
]].head(15)
)

# Cash reinvestment ratio

query = """
SELECT

c.company_id,
c.year,

c.operating_activity,

b.fixed_assets

FROM cashflow c

JOIN balancesheet b

ON c.company_id = b.company_id

AND c.year = b.year
"""
df = pd.read_sql(query, conn)
df["cash_reinvestment_ratio"] = df.apply(

    lambda row:

    calculate_cash_reinvestment_ratio(

        row["operating_activity"],

        row["fixed_assets"]

    ),axis=1
)

print("\nCASH REINVESTMENT RATIO")

print(df[[
    "company_id",
    "year",
    "fixed_assets",
    "operating_activity",
    "cash_reinvestment_ratio"
]].head(15)
)

# Retention ratio

query = """
SELECT

company_id,
year,

dividend_payout

FROM profitandloss
"""
df = pd.read_sql(query, conn)
df["retention_ratio"] = df.apply(

    lambda row:

    calculate_retention_ratio(

        row["dividend_payout"]

    ),axis=1
)
print("\nRETENTION RATIO")
print(df[[
    "company_id",
    "year",
    "dividend_payout",
    "retention_ratio"
]].head(15)
)

query = """
SELECT *
FROM balancesheet
LIMIT 5
"""

df = pd.read_sql(query, conn)

print(df.columns.tolist())


# Financial leverage

query = """
SELECT

company_id,
year,

total_assets,
equity_capital,
reserves

FROM balancesheet
"""
df = pd.read_sql(query, conn)

df["financial_leverage"] = df.apply(

    lambda row:

    calculate_financial_leverage(

        row["total_assets"],

        row["equity_capital"],

        row["reserves"]

    ),axis=1
)
print("\nFINANCIAL LEVERAGE")

print(df[[

    "company_id",
    "year",
    "total_assets",
    "equity_capital",
    "reserves",
    "financial_leverage"

]].head(15)

)

# Debt ratio

query = """
SELECT

company_id,
year,

borrowings,
total_assets

FROM balancesheet
"""
df = pd.read_sql(query, conn)
df["debt_ratio"] = df.apply(

    lambda row:

    calculate_debt_ratio(

        row["borrowings"],

        row["total_assets"]

    ),axis=1
)
print("\nDEBT RATIO")

print(df[[

    "company_id",
    "year",
    "borrowings",
    "total_assets",
    "debt_ratio"

]].head(15)
)


# Capital employed turnover

query = """
SELECT

p.company_id,
p.year,

p.sales,

b.equity_capital,
b.reserves,
b.borrowings

FROM profitandloss p

JOIN balancesheet b

ON p.company_id = b.company_id

AND p.year = b.year
"""
df = pd.read_sql(query, conn)
df["capital_employed_turnover"] = df.apply(

    lambda row:

    calculate_capital_employed_turnover(

        row["sales"],

        row["equity_capital"],

        row["reserves"],

        row["borrowings"]

    ),axis=1

)
print("\nCAPITAL EMPLOYED TURNOVER")

print(df[[

    "company_id",
    "year",
    "sales",
    "equity_capital",
    "reserves",
    "borrowings",
    "capital_employed_turnover"

]].head(15)
)

# NET asset turnover

query = """
SELECT

p.company_id,
p.year,

p.sales,

b.total_assets,
b.investments

FROM profitandloss p

JOIN balancesheet b

ON p.company_id = b.company_id

AND p.year = b.year
"""
df = pd.read_sql(query, conn)
df["net_asset_turnover"] = df.apply(

    lambda row:

    calculate_net_asset_turnover(

        row["sales"],

        row["total_assets"],

        row["investments"]

    ),axis=1
)
print("\nNET ASSET TURNOVER")

print(df[[

    "company_id",
    "year",
    "sales",
    "total_assets",
    "investments",
    "net_asset_turnover"

]].head(15)
)


# Investment ratio

query = """
SELECT

company_id,
year,

investments,
total_assets

FROM balancesheet
"""
df = pd.read_sql(query, conn)
df["investment_ratio"] = df.apply(

    lambda row:

    calculate_investment_ratio(

        row["investments"],

        row["total_assets"]

    ),axis=1
)
print("\nINVESTMENT RATIO")

print(df[[

    "company_id",
    "year",
    "investments",
    "total_assets",
    "investment_ratio"

]].head(15)
)


# Fixed asset ratio

query = """
SELECT

company_id,
year,

fixed_assets,
total_assets

FROM balancesheet
"""
df = pd.read_sql(query, conn)
df["fixed_asset_ratio"] = df.apply(

    lambda row:

    calculate_fixed_asset_ratio(

        row["fixed_assets"],

        row["total_assets"]

    ),axis=1
)
print("\nFIXED ASSET RATIO")

print(df[[

    "company_id",
    "year",
    "fixed_assets",
    "total_assets",
    "fixed_asset_ratio"

]].head(15)
)


# Reserve to equity ratio

query = """
SELECT

company_id,
year,

equity_capital,
reserves

FROM balancesheet
"""
df = pd.read_sql(query, conn)
df["reserve_to_equity_ratio"] = df.apply(

    lambda row:

    calculate_reserve_to_equity_ratio(

        row["reserves"],

        row["equity_capital"]

    ),axis=1
)
print("\nRESERVE TO EQUITY RATIO")

print(df[[

    "company_id",
    "year",
    "equity_capital",
    "reserves",
    "reserve_to_equity_ratio"

]].head(15)
)


# Reserve CAGR (5 year)

query = """
SELECT

company_id,
year,
reserves

FROM balancesheet

ORDER BY
company_id,
year
"""
reserve_df = pd.read_sql(query, conn)
reserve_df = reserve_df[
    reserve_df["year"] != "TTM"
]
results = []

companies = reserve_df["company_id"].unique()

for company in companies:

    company_df = reserve_df[
        reserve_df["company_id"] == company
    ]

    if len(company_df) < 6:

        results.append({

            "company_id": company,

            "reserve_cagr_5yr": None,

            "flag": "INSUFFICIENT"

        })

        continue

    start_value = company_df.iloc[-6]["reserves"]
    end_value = company_df.iloc[-1]["reserves"]

    value, flag = calculate_cagr(

        start_value,
        end_value,5

    )

    results.append({

        "company_id": company,

        "reserve_cagr_5yr": value,

        "flag": flag

    })
reserve_result = pd.DataFrame(results)
print("\nRESERVE CAGR")

print(reserve_result.head(15))

print("\nTotal Rows :", len(reserve_result))


# Operating profit CAGR (5 year)

query = """
SELECT

company_id,
year,
operating_profit

FROM profitandloss

ORDER BY
company_id,
year
"""
op_df = pd.read_sql(query, conn)

results = []

companies = op_df["company_id"].unique()

for company in companies:

    company_df = op_df[
        op_df["company_id"] == company
    ]

    if len(company_df) < 6:

        results.append({

            "company_id": company,

            "operating_profit_cagr_5yr": None,

            "flag": "INSUFFICIENT"

        })

        continue

    start_value = company_df.iloc[-6]["operating_profit"]
    end_value = company_df.iloc[-1]["operating_profit"]

    value, flag = calculate_cagr(
        start_value,
        end_value,5
    )

    results.append({

        "company_id": company,

        "operating_profit_cagr_5yr": value,

        "flag": flag

    })

op_result = pd.DataFrame(results)

print("\nOPERATING PROFIT CAGR")

print(op_result.head(15))

print("\nTotal Rows:", len(op_result))


# Book value CAGR (5 year)

query = """
SELECT

company_id,
year,

equity_capital,
reserves

FROM balancesheet

ORDER BY
company_id,
year
"""

bv_df = pd.read_sql(query, conn)

# Remove TTM rows if present
bv_df = bv_df[
    bv_df["year"] != "TTM"
]

import numpy as np

# Calculate Book Value
bv_df["book_value"] = np.where(
    bv_df["equity_capital"] > 0,
    (bv_df["equity_capital"] + bv_df["reserves"]) /
    bv_df["equity_capital"],
    np.nan
)

results = []

companies = bv_df["company_id"].unique()

for company in companies:

    company_df = bv_df[
        bv_df["company_id"] == company
    ]

    if len(company_df) < 6:

        results.append({

            "company_id": company,

            "book_value_cagr_5yr": None,

            "flag": "INSUFFICIENT"

        })

        continue

    start_value = company_df.iloc[-6]["book_value"]
    end_value = company_df.iloc[-1]["book_value"]

    value, flag = calculate_cagr(
        start_value,
        end_value,5
    )

    results.append({

        "company_id": company,

        "book_value_cagr_5yr": value,

        "flag": flag

    })

bv_result = pd.DataFrame(results)

print("\nBOOK VALUE CAGR")

print(bv_result.head(15))

print("\nTotal Rows:", len(bv_result))
conn.close()