import pytest
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


class TestLogout:
    def test_logout(self, client):
        response = client.get("/logout")
        assert response.status_code == 302
