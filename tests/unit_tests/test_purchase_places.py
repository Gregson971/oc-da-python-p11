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
            "points": "15",
        }
    ]

    places_booked = [
        {
            "competition": "Test compétition",
            "club": "Test club",
            "places": 0,
        }
    ]

    def setup_method(self):
        server.competitions = self.competitions
        server.clubs = self.clubs
        server.places_booked = self.places_booked
        # Reset the number of places
        self.competitions[0]["numberOfPlaces"] = 25

    def test_should_not_be_able_to_purchase_more_than_12_places(self, client):
        places_booked = 14
        response = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        data = response.get_data()
        assert response.status_code == 400
        assert data.find(b"Sorry, you cannot purchase more than 12 places") != -1
        assert self.places_booked[0]["places"] == 0
