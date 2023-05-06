# pylint: disable=redefined-outer-name
import pytest
from app import create_app, db


@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for each test session."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def auth_client(client):
    """A test client authenticated with a test user."""
    with client.session_transaction() as session:
        # Here you can mock a logged-in user
        session["user_id"] = 1
        session["_fresh"] = True

    return client
