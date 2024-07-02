from locust import HttpUser, between, task
import random
from utils.helpers import user_login
import os
from tasks.product import ProductCreationTaskSet
from tasks.product import AsyncProductCreationTaskSet


class ProductCreationBehaviour(HttpUser):
    tasks = {
        ProductCreationTaskSet: 1
    }
    wait_time = between(1, 5)
    
    def on_start(self):
        self.access_token_data = user_login(4)
class AsyncProductCreationBehaviour(HttpUser):
    tasks = {
        AsyncProductCreationTaskSet: 1
    }
    wait_time = between(1, 5)
    
    def on_start(self):
        self.access_token_data = user_login(4)
        
        
        