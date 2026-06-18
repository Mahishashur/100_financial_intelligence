import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(ROOT)
)

from src.etl.normaliser import (
    normalize_year,
    normalize_ticker
)


def test_year():

    assert normalize_year(
        "2024"
    ) == 2024


def test_ticker():

    assert normalize_ticker(
        " tcs "
    ) == "TCS"