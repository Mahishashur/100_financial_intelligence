SELECT COUNT(*) FROM companies;

SELECT COUNT(*) FROM balancesheet;

SELECT COUNT(*) FROM cashflow;

SELECT COUNT(*) FROM profitandloss;

SELECT COUNT(*) FROM stock_prices;

SELECT sector,
COUNT(*)

FROM sectors

GROUP BY sector;

SELECT *

FROM companies

LIMIT 10;

SELECT *

FROM stock_prices

LIMIT 10;

SELECT AVG(close)

FROM stock_prices;

SELECT COUNT(*)

FROM documents;