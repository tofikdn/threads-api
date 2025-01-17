import requests
import json

from threads_api.src.http_sessions.abstract_session import HTTPSession
from threads_api.src.threads_api import log

class RequestsSession(HTTPSession):
    def __init__(self):
        self._session = requests.Session()

    async def start(self):
        if self._session is None:
            self._session = requests.Session()

    async def close(self):
        self._session.close()
        self._session = None

    def auth(self, auth_callback_func, **kwargs):
        return auth_callback_func(**kwargs)

    async def post(self, **kwargs):
        log(title='PRIVATE REQUEST', type='POST', requests_session_params=vars(self._session), **kwargs)
        response = self._session.post(**kwargs)
        try:
            resp = response.json()
            log(title='PRIVATE RESPONSE', response=resp)

            if resp['status'] == 'fail':
                raise Exception(f"Request Failed: [{resp['message']}]")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            raise Exception('Failed to decode response as JSON')
        
        return resp

    async def get(self, **kwargs):
        log(title='PRIVATE REQUEST', type='GET', **kwargs)
        response = self._session.get(**kwargs)
        try:
            resp = response.json()
            log(title='PRIVATE RESPONSE', response=resp)

            if resp['status'] == 'fail':
                raise Exception(f"Request Failed: [{resp['message']}]")
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            raise Exception('Failed to decode response as JSON')
        
        return resp