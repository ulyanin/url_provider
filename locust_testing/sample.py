from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):

    @task
    def ping(self):
        self.client.get("/ping/")

    @task
    def get(self):
        self.client.get("/get/1DOVm1")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 5000
    max_wait = 15000