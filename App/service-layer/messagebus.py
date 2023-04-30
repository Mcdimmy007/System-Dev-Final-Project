from typing import Dict, List, Type
from uuid import uuid4

from cryptography.fernet import Fernet
from allocation.domain import commands, events


class ChatroomService:
    def __init__(
        self,
        message_bus: MessageBus,
        encryption_key: bytes,
    ):
        self.message_bus = message_bus
        self.encryption_key = encryption_key
        self.chatrooms: Dict[str, Dict[str, List[str]]] = {}

    def create_chatroom(self, chatroom_id: str, user_id: str):
        command = commands.CreateChatroom(chatroom_id=chatroom_id, user_id=user_id)
        self.message_bus.handle(command)

    def join_chatroom(self, chatroom_id: str, user_id: str):
        command = commands.JoinChatroom(chatroom_id=chatroom_id, user_id=user_id)
        self.message_bus.handle(command)

    def leave_chatroom(self, chatroom_id: str, user_id: str):
        command = commands.LeaveChatroom(chatroom_id=chatroom_id, user_id=user_id)
        self.message_bus.handle(command)

    def send_message(self, chatroom_id: str, sender_id: str, recipient_id: str, message: str):
        command = commands.SendMessage(chatroom_id=chatroom_id, sender_id=sender_id, recipient_id=recipient_id, message=message)
        self.message_bus.handle(command)

    def handle_chatroom_created(self, event: events.ChatroomCreated):
        self.chatrooms[event.chatroom_id] = {event.user_id: []}

    def handle_user_joined_chatroom(self, event: events.UserJoinedChatroom):
        self.chatrooms[event.chatroom_id][event.user_id] = []

    def handle_user_left_chatroom(self, event: events.UserLeftChatroom):
        self.chatrooms[event.chatroom_id].pop(event.user_id, None)

    def handle_message_sent(self, event: events.MessageSent):
        chatroom = self.chatrooms[event.chatroom_id]
        for user_id, messages in chatroom.items():
            if user_id == event.recipient_id or user_id == event.sender_id:
                encrypted_message = self.encrypt_message(event.message)
                messages.append(encrypted_message)

    def encrypt_message(self, message: str) -> str:
        fernet = Fernet(self.encryption_key)
        return fernet.encrypt(message.encode()).decode()

    def decrypt_message(self, encrypted_message: str) -> str:
        fernet = Fernet(self.encryption_key)
        return fernet.decrypt(encrypted_message.encode()).decode()
