from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .serializers import MessageSerializer
from .models import Message
from rest_framework.renderers import JSONRenderer
from account.models import User
from .models import *
from rest_framework.authtoken.models import Token




class ChatConsumer(WebsocketConsumer):
    
    def new_message(self, data):
        message = data['message']
        author =  self.user
        room_name_data = data['room_name']
        chat_model = Chat.objects.get(room_name=room_name_data)
        message_model = Message.objects.create(author=author , content=message, related_chat=chat_model)
        result = eval(self.message_serializer(message_model))
        self.send_to_chat_message(result)


    def read_message(self, data):
        message = Message.objects.get(id=data['message']) 
        if message.read == False and message.author != self.user:
            message.read = True
            message.save()
            async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {'type': 'chat_message',
                    "id" : message.id,
                    'command' : "read_message"
                    }  
                )


    def fetch_message(self, data):
        room_name_data = data['room_name']
        qs = Message.last_message(self, room_name_data)
        for item in qs : 
            if item.author != self.user and item.read == False:
                item.read = True
                item.save()
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {'type': 'chat_message',
                    "id" : item.id,
                    'command' : "read_message"
                    }  
                )

                

            
        message_json = self.message_serializer(qs)
        content = {
            
            "message" : eval(message_json),
            'command' : "fetch_message"
            
        }
        self.chat_message(content)


    def image(self, data):
       self.send_to_chat_message(data)


    def message_serializer(self, qs):
    
        serialized = MessageSerializer(qs, many=(lambda qs : True if (qs.__class__.__name__ == 'QuerySet') else False)(qs))
        content = JSONRenderer().render(serialized.data)
        return content
        
    

    
    def connect(self):
        self.user = Token.objects.get(key = self.scope['url_route']['kwargs']['token']).user 
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )    
        self.accept()

    commands = {
        
        "new_message": new_message,
        "read_message": read_message,
        "fetch_message": fetch_message,
        'img': image
    
    }
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    def receive(self, text_data):
        text_data_dict = json.loads(text_data)
        command = text_data_dict['command']
        
        self.commands[command](self, text_data_dict)
        
        
        
    def send_to_chat_message(self, message):
        
        command = message.get("command", None)
            
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'content': message['content'],
                'id':message['id'],
                'command':(lambda command : "read_message" if( command == "read_message") else "new_message")(command),
                'username' : message['username']
            }  
        )

    
    def chat_message(self, event):
       
        self.send(text_data=json.dumps(event))

class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_dict = json.loads(text_data)
        message = text_data_dict['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
