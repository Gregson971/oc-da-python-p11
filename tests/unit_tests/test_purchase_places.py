import pytest
import server
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_flash(monkeypatch):
    def flash(message, category):
        assert category == "error"
        assert message == "Sorry, you cannot purchase more than 12 places" in message

    monkeypatch.setattr("flask.flash", flash)


@pytest.fixture
def mock_render_template(monkeypatch):
    def render_template(template, club, competition, max_places_available):
        assert template == "booking.html"
        assert club == "Test club"
        assert competition == "Test compétition"
        assert max_places_available == 12

    monkeypatch.setattr("flask.render_template", render_template)


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
        # Reset initial values
        self.competitions[0]["numberOfPlaces"] = 25
        self.clubs[0]["points"] = 15
        self.booked_places[0]["places"] = 0

    def test_purchase_places_with_less_places_than_available(self, client):
        places_booked = 30
        response = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        data = response.get_data()
        assert response.status_code == 400
        assert data.find(b"You do not have enough points") != -1
        assert int(self.competitions[0]["numberOfPlaces"]) == 25
        assert int(self.clubs[0]["points"]) == 15

    def test_purchase_places(self, client):
        places_booked = 5
        response = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        data = response.get_data()
        assert response.status_code == 200
        assert data.find(b"Great-booking complete!") != -1
        assert self.competitions[0]["numberOfPlaces"] == 20
        assert self.clubs[0]["points"] == 10

    def test_should_not_be_able_to_purchase_more_than_12_places(self, client):
        places_booked = 14
        response = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        data = response.get_data()
        assert response.status_code == 400
        assert data.find(b"Sorry, you cannot purchase more than 12 places") != -1
        assert self.booked_places[0]["places"] == 0

    def test_should_deduct_club_points(self, client):
        places_booked = 5
        response = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        assert response.status_code == 200
        assert self.clubs[0]["points"] == 10

    def test_should_enter_purchase_places_between_1_and_12(self, client):
        places_booked = 0
        response = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        assert response.status_code == 400
        data = response.get_data()
        assert data.find(b"Please enter a number between 0 and 12.") != -1

    def test_should_enter_a_valid_number(self, client):
        places_booked = 'hello world'
        response = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        assert response.status_code == 400
        data = response.get_data()
        assert data.find(b"Please enter a valid number for places") != -1

    def test_should_failed_to_update_places(self, client):
        places_booked = 14
        response = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        assert response.status_code == 400
        data = response.get_data()
        assert data.find(b"Sorry, you cannot purchase more than 12 places") != -1

    def test_should_not_be_able_to_purchase_when_competition_has_less_than_12_places(self, client):
        self.competitions[0]["numberOfPlaces"] = 5
        places_booked = 6
        response = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        assert response.status_code == 400
        data = response.get_data()
        assert data.find(b"Sorry, you cannot purchase more than 5 places") != -1
        assert self.booked_places[0]["places"] == 0
        assert self.competitions[0]["numberOfPlaces"] == 5
        assert self.clubs[0]["points"] == 15

    def test_should_return_error_when_no_places_entered(self, client):
        places_booked = ""
        response = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        assert response.status_code == 400
        data = response.get_data()
        assert data.find(b"Please enter a number for places.") != -1
        assert self.booked_places[0]["places"] == 0
        assert self.competitions[0]["numberOfPlaces"] == 25
        assert self.clubs[0]["points"] == 15

    def test_should_failed_if_booked_places_plus_places_required_is_more_than_12(self, client):
        self.booked_places[0]["places"] = 10
        places_booked = 3
        response = client.post(
            '/purchasePlaces',
            data=dict(competition=self.competitions[0]["name"], club=self.clubs[0]["name"], places=places_booked),
        )
        assert response.status_code == 400
        data = response.get_data()
        assert data.find(b"Sorry, you cannot purchase more than 12 places") != -1
        assert self.booked_places[0]["places"] == 10
        assert self.competitions[0]["numberOfPlaces"] == 25
        assert self.clubs[0]["points"] == 15
