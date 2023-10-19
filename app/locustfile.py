import time
from locust import HttpUser, task

class User(HttpUser):
    @task(5)
    def calculate(self):
        self.client.get("/calculate?value1=10&value2=2&method=sum&form=sent")
        time.sleep(1)

    @task
    def report(self):
        self.client.get("/report")
        time.sleep(1)