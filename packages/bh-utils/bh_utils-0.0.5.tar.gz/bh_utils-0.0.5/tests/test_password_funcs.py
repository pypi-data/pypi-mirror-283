"""
Test password functions.
"""
import pytest

from bh_utils.password_funcs import (
    generate_password
)

@pytest.mark.password_funcs
def test_generate_password():
    print("\n")

    pwd = generate_password(5, 10)
    assert len(pwd) >= 5
    assert len(pwd) <= 10    
    print(pwd)

    pwd = generate_password(12, 20)
    assert len(pwd) >= 12
    assert len(pwd) <= 20
    print(pwd)
