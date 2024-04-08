import sqlite3
import pytest
from website.models import get_db
from website import construct_app

def test_get_close_db():
    app = construct_app({
        'TESTING': True,
        'DATABASE': 'sqlite:///:memory:',
    })

    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.session.execute('SELECT 1')

    assert 'closed' in str(e.value)
    
    def test_init_db_command(runner, monkeypatch):
        class Recorder(object):
            called = False
    
        def fake_init_db():
            Recorder.called = True
    
        monkeypatch.setattr('website.db.init_db', fake_init_db)
        result = runner.invoke(args=['init-db'])
        assert 'Initialized' in result.output
        assert Recorder.called

def test_login_logout(auth, test_client):
    # Test that we can login
    response = auth.login()
    assert response.status_code == 200
    assert b'Logged in successfully.' in response.data

    # Test that we can logout
    response = auth.logout()
    assert response.status_code == 200
    assert b'Logged out successfully.' in response.data

