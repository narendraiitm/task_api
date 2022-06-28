import pytest
from main import test_app


@pytest.fixture
def client():
    return test_app.test_client()


def test_get_task(client):
    res = client.get('/api/tasks/5')
    assert res.status_code == 200


def test_post_task(client):
    res = client.post('/api/tasks/5')
    assert res.status_code == 404
