import pytest
from jose import jwt
from app import schemas
from .database import client,session
from app.config import settings


def test_create_user(client):
    res = client.post(
        "/api/v1/users/", json={"username":"thiere","email": "hello123@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        "/api/v1/login", data={"username": test_user['username'], "password": test_user['password'],"email": test_user['email']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("username, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),

])
def test_incorrect_login(test_user, client, username, password, status_code):
    res = client.post(
        "api/v1/login", data={"username": username, "password": password})

    assert res.status_code == 404
    # assert res.json().get('detail') == 'Invalid Credentials'