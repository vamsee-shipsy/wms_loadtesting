from locust import HttpUser, between
import random
from utils.helpers import user_login, order_payload_creation, load_json, is_token_expired
from utils.logger import setup_logger
import os
from tasks.sale_order import SaleOrderTaskSet, AsyncSaleOrderTaskSet

class SaleOrderBehaviour(HttpUser):
    tasks = [
        SaleOrderTaskSet
    ]
    wait_time = between(1, 5)
    
    def on_start(self):
        if not os.path.exists('data/access_token_data.json'):
            self.access_token_data = user_login(5)
        else:
            self.access_token_data = load_json('data/access_token_data.json')
            for token_data in self.access_token_data:
                if is_token_expired(token_data['expires_at']):
                    self.access_token_data = user_login(5)
                    break
                
        self.logger = setup_logger('sync_sale_order_creation', 'logs/sync_sale_order_creation.log')
        self.order_payload = order_payload_creation(no_of_items=1000)
        
class AsyncSaleOrderBehaviour(HttpUser):
    tasks = [
        AsyncSaleOrderTaskSet
    ]
    wait_time = between(1, 5)
    
    def on_start(self):
        if not os.path.exists('data/access_token_data.json'):
            self.access_token_data = user_login(5)
        else:
            self.access_token_data = load_json('data/access_token_data.json')
            for token_data in self.access_token_data:
                if is_token_expired(token_data['expires_at']):
                    self.access_token_data = user_login(5)
                    break
                
        self.logger = setup_logger('async_sale_order_creation', 'logs/async_sale_order_creation.log')
        self.order_payload = order_payload_creation(no_of_items=1000)
    
