import random
import json
import time
from utils.helpers import load_json
from locust import TaskSet, task
from utils.logger import setup_logger
from config.settings import WAREHOUSES

sync_product_creation_logger = setup_logger('sync_product_creation', 'logs/sync_product_creation.log')


class ProductCreationTaskSet(TaskSet):

    def on_start(self):
        self.access_token_data = self.user.access_token_data


    @task()
    def create_product(self):
        token_data = self.access_token_data[0]
        warehouse = random.choice(WAREHOUSES)
        headers = {
            "Authorization": token_data.get('access_token'),
            "warehouse": warehouse
        }
        payload = {
            "warehouse": warehouse,
            "skus": load_json('data/sku_data.json')
        }
        payload = json.dumps(payload)
        with self.client.post("/api/v1/core/products/", headers=headers, data=payload, catch_response=True, name='product_creation') as sync_response:
            try:
                response_data = sync_response.json()
                if sync_response.status_code != 200:
                    sync_product_creation_logger.error(f"Failed to create product through sync, error response : {response_data} in warehouse: {warehouse}")
                    sync_response.failure("Failed to create product through sync")
                else:
                    sync_product_creation_logger.info(f"Product created successfully with warehouse: {token_data.get('warehouse')}")
            except Exception as e:
                sync_product_creation_logger.error(f"Failed to create product through sync, error response : {sync_response.text} in warehouse: {warehouse}")
                sync_response.failure(f"Failed to create product through sync, error response : {sync_response.status_code}")

class AsyncProductCreationTaskSet(TaskSet):

    def on_start(self):
        self.access_token_data = self.user.access_token_data

    @task()
    def create_async_product(self):
        self.token_data =  self.access_token_data[0]
        warehouse = random.choice(WAREHOUSES)
        self.headers = {
            "Authorization": self.token_data.get('access_token'),
            "warehouse": warehouse
        }

        payload = {
            "warehouse": warehouse,
            "skus": load_json('data/sku_data.json')
        }
        payload = json.dumps(payload)
        with self.client.post("/api/v1/async/core/products/", headers=self.headers, data=payload, catch_response=True, name='async_product_creatoin') as response:
            try:
                response_data = response.json()
                if response_data.get('id'):
                    self.uuid = response_data.get('id')
                    self.user.logger.info(f"Product created successfully with warehouse: {warehouse} with id: {self.uuid}")
                else:
                    self.user.logger.error(f"Failed to create product through async, error response : {response_data}")
                    response.failure("Failed to create product through async")
            except Exception as e:
                self.user.logger.error(f"Failed to create product through async, error response : {response.text}")
                response.failure(f"Failed to create product through async, error response : {response.status_code}")
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
