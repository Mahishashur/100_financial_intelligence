import sqlite3
import pandas as pd


conn = sqlite3.connect(
"nifty100.db"
)

tables = [

"companies",

"profitandloss",

"balancesheet",

"cashflow",

"stock_prices"

]


for t in tables:

    print(
        f"\n=== {t} ==="
    )

    q=f"""

SELECT *

FROM {t}

LIMIT 5

"""

    print(

pd.read_sql(
q,
conn
)

)

conn.close()