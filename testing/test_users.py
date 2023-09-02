from ..app.schema import UserOut, Token
import pytest
from jose import jwt
from ..app.env import settings


def test_home_path(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


def test_user_creation(client):
    response = client.post(
        "/users/", json={"email": "userfromtesting@gmail.com", "password": "hellotesting"})
    new_user = UserOut(**response.json())
    assert response.status_code == 201
    assert new_user.email == "userfromtesting@gmail.com"


def test_login(client, test_user):
    response = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = Token(**response.json())
    payload = jwt.decode(login_res.access_token,
                         settings.SECRET_KEY, settings.ALGORITHM)
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == 'bearer'
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongEmail@gmail.com", "password123", 403),
    ("userfromtesting@gmail.com", "wrongPassword", 403),
    (None, "password123!", 422),
    ("userfromtesting@gmail.com", None, 422),
])
def test_failed_login(client, email, password, status_code):
    response = client.post(
        "/login", data={"username": email, "password": password})
    assert response.status_code == status_code
    if (response.status_code == 403):
        assert response.json().get('detail') == "Invalid Credentials Not Found."
