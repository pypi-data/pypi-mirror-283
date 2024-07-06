"""
Test string functions.
"""
import pytest

from bh_utils.str_funcs import (
    extract_session_cookie,
    camel_case,
)

@pytest.mark.str_funcs
def test_extract_session_cookie_01():
    str = "csrftoken=7c4Dfm5zLcCKs5lEHsOwgacPCfoVVLg6lgA4kWpYbbinWzBx6B8iRi4YaESzSEyl; session=6bdb90a8-38b0-4251-9d1c-08a183fc9306.nXsyZ6p1OptV7S3xsBWT4bkJcQs"
    assert extract_session_cookie(str) == "6bdb90a8-38b0-4251-9d1c-08a183fc9306.nXsyZ6p1OptV7S3xsBWT4bkJcQs"

    str = "session=84f32fae-3d44-477b-a0ea-bdba5d540ceb.92b5eohdHU6-9F1uQcci_luSWsc"
    assert extract_session_cookie(str) == "84f32fae-3d44-477b-a0ea-bdba5d540ceb.92b5eohdHU6-9F1uQcci_luSWsc"

@pytest.mark.str_funcs
def test_extract_session_cookie_02():
    str = "session="
    assert extract_session_cookie(str) == ""

    str = "csrftoken=7c4Dfm5zLcCKs5lEHsOwgacPCfoVVLg6lgA4kWpYbbinWzBx6B8iRi4YaESzSEyl"
    assert extract_session_cookie(str) == "--- No Cookie ---"

@pytest.mark.str_funcs
def test_extract_session_cookie_03():
    str = "csrftoken=7c4Dfm5zLcCKs5lEHsOwgacPCfoVVLg6lgA4kWpYbbinWzBx6B8iRi4YaESzSEyl;session=6bdb90a8-38b0-4251-9d1c-08a183fc9306.nXsyZ6p1OptV7S3xsBWT4bkJcQs"
    assert extract_session_cookie(str) == "6bdb90a8-38b0-4251-9d1c-08a183fc9306.nXsyZ6p1OptV7S3xsBWT4bkJcQs"

@pytest.mark.str_funcs
def test_camel_case():
    str = camel_case('project-id')
    assert str == 'projectId'

    str = camel_case('project id')
    assert str == 'projectId'

    str = camel_case('name')
    assert str == 'name'
