import json
import requests
from copy import deepcopy
from datetime import datetime, timedelta
from config.settings import BASE_URL, LOGIN_CREDENTIALS
from utils.logger import setup_logger

user_login_logger = setup_logger('user_login', 'logs/user_login.log')

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
    
def is_token_expired(expiry_time_str):
    expiry_time = datetime.strptime(expiry_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return datetime.utcnow() > expiry_time
    
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
        user_login_logger.info(f"User: {user.get('username')} - {token_response_data}")
        if token_response_data.get('access_token'):
            expiry_time = (datetime.utcnow() + timedelta(seconds=token_response_data.get('expires_in'))).isoformat() + 'Z'
            data['access_token'] = token_response_data.get('access_token')
            data['warehouse'] = user.get('warehouse')
            data['expires_at'] = expiry_time
            access_token_data.append(data)
    save_json(access_token_data, 'data/access_token_data.json')
    return access_token_data

def order_payload_creation(no_of_orders=1, no_of_items=1000):
    
    order_headers = {
        "order_type":"slot",
        "promised_time": "2022-01-23 16:30:00",
        "slot_from": "2022-01-23 15:30:00",
        "slot_to": "2022-01-23 16:30:00",
        "order_reference": "",
        "customer": {
            "customer_reference": "TEST",
            "customer_name": "TEST"
        },
        "payment_info": {
            "payment_mode": "prepaid",
            "method_of_payment": "",
            "transaction_id": "",
            "paid_amount": 250.0,
            "payment_date": "2021-07-17"
        },
        "charges": [
            {
                "name": "shipping charges",
                "amount": 25,
                "tax_amount": 0
            },
            {
                "name": "packing charges",
                "amount": 10,
                "tax_amount": 0
            }
        ],
    }
    final_payload = []
    while no_of_orders:
        data = deepcopy(order_headers)
        data['items'] = load_json('data/sale_order_items.json')[:no_of_items]
        final_payload.append(data) 
        no_of_orders -= 1
    return final_payload

if __name__ == '__main__':
    user_login(20)