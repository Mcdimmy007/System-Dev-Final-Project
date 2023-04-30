from flask import Flask, jsonify, request
from chatroom_service import ChatroomService, ChatroomError

app = Flask(__name__)

# create an instance of the chatroom service
chatroom_service = ChatroomService()

@app.route('/create-room', methods=['POST'])
def create_room():
    """
    Endpoint to create a new chatroom.
    Expects a JSON payload with the following structure:
    {
        "name": "name_of_chatroom",
        "usernames": ["username1", "username2"]
    }
    """
    data = request.get_json()
    name = data['name']
    usernames = data['usernames']
    try:
        chatroom = chatroom_service.create_chatroom(name, usernames)
        return jsonify(chatroom.serialize()), 201
    except ChatroomError as e:
        return str(e), 400

@app.route('/rooms/<chatroom_id>/messages', methods=['GET', 'POST'])
def room_messages(chatroom_id):
    """
    Endpoint to get or post messages in a chatroom.
    If the method is GET, returns all messages in the chatroom.
    If the method is POST, expects a JSON payload with the following structure:
    {
        "username": "username",
        "message": "message_text"
    }
    """
    if request.method == 'GET':
        try:
            messages = chatroom_service.get_chatroom_messages(chatroom_id)
            return jsonify([msg.serialize() for msg in messages]), 200
        except ChatroomError as e:
            return str(e), 404
    elif request.method == 'POST':
        data = request.get_json()
        username = data['username']
        message = data['message']
        try:
            chatroom_service.post_chatroom_message(chatroom_id, username, message)
            return '', 201
        except ChatroomError as e:
            return str(e), 404

if __name__ == '__main__':
    app.run(debug=True)
