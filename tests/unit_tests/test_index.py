import pytest
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestIndex:
    def test_index(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.data.decode()
        assert data.find("Welcome to the GUDLFT Registration Portal!") != -1
