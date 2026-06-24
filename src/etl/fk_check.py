import sqlite3


conn = sqlite3.connect(
    "nifty100.db"
)


cur = conn.cursor()


cur.execute(
    "PRAGMA foreign_key_check"
)


rows = cur.fetchall()


if len(rows)==0:

    print(
        "FK CHECK PASSED"
    )

else:

    print(
        rows
    )


conn.close()