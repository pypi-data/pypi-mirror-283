from flask import request

from flavours import FlavourHandler
from flavours.utils import set_response_json

class ApplogicHandler(FlavourHandler):
    def construct_function_parameters():
        return (request,)

    def return_error_response(error):
        set_response_json(500, { 'error': error })