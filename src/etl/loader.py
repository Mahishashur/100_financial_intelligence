from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")

OUT.mkdir(exist_ok=True)


def clean_columns(df):

     df.columns = (

        df.columns

        .astype(str)

        .str.strip()

        .str.lower()

        .str.replace(" ","_")

        .str.replace("-","_")

    )

     df = df.loc[:, ~df.columns.str.contains("unnamed")]

     return df


def process_folder():

    files = list(RAW.glob("**/*.xlsx")
    )

    for f in files:

        print(f"Loading {f.name}")

        if "stock_prices" in f.name:

         df = pd.read_excel(f,header=0
    )

        else:

            df = pd.read_excel(f,header=1
    )

        df = clean_columns(df)

        save = (OUT /f"{f.stem}_clean.csv"
        )

        df.to_csv(save,index=False)

        print(f"Saved  {save}")


if __name__=="__main__":
    process_folder()