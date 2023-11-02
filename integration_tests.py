import responses
import json
from fastapi.testclient import TestClient
from main import app

@responses.activate
def test_fetch_user_data():
    test_response_data = {
        "data": [
            {
                "username": "testuser",
                "userId": "12345",
                "firstSeen": 1633036800
            }
        ]
    }

    responses.add(
        responses.GET,
        "https://sef.podkolzin.consulting/api/users/lastSeen?offset=0",
        json=test_response_data,
        status=200
    )


client = TestClient(app)

def test_get_user_list_integration():
    response = client.get("/api/users/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
