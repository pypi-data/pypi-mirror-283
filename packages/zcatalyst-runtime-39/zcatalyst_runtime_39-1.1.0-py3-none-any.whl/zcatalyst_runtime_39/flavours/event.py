import os
import time

from flavours import FlavourHandler
from flavours.utils import get_request_json, set_response_json

class EventDetails:
    def __init__(self) -> None:
        self.__catalyst_body = get_request_json()
        
        self.data = self.__catalyst_body.get('data')
        self.time = self.__catalyst_body.get('event_time')

    def get_project_details(self):
        return self.__catalyst_body.get('project_details')

    def get_data(self):
        return self.__catalyst_body.get('data')

    def get_time(self):
        return self.__catalyst_body.get('event_time')

    def get_action(self):
        return self.__catalyst_body.get('action')
    
    def get_source(self):
        return self.__catalyst_body.get('source')

    def get_source_entity_id(self):
        return self.__catalyst_body.get('source_entity_id')

    def get_event_bus_details(self):
        return self.__catalyst_body.get('event_bus_details')
    
    def get_raw_data(self):
        """
        get raw data of the event

        Returns:
        dict: raw data
        """
        return self.__catalyst_body

class Context():
    __max_execution_time_ms = int(os.getenv('CATALYST_MAX_TIMEOUT', -1)) 

    def __init__(self) -> None:
        max_execution_buffer_time_ms = 500
        max_execution_hidden_time_ms = self.__max_execution_time_ms - max_execution_buffer_time_ms

        self.__endtime_timestamp = int(time.time() * 1000) + max_execution_hidden_time_ms

    def close_with_success(self):
        set_response_json(200)

    def close_with_failure(self):
        set_response_json(530)

    def get_remaining_execution_time_ms(self):
        time_remaining = self.__endtime_timestamp - int(time.time() * 1000)
        return 0 if time_remaining < 0 else time_remaining

    def get_max_execution_time_ms(self):
        return Context.__max_execution_time_ms


class EventHandler(FlavourHandler):
    def construct_function_parameters():
        return (EventDetails(), Context())

    def return_error_response(error):
        set_response_json(532, { 'error': error })