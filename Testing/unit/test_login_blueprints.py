import pytest
from flask import Flask, session
from app.login.login_form import LoginForm

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test_secret_key'
    app.register_blueprint(login_blueprints)

    with app.test_client() as client:
        with app.app_context():
            yield client

def test_login(client):
    # Ensure that the login page is accessible
    response = client.get('/login')
    assert response.status_code == 200

    # Ensure that a successful login redirects to the home page
    form = LoginForm()
    form.email.data = 'testuser@test.com'
    form.password.data = 'test_password'
    response = client.post('/login', data=form.data)
    assert response.headers['Location'] == 'http://localhost/'

    # Ensure that session is set with user_id
    with client.session_transaction() as sess:
        assert sess['user_id'] is not None

def test_logout(client):
    # Ensure that the logout page redirects to the login page
    response = client.get('/logout', follow_redirects=True)
    assert response.headers['Location'] == 'http://localhost/login'
