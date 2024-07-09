import os
import time
import logging

import requests

from flavours.utils import get_env_strict

# Note:
# 'requests' library writes debug logs for each http request, so we're 
# setting the 'requests' and 'urllib3' logging level to WARNING.
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

CATALYST_AUTH_TOKEN = get_env_strict('X_ZOHO_ADMIN_CRED_TOKEN')
CATALYST_PROJECT_SECRET_KEY = get_env_strict('X_ZOHO_PROJECT_SECRET_KEY')
CATALYST_ORG = get_env_strict('X_ZOHO_CATALYST_ORG')
CATALYST_ENVIRONMENT = get_env_strict('X_ZOHO_CATALYST_ENVIRONMENT')
CATALYST_JOB_ID = get_env_strict('X_ZOHO_JOBMETA_JOBID')
MAX_RETRIES = 2

def get_job_data(i_retry = 0):
    if i_retry > MAX_RETRIES:
        logging.error('get job details retry count exceeded!')
        os._exit(1)

    request_url = get_env_strict('X_ZOHO_DATA_URL')
    request_params = {
        'jobId': CATALYST_JOB_ID,
    }
    request_headers = { 
        'Authorization': f'Bearer {CATALYST_AUTH_TOKEN}',
        'X-ZC-PROJECT-SECRET-KEY': CATALYST_PROJECT_SECRET_KEY,
        'CATALYST-ORG': CATALYST_ORG,
        'Environment': CATALYST_ENVIRONMENT,
    }

    response = requests.get(request_url, params=request_params, headers=request_headers)

    if response.status_code == 200:
        return response.json()['data']
    else:
        time.sleep(1)
        return get_job_data(i_retry + 1)

def post_job_status(job_status, i_retry = 0):
    if i_retry > MAX_RETRIES:
        logging.error('post job status retry count exceeded!')
        os._exit(1)

    request_url = get_env_strict('X_ZOHO_CALLBACK_URL')
    request_headers = { 
        'Authorization': f'Bearer {CATALYST_AUTH_TOKEN}',
        'X-ZC-PROJECT-SECRET-KEY': CATALYST_PROJECT_SECRET_KEY,
        'CATALYST-ORG': CATALYST_ORG,
        'Environment': CATALYST_ENVIRONMENT,
    }
    request_data = { 
        'job_id': CATALYST_JOB_ID, 
        'job_status': job_status
    }

    response = requests.post(request_url, headers=request_headers, json=request_data)

    if response.status_code == 200:
        os._exit(0)
    else:
        time.sleep(1)
        return post_job_status(job_status, i_retry + 1)
        