from locust import HttpUser, between
import random
from utils.helpers import user_login, order_payload_creation
import os
from tasks.sale_order import SaleOrderTaskSet, AsyncSaleOrderTaskSet

class SaleOrderBehaviour(HttpUser):
    tasks = [
        SaleOrderTaskSet
    ]
    wait_time = between(1, 5)
    
    def on_start(self):
        self.access_token_data = user_login(5)
        self.order_payload = order_payload_creation(no_of_items=1000)
        
class AsyncSaleOrderBehaviour(HttpUser):
    tasks = [
        AsyncSaleOrderTaskSet
    ]
    wait_time = between(1, 5)
    
    def on_start(self):
        self.access_token_data = user_login(5)
        self.order_payload = order_payload_creation(no_of_items=1000)
    
