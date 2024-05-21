# https://blog.csdn.net/qq_38924521/article/details/127693336

from locust import HttpUser, constant, task, TaskSet


class TaskApi(TaskSet):

    @task(1)
    def login1(self):
        url = '/b'
        # data = {"userName": "xuyang@test.ai", "password": "xy123456"}
        headers = {"Content-Type": "application/json"}
        # self.client.request(method='GET', url=url, json=data, headers=headers, name='login-登录接口1')
        self.client.request(method='GET', url=url, headers=headers, name='login-demo1')

    @task(1)
    def login2(self):
        url = '/a'
        # data = {"userName": "xuyang@test.ai", "password": "xy123456"}
        headers = {"Content-Type": "application/json"}
        self.client.request(method='GET', url=url, headers=headers, name='login-demo2')

    @task(1)
    def login3(self):
        url = '/c'
        # data = {"userName": "xuyang@test.ai", "password": "xy123456"}
        headers = {"Content-Type": "application/json"}
        # self.client.request(method='GET', url=url, json=data, headers=headers, name='login-登录接口1')
        self.client.request(method='GET', url=url, headers=headers, name='login-demo3')

    @task(1)
    def login4(self):
        url = '/d'
        # data = {"userName": "xuyang@test.ai", "password": "xy123456"}
        headers = {"Content-Type": "application/json"}
        self.client.request(method='GET', url=url, headers=headers, name='login-demo4')
class FlashUser(HttpUser):
    host = 'http://127.0.0.1:8000'
    # wait_time = constant(2)
    tasks = [TaskApi]

