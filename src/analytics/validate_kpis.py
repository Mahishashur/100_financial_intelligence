import pandas as pd

df = pd.read_csv("data/output/financial_kpis.csv")

print("=" * 50)
print("Dataset Shape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nFirst 5 Rows")
print(df.head())
