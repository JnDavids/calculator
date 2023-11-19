import time
from locust import HttpUser, task


class User(HttpUser):

    @task(5)
    def calculate(self):
        self.client.get("/calculate?value_1=10&value_2=2&operation=sum")
        time.sleep(1)

    @task
    def report(self):
        self.client.get("/report")
        time.sleep(1)