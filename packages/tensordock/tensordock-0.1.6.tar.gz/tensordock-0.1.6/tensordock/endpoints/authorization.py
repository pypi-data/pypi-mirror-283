import requests
from ..exceptions import TensorDockAPIException

class Authorization:
    def __init__(self, api):
        self.api = api

    def test_authorization(self):
        url = f"{self.api.base_url}/auth/test"  # Note the corrected endpoint
        data = {
            'api_key': self.api.api_key,
            'api_token': self.api.api_token
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise TensorDockAPIException(f"Error testing authorization: {response.text}")