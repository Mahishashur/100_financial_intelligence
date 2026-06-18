PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS companies (

company_id INTEGER PRIMARY KEY,

ticker TEXT NOT NULL,

company_name TEXT NOT NULL,

sector TEXT

);

CREATE TABLE IF NOT EXISTS profitandloss (

id INTEGER PRIMARY KEY AUTOINCREMENT,

company_id INTEGER,

year INTEGER,

sales REAL,

profit REAL,

FOREIGN KEY (
company_id
)

REFERENCES companies(
company_id
)

);