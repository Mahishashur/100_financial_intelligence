from src.analytics.ratios import (
    calculate_npm,
    calculate_opm,
    calculate_roe,
    calculate_roce,
    calculate_roa,
    calculate_debt_to_equity,
    calculate_interest_coverage,
    calculate_free_cash_flow,
    calculate_net_debt,
    calculate_asset_turnover,
    calculate_free_cash_flow,
    calculate_cfo_quality,
    calculate_fcf_conversion,
    calculate_capex_intensity,
    calculate_ocf_margin,
    calculate_cash_conversion_ratio,
    calculate_cash_reinvestment_ratio,
    calculate_cash_reinvestment_ratio,
    calculate_retention_ratio,
    calculate_retention_ratio,
    calculate_financial_leverage,
    calculate_debt_ratio,
    calculate_capital_employed_turnover,
    calculate_net_asset_turnover,
    calculate_investment_ratio,
    calculate_fixed_asset_ratio,
    calculate_reserve_to_equity_ratio
)


def test_npm():

    assert calculate_npm(1000,100) == 10


def test_opm():

    assert calculate_opm(1000,200) == 20


def test_roe():

    assert calculate_roe(100,200,300) == 20


def test_roce():

    assert calculate_roce(250,100,400,500) == 25


def test_roa():

    assert calculate_roa(120,1000) == 12
    
    
import pytest

from src.analytics.ratios import (
    calculate_npm,
    calculate_opm,
    calculate_roe,
    calculate_roce,
    calculate_roa
)

# NPM

def test_npm():
    assert calculate_npm(1000, 100) == 10


def test_npm_zero_sales():
    assert calculate_npm(0, 100) is None

# OPM

def test_opm():
    assert calculate_opm(1000, 200) == 20


def test_opm_zero_sales():
    assert calculate_opm(0, 200) is None

# ROE

def test_roe():
    assert calculate_roe(100, 200, 300) == 20


def test_roe_negative_equity():
    assert calculate_roe(100, -200, 100) is None

# ROCE

def test_roce():
    assert calculate_roce(250, 100, 400, 500) == 25


def test_roce_zero_capital():
    assert calculate_roce(250, 0, 0, 0) is None

# ROA

def test_roa():
    assert calculate_roa(120, 1000) == 12


def test_roa_zero_assets():
    assert calculate_roa(120, 0) is None
    
    
def test_npm_zero_sales():
    assert calculate_npm(0, 100) is None


def test_opm_zero_sales():
    assert calculate_opm(0, 100) is None


def test_roe_negative_equity():
    assert calculate_roe(100, -200, 100) is None


def test_roce_zero_capital():
    assert calculate_roce(250, 0, 0, 0) is None


def test_roa_zero_assets():
    assert calculate_roa(100, 0) is None
    
    
# Debt to equity

def test_debt_to_equity():

    assert calculate_debt_to_equity(500,100,400) == 1


def test_debt_free():

    assert calculate_debt_to_equity(0,100,400) == 0


# Interest coverage

def test_interest_coverage():

    assert calculate_interest_coverage(500,100,100) == 6


def test_interest_zero():

    assert calculate_interest_coverage(500,100,0) is None


# Net debt

def test_net_debt():

    assert calculate_net_debt(1000,200) == 800

# Asset turnover

def test_asset_turnover():
    assert calculate_asset_turnover(2000,1000) == 2


def test_asset_turnover_zero_assets():

    assert calculate_asset_turnover(2000,0) is None
    
    
def test_free_cash_flow():

    assert calculate_free_cash_flow(500,-200) == 300
    
    calculate_cfo_quality
    
def test_cfo_quality_zero_profit():

    assert calculate_cfo_quality(100,0) is None
    
    
def test_fcf_conversion():

    assert calculate_fcf_conversion(
        200,100) == 2


def test_fcf_conversion_zero_profit():

    assert calculate_fcf_conversion(100,0) is None
    
def test_fcf_conversion_negative_profit():

    assert calculate_fcf_conversion(100,-10) is None
    
    
def test_capex_intensity():

    assert calculate_capex_intensity(1000,-400) == 0.40

def test_capex_intensity_zero_operating():

    assert calculate_capex_intensity(0,-200) is None


def test_capex_intensity_negative_operating():

    assert calculate_capex_intensity(-100,-50) is None


