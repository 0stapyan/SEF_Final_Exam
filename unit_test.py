from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest
from main import fetch_user_data, app

mock_response = {
    "data": [
        {
            "nickname": "testuser",
            "userId": "123",
            "firstSeen": 1633036800
        }
    ]
}

@patch('requests.get')
def test_fetch_user_data(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    result = fetch_user_data(0)

    assert mock_get.called
    assert result == mock_response["data"]
    assert result[0]['nickname'] == "testuser"


client = TestClient(app)

mocked_users_data = [
    {
        "nickname": "JohnDoe",
        "userId": "123",
        "firstSeen": 1633036800
    },
    {
        "nickname": "JaneDoe",
        "userId": "456",
        "firstSeen": None
    }
]

@patch('main.fetch_user_data')
def test_get_user_list(mock_fetch):
    mock_fetch.return_value = mocked_users_data

    response = client.get("/api/users/list")

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)

    assert len(data) == len(mocked_users_data)

    for user in data:
        assert "username" in user
        assert "userId" in user
        assert "firstSeen" in user

        if user["userId"] == "123":
            assert user["username"] == "JohnDoe"
            assert user["firstSeen"] == "2021-09-30 00:00:00"
        elif user["userId"] == "456":
            assert user["username"] == "JaneDoe"
            assert user["firstSeen"] == "Unknown"

