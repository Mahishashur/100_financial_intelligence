import sqlite3
import pandas as pd
from pathlib import Path


DB = "nifty100.db"

DATA = Path(
    "data/processed"
)


conn = sqlite3.connect(
    DB
)


files = list(
    DATA.glob(
        "*.csv"
    )
)


for f in files:

    table = f.stem.replace(
        "_clean",
        ""
    )

    print(
        f"Loading {table}"
    )

    df = pd.read_csv(
        f
    )

    df.to_sql(

        table,

        conn,

        if_exists="replace",

        index=False

    )

    print(
        f"Loaded {len(df)} rows"
    )


conn.close()

print(
    "\nDB Load Complete"
)