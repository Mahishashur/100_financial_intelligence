from src.etl.normaliser import *



def test_year():

    assert normalize_year(
"2024"
)==2024



def test_ticker():

    assert normalize_ticker(
"tcs.ns"
)=="TCS"