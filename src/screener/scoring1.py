import pandas as pd


def winsorize_series(series):

    """
    Clip values between 10th and 90th percentile.
    """

    lower = series.quantile(0.10)

    upper = series.quantile(0.90)

    return series.clip(lower, upper)

def normalize_score(series, reverse=False):
    """
    Normalize any metric to a 0-100 score.
    """

    series = winsorize_series(series)

    minimum = series.min()

    maximum = series.max()

    if minimum == maximum:
        return pd.Series(50, index=series.index)

    score = (series - minimum) / (maximum - minimum) * 100

    if reverse:
        score = 100 - score

    return score

def positive_flag(series):
    """
    Positive values become 100, otherwise 0.
    """

    return series.apply(
        lambda x: 100 if x > 0 else 0
    )
    
def calculate_composite_score(df):

    # Profitability (35%)

    roe_score = normalize_score(df["roe_calculated_pct"])

    roce_score = normalize_score(df["roce_calculated_pct"])

    npm_score = normalize_score(df["net_profit_margin_pct"])


    # Cash Quality (30%)

    fcf_conversion_score = normalize_score(df["fcf_conversion"])

    cfo_quality_score = normalize_score(df["cfo_quality"])

    fcf_positive_score = positive_flag(df["free_cash_flow"])


    # Growth (20%)

    sales_growth_score = normalize_score(df["sales_cagr_5yr"])

    profit_growth_score = normalize_score(df["profit_cagr_5yr"])


    # Leverage (15%)

    debt_score = normalize_score(
        df["debt_to_equity"],
        reverse=True
    )

    interest_score = normalize_score(
        df["interest_coverage"]
    )


    df["composite_quality_score"] = (

        roe_score * 0.15 +

        roce_score * 0.10 +

        npm_score * 0.10 +

        fcf_conversion_score * 0.15 +

        cfo_quality_score * 0.10 +

        fcf_positive_score * 0.05 +

        sales_growth_score * 0.10 +

        profit_growth_score * 0.10 +

        debt_score * 0.10 +

        interest_score * 0.05

    )

    return df