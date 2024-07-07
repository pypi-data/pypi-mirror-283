import requests
from ..exceptions import TensorDockAPIException

class VirtualMachines:
    def __init__(self, api):
        self.api = api

    def _make_request(self, endpoint, data):
        url = f"{self.api.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data['api_key'] = self.api.api_key
        data['api_token'] = self.api.api_token
        
        response = requests.post(url, data=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise TensorDockAPIException(f"Error in {endpoint}: {response.text}")

    def deploy_vm(self, **kwargs):
        return self._make_request('deploy_vm', kwargs)

    def validate_spot_price_new(self, **kwargs):
        return self._make_request('validate_spot_price_new', kwargs)

    def validate_spot_price_existing(self, **kwargs):
        return self._make_request('validate_spot_price_existing', kwargs)

    def list_vms(self):
        return self._make_request('list_vms', {})

    def get_vm_details(self, vm_id):
        return self._make_request('vm_details', {'vm_id': vm_id})

    def start_vm(self, vm_id):
        return self._make_request('start_vm', {'vm_id': vm_id})

    def stop_vm(self, vm_id):
        return self._make_request('stop_vm', {'vm_id': vm_id})

    def modify_vm(self, vm_id, **kwargs):
        kwargs['vm_id'] = vm_id
        return self._make_request('modify_vm', kwargs)

    def delete_vm(self, vm_id):
        return self._make_request('delete_vm', {'vm_id': vm_id})