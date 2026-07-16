import pandas as pd

df = pd.read_excel(
    "data/raw/core/prosandcons.xlsx",
    header=1
)

print(df.columns.tolist())
print(df.head())