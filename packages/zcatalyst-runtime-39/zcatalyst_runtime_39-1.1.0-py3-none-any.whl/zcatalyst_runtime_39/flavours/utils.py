import json
import os

from flask import g, request

def get_catalyst_headers(headers: dict = {}) -> dict:
    catalyst_headers = {}
    for header in headers.keys():
        header_lower: str = header.lower()
        if header_lower.startswith('x-zc-'):
            catalyst_headers[header] = headers.get(header)

    return catalyst_headers

def get_request_json() -> dict:
    request_body = request.get_data()
    return json.loads(request_body) if request_body else {}

def set_response_json(status_code: int, message: dict = None):
    g.response.status_code = status_code

    if message:
        g.response.content_type = 'application/json; charset=utf-8'
        g.response.mimetype = 'application/json'

        message_str = json.dumps(message)
        g.response.set_data(message_str)

def get_env_strict(key: str) -> str:
    value = os.getenv(key)
    if value:
        return value
    else:
        raise Exception(f'environment variable not found: {key}')
