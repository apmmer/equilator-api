from typing import Any


def split_value(value: str, separator: str = ',') -> list:
    if value and isinstance(value, str) and separator != value:
        return value.split(separator)
    return []


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


def split_cors_middleware(value: str, sep: str):
    """
        Custom splitter, which also includes separator with space.
    """

    if f'{sep} ' in value:
        sep = f'{sep} '
    return split_value(value, separator=sep)
