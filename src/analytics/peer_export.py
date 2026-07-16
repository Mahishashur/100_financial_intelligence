import sqlite3
import pandas as pd


def save_peer_sqlite(peer_df):

    conn = sqlite3.connect(
        "data/output/financial.db"
    )

    peer_df.to_sql(

        "peer_percentiles",

        conn,

        if_exists="replace",

        index=False

    )

    conn.close()

    print("\n✓ peer_percentiles table created successfully.")



def export_peer_excel(peer_df):

    with pd.ExcelWriter(

        "output/peer_comparison.xlsx",

        engine="openpyxl"

    ) as writer:

        for group in sorted(

            peer_df["peer_group_name"]

            .dropna()

            .unique()

        ):

            sheet = peer_df[

                peer_df["peer_group_name"] == group

            ]

            sheet.to_excel(

                writer,

                sheet_name=group[:31],

                index=False

            )

    print("\n✓ peer_comparison.xlsx created successfully.")