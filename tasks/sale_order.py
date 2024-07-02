import json
import random
import time
from locust import TaskSet, task
from utils.helpers import load_json

class SaleOrderTaskSet(TaskSet):
    
    def on_start(self):
        self.access_token_data = self.user.access_token_data
    
    @task
    def create_sale_order(self):
        token_data = random.choice(self.access_token_data)
        headers = {
            "Authorization": token_data.get('access_token'),
            "warehouse": token_data.get('warehouse')
        }
        payload = {
            "warehouse": f"{token_data.get('warehouse')}",
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
            "items": load_json('data/sale_order_items.json')
        }
        payload = json.dumps(payload)
        self.client.post("/api/v1/outbound/orders/", headers=headers, data=payload)
        
class AsyncSaleOrderTaskSet(TaskSet):
    
    def on_start(self):
        self.access_token_data = self.user.access_token_data
    
    @task
    def create_async_sale_order(self):
        token_data = random.choice(self.access_token_data)
        self.headers = {
            "Authorization": token_data.get('access_token'),
            "warehouse": token_data.get('warehouse')
        }
        payload = {
            "warehouse": f"{token_data.get('warehouse')}",
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
            "items": load_json('data/sale_order_items.json')
        }
        payload = json.dumps(payload)
        with self.client.post("/api/v1/async/outbound/orders/", headers=self.headers, data=payload) as async_response:
            response_data = async_response.json()
            if response_data.get('id'):
                self.uuid = response_data.get('id')
            else:
                async_response.failure("Failed to create product through async")   
        params = {
            "id": self.uuid
        }
        while True:
            with self.client.get("/api/v1/async/core/api_status/", headers=self.headers, params=params) as get_response:
                time.sleep(2)
                response_data = get_response.json()
                if response_data.get('data',[])[0].get('status') == "Failed":
                    get_response.failure("Failed to create product through async") 
                elif response_data.get('data',[])[0].get('status') == "Success":
                    break
                else:
                    continue
        
        
        
    