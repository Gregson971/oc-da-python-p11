import pytest
import server
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestBookPlaces:
    competitions = [
        {
            "name": "Test compétition",
            "date": "2024-10-19 11:30:00",
            "numberOfPlaces": "25",
        },
        {
            "name": "Test 2 compétition",
            "date": "2023-10-19 11:30:00",
            "numberOfPlaces": "25",
        },
    ]

    clubs = [
        {
            "name": "Test club",
            "email": "test_club@example.com",
            "points": "15",
        }
    ]

    def setup_method(self):
        server.competitions = self.competitions
        server.clubs = self.clubs

    def test_should_not_book_places_in_past_competition(self, client):
        response = client.get("/book/Test 2 compétition/Test club")
        assert response.status_code == 400
        data = response.data.decode()
        assert data.find("This competition is over.") != -1

    def test_should_book_places(self, client):
        response = client.get("/book/Test compétition/Test club")
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("Booking for Test compétition || GUDLFT") != -1

    def test_book_non_existant_competition(self, client):
        response = client.get("/book/random_name/Test club")
        assert response.status_code == 404
        data = response.data.decode()
        assert data.find("Something went wrong-please try again") != -1

    def test_book_non_existant_club(self, client):
        response = client.get("/book/Test compétition/random_name")
        assert response.status_code == 404
        data = response.data.decode()
        assert data.find("Something went wrong-please try again") != -1
