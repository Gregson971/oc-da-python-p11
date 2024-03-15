import pytest
import server
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestShowSummary:
    clubs = [
        {
            "name": "Test club",
            "email": "test_club@example.com",
            "points": "15",
        }
    ]

    def setup_method(self):
        server.clubs = self.clubs

    def test_showSummary_with_empty_mail(self, client):
        response = client.post("/showSummary", data=dict(email=""))
        data = response.data.decode()
        assert data.find("Please enter your email address") != -1
        assert response.status_code == 401

    def test_showSummary_with_invalid_mail(self, client):
        response = client.post("/showSummary", data=dict(email="test@example.com"))
        data = response.data.decode()
        assert data.find("The email address you entered does not exist") != -1
        assert response.status_code == 401

    def test_showSummary_with_valid_mail(self, client):
        response = client.post("/showSummary", data=dict(email=self.clubs[0]["email"]), follow_redirects=True)
        data = response.data.decode()
        assert data.find("Welcome, test_club@example.com") != -1
        assert response.status_code == 200
