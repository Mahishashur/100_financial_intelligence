import pandas as pd
import yaml


class ScreenerEngine:

    def __init__(self, csv_path, config_path):

        self.df = pd.read_csv(csv_path)
        # Remove TTM rows
        self.df = self.df[
            self.df["year"] != "TTM"
        ]
        self.df = (self.df
            .sort_values(["company_id", "year"])
            .groupby("company_id")
            .tail(1)
            .reset_index(drop=True)
        )

        # Keep latest record of each company
        self.df = (self.df
            .sort_values(["company_id", "year"])
            .groupby("company_id")
            .tail(1)
            .reset_index(drop=True)
        )

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def get_preset(self, preset_name):

        return self.config[preset_name]

    def apply_filters(self, preset_name):

        preset = self.get_preset(preset_name)

        filtered_df = self.df.copy()

        print("Initial:", len(filtered_df))

        if "roe_min" in preset:

            filtered_df = filtered_df[
                filtered_df["roe_calculated_pct"] >= preset["roe_min"]
            ]

            print("After ROE:", len(filtered_df))
            
        if "profit_cagr_5yr_min" in preset:

            filtered_df = filtered_df[
                filtered_df["profit_cagr_5yr"] >= preset["profit_cagr_5yr_min"]
            ]

            print("After Profit CAGR:", len(filtered_df))

        if "sales_min" in preset:

            filtered_df = filtered_df[
                filtered_df["sales"] >= preset["sales_min"]
            ]

            print("After Sales:", len(filtered_df))
            
        if "dividend_payout_max" in preset:

            filtered_df = filtered_df[
                filtered_df["dividend_payout"] <= preset["dividend_payout_max"]
            ]

        print("After Dividend Payout:", len(filtered_df))

        if "debt_to_equity_max" in preset:

            filtered_df = filtered_df[
                filtered_df["debt_to_equity"] <= preset["debt_to_equity_max"]
            ]

            print("After D/E:", len(filtered_df))

        if "free_cash_flow_min" in preset:

            filtered_df = filtered_df[
                filtered_df["free_cash_flow"] >= preset["free_cash_flow_min"]
            ]

            print("After FCF:", len(filtered_df))

        if "sales_cagr_5yr_min" in preset:

            filtered_df = filtered_df[
                filtered_df["sales_cagr_5yr"] >= preset["sales_cagr_5yr_min"]
            ]

            print("After Sales CAGR:", len(filtered_df))

        return filtered_df


if __name__ == "__main__":

    engine = ScreenerEngine(
        "data/output/financial_kpis.csv",
        "config/screener_config.yaml"
    )

    print("Total Companies:", len(engine.df))
    
    print("\nTop 20 Companies by ROE")

    print(
        engine.df[
            [
                "company_id",
                "year",
                "roe_calculated_pct"
            ]
        ].sort_values("roe_calculated_pct",ascending=False).head(20)
    )

    result = engine.apply_filters("quality_compounder")


presets = [

    "quality_compounder",

    "value_pick",

    "growth_accelerator",

    "dividend_champion",

    "debt_free_blue_chip",

    "turnaround_watch"

]

for preset in presets:

    print("=" * 60)

    print("Preset :", preset)

    result = engine.apply_filters(preset)

    print("Companies :", len(result))

    print(
        result[
            [
                "company_id",
                "year"
            ]
        ].head(10)
    )
    
print("\nColumns Available:\n")

print(engine.df.columns.tolist())
