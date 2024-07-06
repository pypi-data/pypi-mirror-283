"""
Test date functions.
"""
import pytest

from bh_utils.date_funcs import (
    australian_date_to_iso_datetime,
)

@pytest.mark.date_funcs
def test_australian_date_to_iso_datetime_01():
    d1, d2 = australian_date_to_iso_datetime({'startDate': '29/1/2022', \
        'endDate': '1/12/2022'}, False)

    assert isinstance(d1, str) == True
    assert isinstance(d2, str) == True

    assert d1 == '2022-01-29'
    assert d2 == '2022-12-01'

@pytest.mark.date_funcs
def test_australian_date_to_iso_datetime_02():
    date_str = australian_date_to_iso_datetime('29/1/2022', False)
    assert date_str == '2022-01-29'

@pytest.mark.date_funcs
def test_australian_date_to_iso_datetime_03():
    d1, d2 = australian_date_to_iso_datetime({'startDate': '29/1/2022 2:15:03 PM', \
        'endDate': '1/12/2022 10:15:00 AM'})

    assert d1 == "2022-01-29T14:15:03"
    assert d2 == "2022-12-01T10:15:00"

@pytest.mark.date_funcs
def test_australian_date_to_iso_datetime_04():
    date_str = australian_date_to_iso_datetime('29/1/2022 2:00:00 AM', True)
    assert date_str == '2022-01-29T02:00:00'
