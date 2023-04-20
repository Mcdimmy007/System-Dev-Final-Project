import pytest
from App import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_registration_and_login(client):
    # Test user registration
    response = client.post('/register', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert b'Account created successfully!' in response.data

    # Test user login
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert b'Welcome, testuser!' in response.data
