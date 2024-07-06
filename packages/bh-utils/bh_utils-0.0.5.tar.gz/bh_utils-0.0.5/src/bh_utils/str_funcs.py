"""
Some string routines.

For usage examples, see ``./tests/test_str_funcs.py``.
"""

from re import sub

def extract_session_cookie(cookie: str) -> str:
    """
    From a string which might have multiple ``name=value`` pair strings, get the value 
    for ``session`` name.

    ``name=value`` pair strings are separated by semicolon (``;``). For example:

    - csrftoken=7c4Df...zSEyl; session=6bdb9...kJcQs
    - session=84f32...uSWsc

    :param str cookie: a which contains multiple ``name=value`` pair strings.

    :return: value for ``session`` if found, otherwise ``--- No Cookie ---``.
    :rtype: str.
    """
    
    items = cookie.split(';')
    for itm in items:
        itm_cleaned = itm.strip()
        if ("session=" in itm_cleaned): return itm_cleaned[8:]
    return '--- No Cookie ---'

def camel_case(s: str) -> str:
    """Convert a string to camelCase.

    Source: https://www.w3resource.com/python-exercises/string/python-data-type-string-exercise-96.php
	
    Example::
	
    ``project-id`` converted to ``projectId``.	
    ``name`` to ``name``.

    :param str s: source string to be converted.

    :return: camelCase representation of source string.
    :rtype: str.
    """

    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([s[0].lower(), s[1:]])
