"""
Test JSON functions.
"""
import sys
import pytest

from datetime import date, datetime

import simplejson as json

from bh_utils import json_funcs

EMPLOYEES = [
    {'emp_no': 12483, 'birth_date': datetime(1959, 10, 19), 'first_name': 'Niranjan', \
        'last_name': 'Gornas', 'gender': 'M', 'hire_date': datetime(1990, 1, 10)}, 
    {'emp_no': 18671, 'birth_date': date(1955, 12, 12), 'first_name': 'Shan', \
        'last_name': 'Nastansky', 'gender': 'M', 'hire_date': date(1986, 5, 4)}
]

@pytest.mark.json_funcs
def test_serialise():
    data = json.loads(json.dumps(EMPLOYEES, use_decimal=True, default=json_funcs.serialise, indent="  "))

    assert data[0]['birth_date'] == '19/10/1959'
    assert data[0]['hire_date'] == '10/01/1990'
    assert data[1]['birth_date'] == '12/12/1955'
    assert data[1]['hire_date'] == '04/05/1986'

@pytest.mark.json_funcs
def test_json_dumps():
    data = json_funcs.dumps(EMPLOYEES)

    assert '"emp_no": 12483' in data
    assert '"birth_date": "19/10/1959"' in data
    assert '"hire_date": "10/01/1990"' in data
    assert '"emp_no": 18671' in data
    assert '"birth_date": "12/12/1955"' in data
    assert '"hire_date": "04/05/1986"' in data