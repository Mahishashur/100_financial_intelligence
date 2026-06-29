from src.analytics.ratios import (
    calculate_npm,
    calculate_opm,
    calculate_roe,
    calculate_roce,
    calculate_roa
)


def test_npm():

    assert calculate_npm(
        1000,
        100
    ) == 10


def test_opm():

    assert calculate_opm(
        1000,
        200
    ) == 20


def test_roe():

    assert calculate_roe(
        100,
        200,
        300
    ) == 20


def test_roce():

    assert calculate_roce(
        250,
        100,
        400,
        500
    ) == 25


def test_roa():

    assert calculate_roa(
        120,
        1000
    ) == 12
    
    
import pytest

from src.analytics.ratios import (
    calculate_npm,
    calculate_opm,
    calculate_roe,
    calculate_roce,
    calculate_roa
)


# ----------------------------
# NPM
# ----------------------------

def test_npm():
    assert calculate_npm(1000, 100) == 10


def test_npm_zero_sales():
    assert calculate_npm(0, 100) is None


# ----------------------------
# OPM
# ----------------------------

def test_opm():
    assert calculate_opm(1000, 200) == 20


def test_opm_zero_sales():
    assert calculate_opm(0, 200) is None


# ----------------------------
# ROE
# ----------------------------

def test_roe():
    assert calculate_roe(100, 200, 300) == 20


def test_roe_negative_equity():
    assert calculate_roe(100, -200, 100) is None


# ----------------------------
# ROCE
# ----------------------------

def test_roce():
    assert calculate_roce(250, 100, 400, 500) == 25


def test_roce_zero_capital():
    assert calculate_roce(250, 0, 0, 0) is None


# ----------------------------
# ROA
# ----------------------------

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