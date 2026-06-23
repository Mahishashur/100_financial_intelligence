from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")

OUT.mkdir(exist_ok=True)


def clean_columns(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


def process_folder():

    files = list(RAW.glob("**/*.xlsx")
    )

    for f in files:

        print(f"Loading {f.name}")

        df = pd.read_excel(f)

        df = clean_columns(df)

        save = (OUT /f"{f.stem}_clean.csv"
        )

        df.to_csv(save,index=False)

        print(f"Saved  {save}")


if __name__=="__main__":
    process_folder()