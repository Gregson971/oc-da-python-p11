from locust import HttpUser, task, between
from helpers import loadCompetitions, loadClubs


class PerfTestServer(HttpUser):
    wait_time = between(1, 5)
    competition = loadCompetitions()[3]
    club = loadClubs()[3]

    def on_start(self):
        self.client.get("/", name="index")
        self.client.post("/showSummary", data=dict(email=self.club["email"]), name="showSummary")

    @task
    def book(self):
        self.client.get(f"/book/{self.competition['name']}/{self.club['name']}", name="book")

    @task
    def purchase(self):
        self.client.post(
            '/purchasePlaces',
            data=dict(competition=self.competition["name"], club=self.club["name"], places=1),
            name="purchasePlaces",
        )

    @task
    def show_dashboard(self):
        self.client.get("/dashboard", name="dashboard")
