import requests

class UserManagement:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'api-key': self.api_key
        }

    def create_user(self, user_id, name, plan, plan_type=None, plan_duration_days=None, tokens=None):
        data = {
            'userId': user_id,
            'nombre': name,
            'plan': plan,
            'planType': plan_type,
            'planDurationDays': plan_duration_days,
            'tokens': tokens
        }
        response = requests.post(f'{self.api_url}/users/create', json=data, headers=self._get_headers())
        return response.json()

    def get_user(self, user_id):
        response = requests.get(f'{self.api_url}/users/info/{user_id}', headers=self._get_headers())
        return response.json()

    def list_users(self, plan=None):
        url = f'{self.api_url}/users/list'
        if plan:
            url += f'/{plan}'
        response = requests.get(url, headers=self._get_headers())
        return response.json()

    def edit_user(self, user_id, name=None, plan=None, plan_type=None, plan_duration_days=None, tokens=None):
        data = {
            'nombre': name,
            'plan': plan,
            'planType': plan_type,
            'planDurationDays': plan_duration_days,
            'tokens': tokens
        }
        response = requests.put(f'{self.api_url}/users/edit/{user_id}', json=data, headers=self._get_headers())
        return response.json()

    def delete_user(self, user_id):
        response = requests.delete(f'{self.api_url}/users/delete/{user_id}', headers=self._get_headers())
        return response.json()

    def verify_user(self, user_id):
        data = {'userId': user_id}
        response = requests.post(f'{self.api_url}/users/verify', json=data, headers=self._get_headers())
        return response.json()

    def consume_token(self, user_id):
        data = {'userId': user_id}
        response = requests.post(f'{self.api_url}/users/consume-token', json=data, headers=self._get_headers())
        return response.json()