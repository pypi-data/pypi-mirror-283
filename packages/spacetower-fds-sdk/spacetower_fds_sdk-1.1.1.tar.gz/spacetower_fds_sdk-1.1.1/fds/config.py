import os


class Config:
    api_key = os.getenv('FDS_API_KEY', '')
    client_id: str = os.getenv('FDS_API_CLIENT_ID', '')
    client_secret = os.getenv('FDS_API_CLIENT_SECRET', '')
    api_url = os.getenv('FDS_API_URL', "https://api.spacetower.exotrail.space/fds/v1")
    proxy = os.getenv('HTTP_PROXY')
    instrumentation = os.getenv('INSTRUMENTATION', 'True') == 'True'


def get_proxy():
    return Config.proxy


def set_api_key(token: str):
    Config.api_key = token


def get_api_key():
    return Config.api_key


def set_url(url: str):
    Config.api_url = url


def get_api_url():
    return Config.api_url


def set_client_id(client_id: str):
    Config.client_id = client_id


def get_client_id():
    return Config.client_id


def set_client_secret(client_secret: str):
    Config.client_secret = client_secret


def get_client_secret():
    return Config.client_secret
