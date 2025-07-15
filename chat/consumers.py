import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import PrivetMassage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Validate that the connected user is allowed in this private chat
        if self.room_name.startswith("private_"):
            parts = self.room_name.split("_")
            try:
                user1_id = int(parts[1])
                user2_id = int(parts[2])
            except (IndexError, ValueError):
                await self.close()
                return

            current_user_id = self.scope["user"].id
            if current_user_id not in (user1_id, user2_id):
                await self.close()
                return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_username = data['sender']
        receiver_username = await self.get_receiver(sender_username)

        await self.save_message(sender_username, receiver_username, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))

    @database_sync_to_async
    def get_receiver(self, sender_username):
        # Parse room to find the other user
        parts = self.room_name.split("_")
        user_ids = [int(parts[1]), int(parts[2])]
        sender = User.objects.get(username=sender_username)
        receiver_id = [uid for uid in user_ids if uid != sender.id][0]
        return User.objects.get(id=receiver_id)

    @database_sync_to_async
    def save_message(self, sender_username, receiver, message):
        sender = User.objects.get(username=sender_username)
        PrivetMassage.objects.create(
            sender=sender,
            receiver=receiver,
            body=message
        )
    