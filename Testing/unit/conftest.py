from app import app, db
from app.models import User, Message
from sqlalchemy import create_engine
import unittest
import datetime

class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation(self):
        user = User(username='testuser', password='testpassword')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)

    def test_message_creation(self):
        user1 = User(username='testuser1', password='testpassword1')
        user2 = User(username='testuser2', password='testpassword2')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        message = Message(content='testmessage', sender_id=user1.id, recipient_id=user2.id, timestamp=datetime.datetime.utcnow())
        db.session.add(message)
        db.session.commit()
        self.assertIsNotNone(message.id)

if __name__ == '__main__':
    unittest.main()