def test_ocf_margin():

    assert calculate_ocf_margin(200,1000) == 20


def test_ocf_margin_zero_sales():

    assert calculate_ocf_margin(100,0) is None


def test_ocf_margin_negative_sales():

    assert calculate_ocf_margin(100,-100) is None
    
    
def test_cash_conversion_ratio():

    assert calculate_cash_conversion_ratio(200,100) == 2


def test_cash_conversion_ratio_zero_profit():

    assert calculate_cash_conversion_ratio(100,0) is None


def test_cash_conversion_ratio_negative_profit():

    assert calculate_cash_conversion_ratio(100,-50) is None

    
def test_cash_reinvestment_ratio():

    assert calculate_cash_reinvestment_ratio(500,250) == 2


def test_cash_reinvestment_zero_assets():

    assert calculate_cash_reinvestment_ratio(100,0) is None


def test_cash_reinvestment_negative_assets():

    assert calculate_cash_reinvestment_ratio(100,-10 ) is None
    
    
def test_cash_reinvestment_ratio():

    assert calculate_cash_reinvestment_ratio(500,250) == 2


def test_cash_reinvestment_zero_assets():

    assert calculate_cash_reinvestment_ratio(100,0) is None


def test_cash_reinvestment_negative_assets():

    assert calculate_cash_reinvestment_ratio(100,-20) is None
    
    
def test_retention_ratio():

    assert calculate_retention_ratio(20) == 0.80


def test_retention_ratio_zero():

    assert calculate_retention_ratio(0) == 1.00


def test_retention_ratio_full():

    assert calculate_retention_ratio(100) == 0.00
    
    
def test_retention_ratio():

    assert calculate_retention_ratio(20) == 0.80


def test_retention_ratio_zero():

    assert calculate_retention_ratio(0) == 1.00


def test_retention_ratio_full():

    assert calculate_retention_ratio(100) == 0.00


def test_retention_ratio_negative():

    assert calculate_retention_ratio(-10) is None
    

def test_financial_leverage():

    assert calculate_financial_leverage(1000,200,300) == 2.00


def test_financial_leverage_zero_equity():

    assert calculate_financial_leverage(1000,0,0) is None


def test_financial_leverage_negative_equity():

    assert calculate_financial_leverage(1000,-100,50) is None
    
    
def test_debt_ratio():

    assert calculate_debt_ratio(500,1000) == 0.50


def test_debt_ratio_zero_assets():

    assert calculate_debt_ratio(500,0) is None


def test_debt_ratio_negative_assets():

    assert calculate_debt_ratio(500,-100) is None
    
    
def test_capital_employed_turnover():

    assert calculate_capital_employed_turnover(1000,200,300,500) == 1.00


def test_capital_employed_turnover_zero():

    assert calculate_capital_employed_turnover(1000,0,0,0) is None


def test_capital_employed_turnover_negative():

    assert calculate_capital_employed_turnover(1000,-100,50,0) is None
    

def test_net_asset_turnover():

    assert calculate_net_asset_turnover(1000,800,300) == 2.00


def test_net_asset_turnover_zero_assets():

    assert calculate_net_asset_turnover(1000,500,500) is None


def test_net_asset_turnover_negative_assets():

    assert calculate_net_asset_turnover(1000,400,500) is None
    
    
def test_investment_ratio():

    assert calculate_investment_ratio(200,1000) == 0.20


def test_investment_ratio_zero_assets():

    assert calculate_investment_ratio(200,0) is None


def test_investment_ratio_negative_assets():

    assert calculate_investment_ratio(200,-100) is None
    
    
def test_fixed_asset_ratio():

    assert calculate_fixed_asset_ratio(500,1000) == 0.50


def test_fixed_asset_ratio_zero_assets():

    assert calculate_fixed_asset_ratio(500,0) is None


def test_fixed_asset_ratio_negative_assets():

    assert calculate_fixed_asset_ratio(500,-100) is None
    
    
def test_reserve_to_equity_ratio():

    assert calculate_reserve_to_equity_ratio(500,100) == 5.00


def test_reserve_to_equity_ratio_zero_equity():

    assert calculate_reserve_to_equity_ratio(500,0) is None


def test_reserve_to_equity_ratio_negative_equity():

    assert calculate_reserve_to_equity_ratio(500,-100) is None