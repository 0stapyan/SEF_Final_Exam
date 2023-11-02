import requests

def test_user_creation_and_listing():
    base_url = "http://localhost:8000"

    list_response = requests.get(f"{base_url}/api/users/list")
    assert list_response.status_code == 200
    initial_users = list_response.json()
    assert isinstance(initial_users, list)

    new_user_data = {"username": "testuser", "email": "test@example.com"}
    create_response = requests.post(f"{base_url}/api/users/create", json=new_user_data)
    assert create_response.status_code == 200

    updated_list_response = requests.get(f"{base_url}/api/users/list")
    assert updated_list_response.status_code == 200
    updated_users = updated_list_response.json()
    assert isinstance(updated_users, list)

    assert len(updated_users) == len(initial_users) + 1

    assert any(user['username'] == "testuser" for user in updated_users)

test_user_creation_and_listing()

