from app.signup.signup_blueprints import load_user
from app.signup.signup_models import User, db
from flask import url_for
import pytest

@pytest.fixture(scope='module')
def new_user():
    user = User(name='test_user', email='test_user@example.com')
    user.set_password('test_password')
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()

def test_signup_page(client):
    # Test GET request to signup page
    response = client.get('/signup')
    assert response.status_code == 200
    assert b'Sign up for a user account.' in response.data

    # Test POST request with valid form data
    response = client.post('/signup', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    })
    assert response.status_code == 302  # Redirect to home page after successful signup

    # Test POST request with existing user email
    response = client.post('/signup', data={
        'name': 'Test User',
        'email': 'test_user@example.com',
        'password': 'password',
        'confirm_password': 'password'
    })
    assert b'A user already exists with that email address.' in response.data

def test_load_user(new_user):
    # Test user loader function with valid user id
    user = load_user(new_user.id)
    assert user == new_user

    # Test user loader function with invalid user id
    user = load_user(999)
    assert user is None

def test_unauthorized_handler(client):
    # Test unauthorized access to protected route
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == url_for('login_blueprints.login')
