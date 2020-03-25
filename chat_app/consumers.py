import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message


@database_sync_to_async
def create_message(user, m_type, msg):
    return Message.objects.create(
            username=user,
            message_type=m_type,
            message=msg
        )


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = 'general_chat'
        self.chat_username = self.scope["url_route"]["kwargs"]["chat_user"]

    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        msg = await create_message(self.chat_username, 'notification', f'"{self.chat_username}" was just added to a chat!')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': msg.message_type,
                'message': msg.message,
                'time': msg.timestamp.strftime('%Y-%m-%d'),
                'username': msg.username
            }
        )
        await self.accept()

    async def disconnect(self, close_code):
        msg = await create_message(self.chat_username, 'notification', f'"{self.chat_username}" just left chat...')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': msg.message_type,
                'message': msg.message,
                'time': msg.timestamp.strftime('%Y-%m-%d'),
                'username': msg.username
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = await create_message(self.chat_username, 'chat_message', text_data_json['message'])
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': msg.message_type,
                'message': msg.message,
                'time': msg.timestamp.strftime('%Y-%m-%d'),
                'username': msg.username
            }
        )

    async def notification(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'time': event['time'],
            'username': event['username']
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'time': event['time'],
            'username': event['username']
        }))