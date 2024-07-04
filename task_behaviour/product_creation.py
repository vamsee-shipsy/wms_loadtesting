from locust import HttpUser, between, task
import random
from utils.helpers import user_login, load_json, is_token_expired
from utils.logger import setup_logger
import os
from tasks.product import ProductCreationTaskSet
from tasks.product import AsyncProductCreationTaskSet

class ProductCreationBehaviour(HttpUser):
    tasks = [
        ProductCreationTaskSet
    ]
    wait_time = between(1, 5)
    
    def on_start(self):
        if not os.path.exists('data/access_token_data.json'):
            self.access_token_data = user_login(10)
        else:
            self.access_token_data = load_json('data/access_token_data.json')
            for token_data in self.access_token_data:
                if is_token_expired(token_data['expires_at']):
                    self.access_token_data = user_login(10)
                    break
                
        self.logger = setup_logger('sync_product_creation', 'logs/sync_product_creation.log')
        

class AsyncProductCreationBehaviour(HttpUser):
    tasks = [
        AsyncProductCreationTaskSet
    ]
    wait_time = between(1, 10)

    def on_start(self):
        if not os.path.exists('data/access_token_data.json'):
            self.access_token_data = user_login(10)
        else:
            self.access_token_data = load_json('data/access_token_data.json')
            for token_data in self.access_token_data:
                if is_token_expired(token_data['expires_at']):
                    self.access_token_data = user_login(10)
                    break
                
        self.logger = setup_logger('async_product_creation', 'logs/async_product_creation.log')