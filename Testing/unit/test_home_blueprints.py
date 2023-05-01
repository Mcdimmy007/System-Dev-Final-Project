# test_home_blueprints.py

from app import create_app
from flask_socketio import SocketIOTestClient

def test_home_blueprints():
    app = create_app()
    app.config["SECRET_KEY"] = "secretkey"
    client = SocketIOTestClient(app, namespace="/")
    with app.test_client() as test_client:
        with client:
            # Test home route
            response = test_client.get("/")
            assert response.status_code == 302  # Expecting a redirect to login page

            # Login as a test user
            test_client.post("/login", data=dict(username="testuser", password="password"))

            # Test home route after login
            response = test_client.get("/")
            assert response.status_code == 200

            # Test room route before joining a room
            response = test_client.get("/room")
            assert response.status_code == 302  # Expecting a redirect to home page

            # Test creating a room
            client.emit("join_room", {"room": None, "name": "testuser", "create": True})
            response = client.get_received()
            assert len(response) == 1
            assert response[0]["name"] == "join_room_response"
            assert response[0]["args"][0]["success"] == True
            assert response[0]["args"][0]["room_code"] != None

            # Test joining a room
            client.emit("join_room", {"room": response[0]["args"][0]["room_code"], "name": "testuser2", "create": False})
            response = client.get_received()
            assert len(response) == 1
            assert response[0]["name"] == "join_room_response"
            assert response[0]["args"][0]["success"] == True

            # Test sending a message
            client.emit("send_message", {"data": "Hello, world!"})
            response = client.get_received()
            assert len(response) == 1
            assert response[0]["name"] == "message"
            assert response[0]["args"][0]["name"] == "testuser"
            assert response[0]["args"][0]["message"] == "Hello, world!"

            # Test leaving a room
            client.emit("leave_room")
            response = client.get_received()
            assert len(response) == 1
            assert response[0]["name"] == "leave_room_response"
            assert response[0]["args"][0]["success"] == True
            
