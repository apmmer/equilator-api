from typing import Any, List


def convert_to_boolean(value: Any) -> bool:
    """
    Takes any boolable value and converts it to boolean.
    This function will be helpful if somebody tries to pass
    '0' as False in environment.
    """

    if value in [None, False, 'False', 'false', '0',
                 0, 'None', 'nan', 'none', '']:
        return False
    return bool(value)


def split_cors_middleware(value: str, sep: str) -> List:
    """
    Custom splitter, which also includes separator with space.
    """

    if f'{sep} ' in value:
        sep = f'{sep} '
    if value and isinstance(value, str) and sep != value:
        res = value.split(sep)
    else:
        res = []
    return res
