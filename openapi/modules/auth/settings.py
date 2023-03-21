from os import getenv


class AuthSettings:
    router_prefix: str = '/auth'
    api_key: str = getenv('API_KEY', 'secret')
