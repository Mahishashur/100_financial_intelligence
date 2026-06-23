from pathlib import Path
import pandas as pd


DATA=Path("data/processed")

def validate():
    files=list(DATA.glob("*.csv")
)

    report=[]

    for f in files:

        df=pd.read_csv(f)

        report.append({

"file":f.name,

"rows":len(df),

"duplicates":df.duplicated().sum(),

"missing":df.isnull().sum().sum(),

"missing_pct":round(df.isnull().mean().mean()*100,2)})

    out=pd.DataFrame(report)

    out.to_csv("output/validation_failures.csv",index=False)
    print(out)


if __name__=="__main__":

    validate()