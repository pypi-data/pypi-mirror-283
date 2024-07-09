import os
import json
import threading
from importlib.util import spec_from_file_location, module_from_spec

from flask import g, request

from init_handler import InitHandler
from flavours.utils import get_catalyst_headers, set_response_json

CUSTOMER_CODE_ENTRYPOINT = None

class FlavourHandler:
    def __init__(self) -> None:
        with open(InitHandler.get_code_location().joinpath('catalyst-config.json'), 'r') as config_file:
            catalyst_config = json.loads(config_file.read())
            entry_point = catalyst_config['execution']['main'] or 'main.py'
            self.__entrypoint = InitHandler.get_code_location().joinpath(entry_point)
            self.__flavour = os.getenv('CATALYST_FUNCTION_TYPE', catalyst_config['deployment']['type'])

    def __get_flavour(self):
        if self.__flavour == 'basicio':
            from flavours.basicio import BasicIOHandler
            return BasicIOHandler
        elif self.__flavour == 'applogic' or self.__flavour == 'advancedio':
            from flavours.applogic import ApplogicHandler
            return ApplogicHandler
        elif self.__flavour == 'cron':
            from flavours.cron import CronHandler
            return CronHandler
        elif self.__flavour == 'event':
            from flavours.event import EventHandler
            return EventHandler
        elif self.__flavour == 'integration':
            from flavours.integration import IntegrationHandler
            return IntegrationHandler
        elif self.__flavour == 'job':
            from flavours.job import JobHandler
            return JobHandler
        else:
            raise Exception(f'unsupported function type: {self.__flavour}')
        
    def invoke_handler(self):
        global CUSTOMER_CODE_ENTRYPOINT
        if not CUSTOMER_CODE_ENTRYPOINT:
            spec = spec_from_file_location('', self.__entrypoint)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            CUSTOMER_CODE_ENTRYPOINT = module.handler

        if self.__flavour == 'job':
            # Note:
            # Job functions runs as a standalone python program and doesn't have Flask's 
            # request object set. So, we're getting the catalyst headers from the job
            # meta details using `get_job_meta_details()`.

            (JOB_DETAILS, CONTEXT) = self.__get_flavour().construct_function_parameters()
            threading.current_thread().__setattr__('__zc_local', { 'catalyst_headers': get_catalyst_headers(JOB_DETAILS.get_job_meta_details()['headers']) })
            
            CUSTOMER_CODE_ENTRYPOINT(*(JOB_DETAILS, CONTEXT))

            # Note:
            #
            # Job functions should call either `close_with_success` or `close_with_failure`
            # to set execution status and exit from the function. If the control reaches
            # here means neither of them is called, so we're setting status to 531 (which 
            # means 'unintentional termination').
            from flavours.job_utils import post_job_status
            post_job_status(531)
        else:
            threading.current_thread().__setattr__('__zc_local', { 'catalyst_headers': get_catalyst_headers(request.headers) })
            RET_VAL = CUSTOMER_CODE_ENTRYPOINT(*(self.__get_flavour().construct_function_parameters()))
            
            if self.__flavour == 'basicio':
                # Note:
                #
                # Basic IO functions can call `basicio.write()` multiple times. So, instead
                # of parsing and modifying output json each time, we're doing it here. We could
                # have done this in `context.close()`, but if it is not called then the output
                # would be sent as plain text.

                set_response_json(g.response.status_code, { 'output': g.response.get_data(as_text=True) })
            elif RET_VAL and (self.__flavour == 'applogic' or self.__flavour == 'advancedio'):
                # Note:
                #
                # AdvancedIO functions can return its own response object, so we're overriding
                # the default response.

                g.response = RET_VAL

    def return_error_response(self, error = None):
        return self.__get_flavour().return_error_response(error)

