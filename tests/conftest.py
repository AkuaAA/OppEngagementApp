import os
import tempfile

import pytest
from website import create_app
from website.models import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'test_data.sql'), 'rb') as f:
    _test_data_sql = f.read().decode('utf8')

@pytest.fixture
def test_app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_test_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def test_client(test_app):
    return test_app.test_client()

@pytest.fixture
def test_runner(test_app):
    return test_app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(test_client):
    return AuthActions(test_client)