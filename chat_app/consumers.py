import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import Message


@database_sync_to_async
def create_message(user, m_type, msg, mentioned):
    return Message.objects.create(
        user=user,
        message_type=m_type,
        message=msg,
        mentioned=mentioned
    )


@database_sync_to_async
def get_user(u_id):
    if not u_id:
        return None
    return get_user_model().objects.get(id=u_id)


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = 'general_chat'

    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        msg = await create_message(
            self.scope['user'], 'notification', f'"{self.scope["user"]}" was just added to a chat!', None
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': msg.message_type,
                'message': msg.message,
                'time': msg.timestamp.strftime('%Y-%m-%d %H:%M'),
                'username': msg.user.username
            }
        )
        await self.accept()

    async def disconnect(self, close_code):
        msg = await create_message(
            self.scope['user'], 'notification', f'"{self.scope["user"]}" just left chat...', None
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': msg.message_type,
                'message': msg.message,
                'time': msg.timestamp.strftime('%Y-%m-%d %H:%M'),
                'username': msg.user.username
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = await create_message(
            self.scope['user'],
            text_data_json['message_type'],
            text_data_json['message'],
            await get_user(text_data_json['mentioned'])
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': msg.message_type,
                'message': msg.message,
                'time': msg.timestamp.strftime('%Y-%m-%d %H:%M'),
                'username': msg.user.username,
                'mentioned': msg.mentioned.username if msg.message_type == 'mention' else None
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

    async def mention(self, event):
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'time': event['time'],
            'username': event['username'],
            'mentioned': event['mentioned']
        }))