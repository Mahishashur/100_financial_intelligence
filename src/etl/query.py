import sqlite3
import pandas as pd


conn = sqlite3.connect(
"nifty100.db"
)


q="""

SELECT
name

FROM sqlite_master

WHERE type='table'

"""


print(

pd.read_sql(
q,
conn
)

)