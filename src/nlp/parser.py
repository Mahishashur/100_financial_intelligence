from pathlib import Path
import pandas as pd
import re

# Paths

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# Locate analysis.xlsx

analysis_files = list(RAW_DIR.rglob("analysis.xlsx"))

if not analysis_files:
    raise FileNotFoundError("analysis.xlsx not found.")

analysis_path = analysis_files[0]
print(f"\nUsing Analysis File:\n{analysis_path}")

# Load Excel

analysis_df = pd.read_excel(
    analysis_path,
    header=1
)

# Remove completely empty rows
analysis_df = analysis_df.dropna(how="all")

# Standardize column names
analysis_df.columns = (
    analysis_df.columns
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nShape :", analysis_df.shape)

print("\nColumns")
print(analysis_df.columns.tolist())

print("\nPreview")
print(analysis_df.head())

print("\nShape :", analysis_df.shape)
print("\nColumns:")
print(analysis_df.columns.tolist())

print("\nPreview:")
print(analysis_df.head())

# Regex Parser

PATTERN = re.compile(
    r"(?:(\d+)\s*Years?|Last\s*Year|TTM)\s*:?\s*(-?\d+(?:\.\d+)?)%",
    re.IGNORECASE,
)

def parse_metric(text):

    if pd.isna(text):
        return None

    text = str(text).strip()

    match = PATTERN.search(text)

    if not match:
        return None

    period = match.group(1)

    label = match.group(0).upper()

    if "TTM" in label:
        period = 0          # TTM (Trailing Twelve Months)

    elif period is None:
        period = 1          # Last Year

    else:
        period = int(period)

    value = float(match.group(2))
    return period, value


print("\nRegex Test")
test_columns = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

for column in test_columns:

    print(f"\n{column}")
    for value in analysis_df[column].head(5):
        print(value, " ---> ", parse_metric(value))
        
# Parse Entire Dataset

parsed_records = []
failed_records = []

metric_columns = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

for _, row in analysis_df.iterrows():
    company_id = row["company_id"]

    for metric in metric_columns:

        original_text = row[metric]
        result = parse_metric(original_text)

        if result is None:

            failed_records.append(
                {
                    "company_id": company_id,
                    "metric_type": metric,
                    "original_text": original_text,
                })

        else:

            period, value = result
            parsed_records.append(
                {
                    "company_id": company_id,
                    "metric_type": metric,
                    "period_years": period,
                    "value_pct": value,
                })
            
# Create Output DataFrames

parsed_df = pd.DataFrame(parsed_records)
failures_df = pd.DataFrame(failed_records)

print("\nParsed Records :", len(parsed_df))
print("Failed Records :", len(failures_df))

print("\nParsed Preview")
print(parsed_df.head())

print("\nFailures Preview")
print(failures_df.head())

# Export Results

parsed_file = OUTPUT_DIR / "analysis_parsed.csv"
failures_file = OUTPUT_DIR / "parse_failures.csv"

parsed_df.to_csv(parsed_file, index=False)
failures_df.to_csv(failures_file, index=False)

print("\nFiles Saved Successfully")
print(f" {parsed_file}")
print(f" {failures_file}")

# Validation Report

print("\n" + "=" * 60)
print("VALIDATION REPORT")
print("=" * 60)

# Basic Statistics
print(f"Total Source Rows : {len(analysis_df)}")
print(f"Unique Companies  : {analysis_df['company_id'].nunique()}")
print(f"Parsed Records    : {len(parsed_df)}")
print(f"Failed Parses     : {len(failures_df)}")

# Duplicate Check
duplicate_rows = parsed_df[
    parsed_df.duplicated(
        subset=[
            "company_id",
            "metric_type",
            "period_years"
        ],keep=False
    )
]
print(f"Duplicate Records: {len(duplicate_rows)}")

if not duplicate_rows.empty:
    print("\nDuplicate Details:")
    print(duplicate_rows.sort_values(
            ["company_id", "metric_type", "period_years"]).to_string(index=False)
    )

# Missing Values

print("\nMissing Values")
print(parsed_df.isna().sum())

# Metric Distribution

print("\nMetric Distribution")
print(parsed_df["metric_type"].value_counts())

# Period Distribution

print("\nPeriod Distribution")

print(
    parsed_df["period_years"]
    .value_counts()
    .sort_index()
)

# Company Distribution

print("\nCompany Distribution")
print(parsed_df["company_id"].value_counts())

# Validation Status


print("\n" + "-" * 60)
status = "PASSED"

if len(failures_df) > 0:
    status = "FAILED"

if len(duplicate_rows) > 0:
    status = "FAILED"

print(f"Validation Status : {status}")
print("=" * 60)

# Expected Record Validation

expected_per_company = len(metric_columns) * analysis_df.groupby("company_id").size()

print("\nExpected Records Per Company")

company_summary = (
    parsed_df.groupby("company_id")
    .size()
    .reset_index(name="actual_records")
)

company_summary["expected_records"] = company_summary["company_id"].map(expected_per_company)

company_summary["status"] = company_summary.apply(
    lambda row: "PASS"
    if row["actual_records"] == row["expected_records"]
    else "FAIL",
    axis=1,
)

print(company_summary.to_string(index=False))