import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .utils import chat_with_bot
from .chat_history import get_message_history
from .models import FinanceDiary
from .serializers import FinanceDiarySerializer



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.child_pk = self.scope['url_route']['kwargs']['child_pk']
        self.room_group_name = f'chat_{self.child_pk}'

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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        # Process the message
        response = await self.chat_with_bot_async(message, user.id)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': response
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def chat_with_bot_async(self, message, user_id):
        return chat_with_bot(message, user_id)

    @database_sync_to_async
    def save_finance_diary(self, data, user):
        finance_diary = FinanceDiary(
            diary_detail=data.get('diary_detail'),
            today=data.get('today'),
            category=data.get('category'),
            transaction_type=data.get('transaction_type'),
            amount=data.get('amount'),
            child=user,
            parent=user.parents
        )
        finance_diary.save()
        return FinanceDiarySerializer(finance_diary).data