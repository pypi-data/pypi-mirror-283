import os
import time

from flavours import FlavourHandler
from flavours.job_utils import get_job_data, post_job_status

class JobDetails:
    def __init__(self) -> None:
        self.__job_data = get_job_data()
    
    def get_job_details(self):
        return self.__job_data['job_details']
    
    def get_job_meta_details(self):
        return self.get_job_details()['job_meta_details']
    
    def get_job_pool_details(self):
        return self.get_job_meta_details()['jobpool_details']
    
    def get_project_details(self):
        return self.get_job_pool_details()['project_details']
    
    def get_job_capacity_attributes(self):
        return self.get_job_details()['capacity']
    
    def get_all_job_params(self):
        return self.get_job_meta_details()['params']
    
    def get_job_param(self, key: str):
        return self.get_all_job_params()[key]

class Context:
    __max_execution_time_ms = int(os.getenv('CATALYST_MAX_TIMEOUT', -1)) 

    def __init__(self) -> None:
        max_execution_buffer_time_ms = 500
        max_execution_hidden_time_ms = self.__max_execution_time_ms - max_execution_buffer_time_ms

        self.__endtime_timestamp = int(time.time() * 1000) + max_execution_hidden_time_ms

    def close_with_success(self):
        post_job_status(200)

    def close_with_failure(self):
        post_job_status(530)

    def get_remaining_execution_time_ms(self):
        time_remaining = self.__endtime_timestamp - int(time.time() * 1000)
        return 0 if time_remaining < 0 else time_remaining

    def get_max_execution_time_ms(self):
        return Context.__max_execution_time_ms

class JobHandler(FlavourHandler):
    def construct_function_parameters():
        return (JobDetails(), Context())

    def return_error_response(_error):
        post_job_status(532)