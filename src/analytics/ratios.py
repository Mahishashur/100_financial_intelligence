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

# Debt to equity

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
    
# High leverage flag

def high_leverage_flag(
    debt_to_equity,
    broad_sector
):

    if debt_to_equity is None:
        return False

    if str(broad_sector).lower() == "financials":
        return False

    return debt_to_equity > 5


# Interest coverage ratio

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
    
    # ICR label


def get_icr_label(interest):

    if interest == 0:
        return "Debt Free"

    return "Has Debt"

# NET debt

def calculate_net_debt(
    borrowings,
    investments
):

    return borrowings - investments

# Asset turnover

def calculate_asset_turnover(
    sales,
    total_assets
):

    if total_assets <= 0:
        return None

    return round(sales / total_assets,2)
    
# Free case flow

def calculate_free_cash_flow(

    operating_activity,

    investing_activity

):

    return operating_activity + investing_activity


def calculate_cfo_quality(
    operating_activity,
    net_profit ):

    if net_profit == 0:
        return None

    return round(
        operating_activity / net_profit,2
    )
    
    
def calculate_fcf_conversion(
    free_cash_flow,
    net_profit
):

    if net_profit <= 0:
        return None

    return round(
        free_cash_flow / net_profit,2
    )
    

def calculate_capex_intensity(
    operating_activity,
    investing_activity):

    if operating_activity <= 0:
        return None

    return round(
        abs(investing_activity) / operating_activity,2
    )
    
    
def calculate_ocf_margin(
    operating_activity,
    sales
):

    if sales <= 0:
        return None

    return round(
        (operating_activity / sales) * 100,2
    )
    
    
def calculate_cash_conversion_ratio(
    operating_activity,
    operating_profit
):

    if operating_profit <= 0:
        return None

    return round(
        operating_activity / operating_profit,2
    )
    
    
def calculate_cash_reinvestment_ratio(
    operating_activity,
    fixed_assets):

    if fixed_assets <= 0:
        return None

    return round(
        operating_activity / fixed_assets,2
    )
    
    
def calculate_cash_reinvestment_ratio(
    operating_activity,
    fixed_assets
):

    if fixed_assets <= 0:
        return None

    return round(
        operating_activity / fixed_assets,2
    )
    
    
def calculate_retention_ratio(
    dividend_payout):

    if dividend_payout is None:
        return None

    return round(
        1 - (dividend_payout / 100),2
    )
    
    
def calculate_retention_ratio(
    dividend_payout):

    if dividend_payout is None:
        return None

    if dividend_payout < 0:
        return None

    return round(
        1 - (dividend_payout / 100),2
    )
    
    
def calculate_financial_leverage(
    total_assets,
    equity_capital,
    reserves):

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(total_assets / equity, 2)


def calculate_debt_ratio(
    borrowings,
    total_assets):

    if total_assets <= 0:
        return None

    return round(
        borrowings / total_assets,2
    )
    

def calculate_capital_employed_turnover(
    sales,
    equity_capital,
    reserves,
    borrowings):

    capital_employed = equity_capital + reserves + borrowings

    if capital_employed <= 0:
        return None

    return round(
        sales / capital_employed,2
    )
    
    
def calculate_net_asset_turnover(
    sales,
    total_assets,
    investments
):

    net_assets = total_assets - investments

    if net_assets <= 0:
        return None

    return round(
        sales / net_assets,2
    )
    
    
def calculate_investment_ratio(
    investments,
    total_assets):

    if total_assets <= 0:
        return None

    return round(
        investments / total_assets,2
    )
    
    
def calculate_fixed_asset_ratio(
    fixed_assets,
    total_assets
):

    if total_assets <= 0:
        return None

    return round(
        fixed_assets / total_assets,2
    )
   
   
def calculate_reserve_to_equity_ratio(
    reserves,
    equity_capital):

    if equity_capital <= 0:
        return None

    return round(
        reserves / equity_capital,2
    ) 