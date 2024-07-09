from flask import g

from flavours import FlavourHandler
from flavours.utils import get_request_json, set_response_json

class IntegrationRequest:
    def __init__(self) -> None:
        pass

    def get_request_body(self) -> dict:
        return get_request_json()

class IntegrationResponse:
    def __init__(self) -> None:
        self.__status_code = 200
        self.__content_type = 'text/plain'

    def set_status(self, status_code: int) -> None:
        self.__status_code = status_code

    def set_content_type(self, content_type: str) -> None:
        self.__content_type = content_type

    def send(self, message: str = None) -> None:
        g.response.status_code = self.__status_code

        if message:
            g.response.content_type = self.__content_type
            g.response.set_data(message)


class IntegrationHandler(FlavourHandler):
    def construct_function_parameters():
        return (IntegrationRequest(), IntegrationResponse())

    def return_error_response(error):
        set_response_json(532, { 'error': error })