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


# ==========================
# DEBT TO EQUITY
# ==========================

def calculate_debt_to_equity(
    borrowings,
    equity_capital,
    reserves
):

    if borrowings == 0:
        return 0

    total_equity = (
        equity_capital + reserves
    )

    if total_equity <= 0:
        return None

    return round(
        borrowings / total_equity,2
        
    )
    
    
    # ==========================
# HIGH LEVERAGE FLAG
# ==========================

def high_leverage_flag(
    debt_to_equity,
    broad_sector
):

    if debt_to_equity is None:
        return False

    if str(broad_sector).lower() == "financials":
        return False

    return debt_to_equity > 5


# ==========================
# INTEREST COVERAGE RATIO
# ==========================

def calculate_interest_coverage(
    operating_profit,
    other_income,
    interest
):

    if interest == 0:
        return None

    return round(

        (operating_profit + other_income) / interest,2

    )
    
    
    # ==========================
# ICR LABEL
# ==========================

def get_icr_label(interest):

    if interest == 0:
        return "Debt Free"

    return "Has Debt"


# ==========================
# NET DEBT
# ==========================

def calculate_net_debt(
    borrowings,
    investments
):

    return borrowings - investments


# ==========================
# ASSET TURNOVER
# ==========================

def calculate_asset_turnover(
    sales,
    total_assets
):

    if total_assets <= 0:
        return None

    return round(
        sales / total_assets,
        2
    )