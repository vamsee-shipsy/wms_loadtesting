import json
import requests
from config.settings import BASE_URL, LOGIN_CREDENTIALS

def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f)

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    
def append_json(data, file_path):
    current_data = load_json(file_path)
    current_data.append(data)
    save_json(current_data, file_path)
    
def user_login(no_of_users=1):
    login_url = f"{BASE_URL}/auth/login/"
    users_data = load_json('data/subuser_data.json')
    access_token_data = []
    for user in users_data[:no_of_users]:
        data = {}
        payload = {
            "login_id": user.get("username"),
            "password": LOGIN_CREDENTIALS.get("password")
        }
        response = requests.post(login_url, data=payload)
        response_data = response.json()
        client_id, client_secret = '', ''
        if response_data.get('message') == "Success":
            client_id = response_data.get('client_id')
            client_secret = response_data.get('client_secret')
            
        get_token_payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
        token_response = requests.post(f"{BASE_URL}/o/token/", data=get_token_payload)
        token_response_data = token_response.json()
        if token_response_data.get('access_token'):
            data['access_token'] = token_response_data.get('access_token')
            data['warehouse'] = user.get('warehouse')
            save_json(user, 'data/login_data.json')
            access_token_data.append(data)
    return access_token_data

if __name__ == '__main__':
    user_login()