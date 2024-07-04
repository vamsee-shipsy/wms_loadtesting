from locust import HttpUser, between, task
import random
from utils.helpers import user_login, load_json
import os
from tasks.product import ProductCreationTaskSet
from tasks.product import AsyncProductCreationTaskSet


class ProductCreationBehaviour(HttpUser):
    tasks = [
        ProductCreationTaskSet
    ]
    wait_time = between(1, 5)
    
    def on_start(self):
        self.access_token_data = user_login(5)
class AsyncProductCreationBehaviour(HttpUser):
    tasks = [
        AsyncProductCreationTaskSet
    ]
    wait_time = between(1, 5)
    
    def on_start(self):
        self.access_token_data = user_login(5)
        
        
        
        