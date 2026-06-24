def normalize_year(year):
    return int(str(year)[:4])


def normalize_ticker(ticker):
    return (str(ticker).strip().upper().replace(".NS","" ))