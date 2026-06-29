# Net_profit_margin

def calculate_npm(sales, net_profit):

    if sales <= 0:
        return None
    return round((net_profit / sales) * 100,2)

# Operating_profit_margin

def calculate_opm(sales, operating_profit):

    if sales <= 0:
        return None
    return round((operating_profit / sales) * 100,2)

# Return_on_equity

def calculate_roe(net_profit,equity_capital,reserves):

    total_equity = equity_capital + reserves
    if total_equity <= 0:
        return None
    return round((net_profit / total_equity) * 100,2)

# Return_on_capital_employed

def calculate_roce(
    operating_profit,
    equity_capital,
    reserves,
    borrowings
):

    capital = (equity_capital + reserves + borrowings)
    if capital <= 0:
        return None
    return round((operating_profit / capital) * 100,2 )

# Return_on_assests

def calculate_roa(net_profit,total_assets):

    if total_assets <= 0:
        return None
    return round((net_profit / total_assets) * 100,2)