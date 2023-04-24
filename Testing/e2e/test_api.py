import pytest
from App import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_registration_and_login(client):
    # Testing the user registration
    response = client.post('/register', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert b'Account created successfully!' in response.data

    # Testing the user login with valid credentials
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302  # redirect to dashboard
    assert b'Welcome, testuser!' in response.data

    # Testing user login with invalid credentials
    response = client.post('/login', data={'username': 'testuser', 'password': 'wrongpassword'})
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

    # Testing access to dashboard after login
    with client.session_transaction() as session:
        session['user_id'] = 1  # simulate user login
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Test User' in response.data  # assuming the registered user's name is Test User

    # Testing access to dashboard without login
    response = client.get('/dashboard')
    assert response.status_code == 302  # redirect to login page
    assert b'Please log in' in response.data
