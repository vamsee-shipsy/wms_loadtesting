from locust import HttpUser, between, task
from utils.helpers import user_login
from utils.logger import setup_logger



class UserBehaviour(HttpUser):

    wait_time = between(1, 5)

    @task()
    def user_authentication(self):
        user_login(1)
