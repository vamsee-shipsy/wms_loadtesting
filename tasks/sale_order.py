import json
import random
import time
from locust import TaskSet, task
from utils.helpers import load_json

class SaleOrderTaskSet(TaskSet):

    def on_start(self):
        self.access_token_data = self.user.access_token_data
        self.payload = json.dumps(self.user.order_payload)

    @task
    def create_sale_order(self):
        token_data = random.choice(self.access_token_data)
        headers = {
            "Authorization": token_data.get('access_token'),
            "warehouse": token_data.get('warehouse')
        }
        payload = self.payload
        with self.client.post("/api/v1/outbound/orders/", headers=headers, data=payload, catch_response=True, name='order_creation') as sync_response:
            try:
                response_data = sync_response.json()
                if sync_response.status_code != 200:
                    self.user.logger.error(f"Failed to create sale order through sync, error response : {response_data} in warehouse: {token_data.get('warehouse')} with access token: {token_data.get('access_token')}")
                    sync_response.failure(f"Failed to create sale order through sync, {response_data}")
                else:
                    self.user.logger.info(f"Sale order created successfully with warehouse: {token_data.get('warehouse')}")
            except Exception as e:
                self.user.logger.error(f"Failed to create sale order through sync, error response : {sync_response.text} in warehouse: {token_data.get('warehouse')} with access token: {token_data.get('access_token')}")
                sync_response.failure(f"Failed to create sale order through sync, {sync_response.status_code}")


class AsyncSaleOrderTaskSet(TaskSet):

    def on_start(self):
        self.access_token_data = self.user.access_token_data
        self.payload = json.dumps(self.user.order_payload)

    @task
    def create_async_sale_order(self):
        token_data = random.choice(self.access_token_data)
        self.headers = {
            "Authorization": token_data.get('access_token'),
            "warehouse": token_data.get('warehouse')
        }
        payload = self.payload
        with self.client.post("/api/v1/async/outbound/orders/", headers=self.headers, data=payload, catch_response=True, name='async_order_creation') as async_response:
            try:
                response_data = async_response.json()
                if response_data.get('id'):
                    self.uuid = response_data.get('id')
                    self.user.logger.info(f"Sale order created successfully with warehouse: {token_data.get('warehouse')} with id: {self.uuid}")
                else:
                    self.user.logger.error(f"Failed to create sale order through async, error response : {response_data}")
                    async_response.failure(f"Failed to create sale order through async, {response_data}")
            except Exception as e:
                self.user.logger.error(f"Failed to create sale order through async, error response : {async_response.text} in warehouse: {token_data.get('warehouse')} with access token: {token_data.get('access_token')}")
                async_response.failure(f"Failed to create sale order through async, {async_response.status_code}")
        # params = {
        #     "id": self.uuid
        # }
        # while True:
        #     with self.client.get("/api/v1/async/core/api_status/", headers=self.headers, params=params, catch_response=True, name='async_order_check') as get_response:
        #         time.sleep(2)
        #         response_data = get_response.json()
        #         if response_data.get('data',[])[0].get('status') == "Failed":
        #             get_response.failure(f"Failed to create sale order through async, {response_data}")
        #             break
        #         elif response_data.get('data',[])[0].get('status') == "Success":
        #             break
        #         else:
        #             continue
