"""
Specific module settings are located here.
"""

from os import getenv


class AuthSettings:
    api_key: str = getenv("API_KEY", "secret")
