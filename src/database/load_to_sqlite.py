from pathlib import Path
import sqlite3
import pandas as pd

# Paths
DATA = Path("data/processed")
DB = Path("data/output/financial.db")

# Remove old database if exists
if DB.exists():
    DB.unlink()

# Create new database
conn = sqlite3.connect(DB)

# Load every cleaned CSV
for file in DATA.glob("*_clean.csv"):

    table = file.stem.replace("_clean", "")

    print(f"Loading {table}...")

    df = pd.read_csv(file)

    df.to_sql(
        table,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"{table} : {len(df)} rows")

conn.close()

print("\nDatabase Created Successfully!")

conn = sqlite3.connect("data/output/financial.db")

cursor = conn.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""")

print(cursor.fetchall())

conn.close()