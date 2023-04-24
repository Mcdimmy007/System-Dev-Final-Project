from App import app, db
from App.models import User, Message
from sqlalchemy import create_engine
import pytest
import datetime
from ModelsTestCase import ModelsTestCase

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    user1 = User(username='testuser1', password='testpassword1')
    user2 = User(username='testuser2', password='testpassword2')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    yield db 

    db.drop_all()

def test_user_creation(init_database):
    user = User(username='testuser', password='testpassword')
    init_database.session.add(user)
    init_database.session.commit()
    assert user.id is not None

def test_message_creation(init_database):
    user1 = User.query.filter_by(username='testuser1').first()
    user2 = User.query.filter_by(username='testuser2').first()
    message = Message(content='testmessage', sender_id=user1.id, recipient_id=user2.id, timestamp=datetime.datetime.utcnow())
    init_database.session.add(message)
    init_database.session.commit()
    assert message.id is not None

def test_models():
    suite = unittest.TestSuite()
    suite.addTest(ModelsTestCase('test_user_creation'))
    suite.addTest(ModelsTestCase('test_message_creation'))
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    assert result.wasSuccessful()
