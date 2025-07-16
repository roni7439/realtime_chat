import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import PrivetMassage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Access control for private chat
        if self.room_name.startswith("private_"):
            try:
                user1_id, user2_id = map(int, self.room_name.split("_")[1:])
                current_user_id = self.scope["user"].id
                if current_user_id not in (user1_id, user2_id):
                    await self.close()
                    return
            except Exception:
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
        message = data.get("message")
        sender_username = data.get("sender")

        if not message or not sender_username:
            return

        # Get sender and receiver
        try:
            sender = await self.get_user_by_username(sender_username)
            receiver = await self.get_receiver(sender.id)
        except User.DoesNotExist:
            await self.close()
            return

        # Save the message
        await self.save_message(sender, receiver, message)

        # Send the message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender_username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"]
        }))

    @database_sync_to_async
    def get_user_by_username(self, username):
        return User.objects.get(username=username)

    @database_sync_to_async
    def get_receiver(self, sender_id):
        parts = self.room_name.split("_")
        user_ids = [int(parts[1]), int(parts[2])]
        receiver_id = next(uid for uid in user_ids if uid != sender_id)
        return User.objects.get(id=receiver_id)

    @database_sync_to_async
    def save_message(self, sender, receiver, message):
        PrivetMassage.objects.create(
            sender=sender,
            receiver=receiver,
            body=message
        )
