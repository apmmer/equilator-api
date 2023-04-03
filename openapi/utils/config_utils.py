"""
Module for utils 
(functions which are not related to code,
they can only use the built-in library)
"""
from typing import Any


def convert_to_boolean(value: Any) -> bool:
    """
    Takes any boolable value and converts it to boolean.
    This function wil lbe helpful if somebody tries to pass
    '0' as False in environment.
    """

    if value in [None, False, 'False', 'false', '0',
                 0, 'None', 'nan', 'none', '']:
        return False
    return bool(value)
