import sqlite3
import pandas as pd


conn = sqlite3.connect(
"nifty100.db"
)


df = pd.read_sql(

"""

SELECT *

FROM profitandloss

""",

conn

)


bad = df[

df["sales"]<0

]


print(

"Negative Sales:",

len(

bad

)

)


conn.close()