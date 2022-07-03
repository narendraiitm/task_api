import pytest
from main import dev_app


@pytest.fixture
def client():
    return dev_app.test_client()


@pytest.fixture
def auth_token():
    res = dev_app.test_client().post('/login?include_auth_token', json={
        "email": "user2@gmail.com",
        "password": "1234"
    })
    return res.json['response']['user']['authentication_token']


def test_get_user(client, auth_token):
    res = client.get('/api/users',
                     headers={
                         "Authentication-token": auth_token}
                     )
    assert res.status_code == 200
    assert res.json['username'] == "user2"


def test_post_task(client, auth_token):
    res = client.post('/api/tasks', json={
        "title": "Task1",
        "description": "description of task1"
    }, headers={
        "Authentication-token": auth_token
    })
    assert res.status_code == 201


def test_get_task(client, auth_token):
    res = client.get('/api/tasks/1', headers={
        "Authentication-token": auth_token
    })
    assert res.status_code == 200
