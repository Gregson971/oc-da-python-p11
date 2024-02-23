import pytest
import server
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestIntegration:
    competitions = [
        {
            "name": "Test compétition",
            "date": "2025-02-19 11:30:00",
            "numberOfPlaces": "25",
        }
    ]

    clubs = [
        {
            "name": "Test club",
            "email": "test_club@example.com",
            "points": "15",
        }
    ]

    booked_places = [
        {
            "competition": "Test compétition",
            "club": "Test club",
            "places": 0,
        }
    ]

    def setup_method(self):
        server.competitions = self.competitions
        server.clubs = self.clubs
        server.booked_places = self.booked_places

    def test_should_login_book_purchase_see_points(self, client):
        # Login
        response = client.post("/showSummary", data=dict(email=self.clubs[0]["email"]), follow_redirects=True)
        assert response.status_code == 200

        # Book places
        response = client.get(f'/book/{self.competitions[0]["name"]}/{self.clubs[0]["name"]}')
        assert response.status_code == 200

        # Purchase places
        places_booked = 5
        response = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        data = response.get_data()
        assert response.status_code == 200
        assert data.find(b"Great-booking complete!") != -1
        assert int(self.competitions[0]["numberOfPlaces"]) == 20
        assert int(self.clubs[0]["points"]) == 10

        # See points
        response = client.get('/dashboard')
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("Dashboard | GUDLFT") != -1
        assert int(self.clubs[0]["points"]) == 10
