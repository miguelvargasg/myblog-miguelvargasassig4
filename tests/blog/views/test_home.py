import pytest

# Needed for database
pytestmark = pytest.mark.django_db


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
