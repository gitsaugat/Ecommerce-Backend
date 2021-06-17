from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import json


class CustomerSupportConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        self.username = self.user.username
        self.thread_name = 'with-{username}'.format(username=user.username)
        await self.channel_layer.group_add(
            self.thread_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.thread_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.thread_name,
            {
                'type': 'send_message',
                'message': data['message']
            }
        )

    async def send_message(self, event):

        message = event['message']

        await self.send(
            text_data=json.dumps({
                "message": message,
                "from": self.username
            })
        )
