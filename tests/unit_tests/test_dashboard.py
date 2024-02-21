import pytest
import server
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestPurchasePlaces:
    competitions = [
        {
            "name": "Test compétition",
            "date": "2024-02-19 11:30:00",
            "numberOfPlaces": "25",
        }
    ]

    clubs = [
        {
            "name": "Test club",
            "email": "test_club@example.com",
            "points": "10",
        },
        {
            "name": "Test club 2",
            "email": "test_club2@example.com",
            "points": "17",
        },
        {
            "name": "Test club 3",
            "email": "test_club3@example.com",
            "points": "4",
        },
    ]

    def setup_method(self):
        server.competitions = self.competitions
        server.clubs = self.clubs
        # Reset the number of places
        self.competitions[0]["numberOfPlaces"] = 25

    def test_should_deduct_club_points(self, client):
        response1 = client.get('/dashboard')
        assert response1.status_code == 200
        assert int(self.clubs[0]["points"]) == 10

        places_booked = 5
        response2 = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        assert response2.status_code == 200

        response3 = client.get('/dashboard')
        assert response3.status_code == 200
        assert int(self.clubs[0]["points"]) == 5
