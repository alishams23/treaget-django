from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync 
from channels.db import database_sync_to_async
import json
from account.models import User , Message

# class chatConsumer(WebsocketConsumer):    
#     def connect(self):

#         self.accept()
#         self.user = self.scope["user"]
        
#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data=None, bytes_data=None):
#         self.send(text_data=text_data + " - Sent By Server")
#         message = Message(text=text_data,author=self.user)
#         message.save()

class chatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope["user"]
        self.group_name = f"chat_{self.user_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            text_data_json = json.loads(text_data)
            username = text_data_json['receiver']
            user_group_name = f"chat_{username}"
            # print(text_data_json["text"])
            # print(self.user_id)
            # print(username)
            userid =self.user_id
            receiver=await database_sync_to_async(User.objects.get)(username=username)
            await database_sync_to_async(Message(text=text_data_json["text"],author=userid,receiver=receiver).save)()
            
 
            await self.channel_layer.group_send(
                user_group_name,
                {
                    'type': 'chat_message',
                    'message': text_data
                }
            )

    async def chat_message(self, event):
        message = event['message']


        await self.send(text_data=message)

