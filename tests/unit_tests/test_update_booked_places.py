import pytest
import server


class TestUpdateBookedPlaces:
    booked_places = [
        {
            "competition": "Comp1",
            "club": "Club1",
            "places": 6,
        }
    ]

    def setup_method(self):
        server.booked_places = self.booked_places
        # Reset initial values
        self.booked_places[0]["places"] = 6

    def test_should_update_places(self):
        competition = 'Comp1'
        club = 'Club1'
        places_required = 3

        server.update_booked_places(competition, club, self.booked_places, places_required)

        assert self.booked_places[0]['places'] == 9

    def test_should_failed_to_update_places(self):
        competition = 'Comp1'
        club = 'Club1'
        places_required = 14

        with pytest.raises(ValueError) as e:
            server.update_booked_places(competition, club, self.booked_places, places_required)

        assert str(e.value) == 'Sorry, you cannot purchase more than 12 places'
        assert self.booked_places[0]['places'] == 6
