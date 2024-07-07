import requests
from ..exceptions import TensorDockAPIException

class Servers:
    def __init__(self, api):
        self.api = api

    def _make_request(self, endpoint, data=None):
        url = f"{self.api.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = data or {}
        data['api_key'] = self.api.api_key
        data['api_token'] = self.api.api_token
        
        response = requests.get(url, params=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise TensorDockAPIException(f"Error in {endpoint}: {response.text}")

    def get_available_servers(self):
        return self._make_request('available_servers')

    def get_available_hostnodes(self):
        return self._make_request('available_hostnodes')

    def get_hostnode_details(self, hostnode_id):
        data = {'hostnode_id': hostnode_id}
        return self._make_request('hostnode_details', data)