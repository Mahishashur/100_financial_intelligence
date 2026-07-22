from pathlib import Path
import pandas as pd

# Paths

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = BASE_DIR / "output"

parsed_file = OUTPUT_DIR / "analysis_parsed.csv"

if not parsed_file.exists():
    raise FileNotFoundError(
        "analysis_parsed.csv not found. Run parser.py first."
    )

parsed_df = pd.read_csv(parsed_file)

print("\nParsed Dataset Shape :", parsed_df.shape)

print("\nColumns")
print(parsed_df.columns.tolist())

print("\nPreview")
print(parsed_df.head())

# Metric Lookup Function

def get_metric(company_df, metric_type, period):

    result = company_df[
        (company_df["metric_type"] == metric_type) &
        (company_df["period_years"] == period)
    ]

    if result.empty:
        return None

    return float(result.iloc[0]["value_pct"])

# Function Test

company = "HDFCBANK"

company_df = parsed_df[
    parsed_df["company_id"] == company
]

print(f"\nTesting Company : {company}")

print("Sales 10Y :", get_metric(company_df, "compounded_sales_growth", 10))
print("Sales 5Y  :", get_metric(company_df, "compounded_sales_growth", 5))
print("Sales 3Y  :", get_metric(company_df, "compounded_sales_growth", 3))
print("Sales TTM :", get_metric(company_df, "compounded_sales_growth", 0))

print()

print("ROE 10Y   :", get_metric(company_df, "roe", 10))
print("ROE 5Y    :", get_metric(company_df, "roe", 5))
print("ROE 3Y    :", get_metric(company_df, "roe", 3))
print("ROE Last Year :", get_metric(company_df, "roe", 1))

# Insight Generator

def generate_insights(company_df):

    pros = []
    cons = []
    score = 0

    # Fetch metrics

    sales10 = get_metric(company_df, "compounded_sales_growth", 10)
    sales5 = get_metric(company_df, "compounded_sales_growth", 5)
    sales3 = get_metric(company_df, "compounded_sales_growth", 3)
    sales_ttm = get_metric(company_df, "compounded_sales_growth", 0)

    profit10 = get_metric(company_df, "compounded_profit_growth", 10)
    profit5 = get_metric(company_df, "compounded_profit_growth", 5)
    profit3 = get_metric(company_df, "compounded_profit_growth", 3)
    profit_ttm = get_metric(company_df, "compounded_profit_growth", 0)

    stock10 = get_metric(company_df, "stock_price_cagr", 10)

    roe10 = get_metric(company_df, "roe", 10)
    roe_last = get_metric(company_df, "roe", 1)

    # Rule 1 - ROE Quality

    if roe10 is not None:

        if roe10 >= 25:
            score += 25
            pros.append(
            f"Excellent long-term ROE ({roe10:.1f}%), indicating highly efficient capital allocation."
        )

        elif roe10 >= 20:
            score += 20
            pros.append(
            f"Strong long-term ROE ({roe10:.1f}%), reflecting healthy profitability."
        )

        elif roe10 >= 15:
            score += 15
            pros.append(
            f"Decent long-term ROE ({roe10:.1f}%), showing stable business performance."
        )

        else:
            score -= 15
            cons.append(
            f"Low long-term ROE ({roe10:.1f}%), indicating weaker capital efficiency."
        )

# Rule 2 - Long-term Sales Growth

    if sales10 is not None:

        if sales10 >= 20:
            score += 20
            pros.append(
            f"Excellent 10-year sales CAGR ({sales10:.1f}%), demonstrating sustained business expansion."
        )

        elif sales10 >= 15:
            score += 15
            pros.append(
            f"Healthy long-term sales growth ({sales10:.1f}%)."
        )

        elif sales10 >= 10:
            score += 10
            pros.append(
            f"Moderate sales growth ({sales10:.1f}%)."
        )

        else:
            score -= 15
            cons.append(
            f"Weak long-term sales growth ({sales10:.1f}%)."
        )
            
# Rule 3 - Growth Trend

    if None not in (sales10, sales5, sales3):

        if sales10 < sales5 < sales3:

            pros.append(
            "Sales growth has accelerated over recent years."
        )

        elif sales10 > sales5 > sales3:

            cons.append(
            "Sales growth has gradually slowed over time."
        )
            
# Rule 4 - Profit Growth Trend

    if None not in (profit10, profit5, profit3):

        if profit10 < profit5 < profit3:

            pros.append(
            "Profit growth has accelerated over recent years."
        )

        elif profit10 > profit5 > profit3:

            cons.append(
            "Profit growth has gradually slowed over time."
        )        
    
# Rule 5 - Stock vs Business Growth

    if stock10 is not None and profit10 is not None:

        difference = profit10 - stock10

        if difference >= 5:

            pros.append(
            "Business profit growth is significantly ahead of stock returns, indicating potential valuation upside."
        )

        elif difference <= -5:

            cons.append(
            "Stock returns have outpaced business profit growth, suggesting possible overvaluation."
        )        
      
# Default Messages

    if not pros:
        pros.append("No significant strengths identified from available metrics.")

    if not cons:
        cons.append("No major concerns identified based on available metrics.") 
    if score >= 45:
        rating = "Excelent"
    elif score >= 35:
        rating = "Good"
    elif score >= 20:
        rating = "Average"
        
    else:
        rating ="Weak"            
    return pros, cons, score, rating

print("\n" + "=" * 60)

pros, cons, score, rating = generate_insights(company_df)

print("PROS")
for p in pros:
    print("PROS:", p)

print("\nCONS")
for c in cons:
    print("CONS:", c)
    
# Executive Summary Generator

def generate_summary(score, rating, pros, cons):

    real_cons = [
        c for c in cons
        if "No major concerns" not in c
    ]

    if rating == "Excellent":

        return (
            f"Excellent company with {len(pros)} key strengths "
            f"and strong long-term financial performance."
        )

    elif rating == "Good":

        return (
            f"Financially healthy company with {len(pros)} positive "
            f"investment indicators."
        )

    elif rating == "Average":

        return (
            f"Company shows balanced strengths and weaknesses "
            f"requiring selective evaluation."
        )

    else:

        if real_cons:

            return (
                "Business fundamentals show multiple concerns "
                "that require careful evaluation."
            )

        return (
            "Business performance is mixed and should be monitored."
        )
    
# Generate Insights for All Companies

all_insights = []

companies = sorted(parsed_df["company_id"].unique())

for company in companies:

    company_df = parsed_df[
        parsed_df["company_id"] == company
    ]
    
    pros, cons, score, rating = generate_insights(company_df)
    summary = generate_summary(
        score,
        rating,
        pros,
        cons
    )

    all_insights.append(
        {
            "company_id": company,
            "score":score,
            "rating": rating,
            "summary":summary,
            "pros": " | ".join(pros),
            "cons": " | ".join(cons),
            "pros_count": len(pros),
            "cons_count": len(cons),
        }
    )


insights_df = (pd.DataFrame(all_insights)
               .sort_values("score", ascending = False)
               .reset_index(drop=True))

print("\nInvestment Summary\n")

print(insights_df[[
            "company_id",
            "score",
            "rating",
            "summary"
        ]]
)

print("\nGenerated Insights")
print(insights_df)

# Export Insights


output_file = OUTPUT_DIR / "company_insights.csv"

insights_df.to_csv(output_file, index=False)

print(f"\n✓ Insights exported to: {output_file}")