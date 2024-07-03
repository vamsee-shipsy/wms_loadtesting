import random
import json
import time
from utils.helpers import load_json
from locust import TaskSet, task



class ProductCreationTaskSet(TaskSet):
    
    def on_start(self):
        self.access_token_data = self.user.access_token_data
    
    
    @task
    def create_product(self):
        token_data = random.choice(self.access_token_data)
        headers = {
            "Authorization": token_data.get('access_token'),
            "warehouse": token_data.get('warehouse')
        }
        payload = {
            "warehouse": f"{token_data.get('warehouse')}",
            "skus": load_json('data/sku_data.json')
        }
        payload = json.dumps(payload)
        self.client.post("/api/v1/core/products/", headers=headers, data=payload, name='product_creation')

class AsyncProductCreationTaskSet(TaskSet):
    
    def on_start(self):
        self.access_token_data = self.user.access_token_data
        
    @task()
    def create_async_product(self):
        self.token_data = random.choice(self.access_token_data)
        self.headers = {
            "Authorization": self.token_data.get('access_token'),
            "warehouse": self.token_data.get('warehouse')
        }
        
        payload = {
            "warehouse": f"{self.token_data.get('warehouse')}",
            "skus": load_json('data/sku_data.json')
        }
        payload = json.dumps(payload)
        with self.client.post("/api/v1/async/core/products/", headers=self.headers, data=payload, catch_response=True, name='async_product_creatoin') as response:
            response_data = response.json()
            print(response_data)
            if response_data.get('id'):
                self.uuid = response_data.get('id')
            else:
                response.failure("Failed to create product through async")      
        # params = {
        #     "id": self.uuid
        # }
        # while True:
        #     with self.client.get("/api/v1/async/core/api_status/", headers=self.headers, params=params, catch_response=True, name='async_product_check') as get_response:
        #         time.sleep(2)
        #         response_data = get_response.json()
        #         if response_data.get('data',[])[0].get('status') == "Failed":
        #             get_response.failure(f"Failed to create product through async, error response : {response_data.get('data',[])[0].get('result')}")
        #             break
        #         elif response_data.get('data',[])[0].get('status') == "Completed":
        #             break
        #         else:
        #             continue
                
