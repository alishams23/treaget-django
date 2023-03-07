from rest_framework import serializers
from .models import *
from api.serializers import UserLessInformationSerializers
from django.db.models.query_utils import Q



class MessageSerializer(serializers.ModelSerializer):
    def username_function(self,obj):
        return f"{obj.author.username}"
    username = serializers.SerializerMethodField("username_function")
    def read_function(self,obj):
        return f"{obj.read}"
    read = serializers.SerializerMethodField("read_function")
    class Meta:
        model = Message
        fields= ['username','content', 'created_at','__str__','id','read']

class ChatSerializer(serializers.ModelSerializer):
    def contact_function(self, obj):
        try:
            user = self.context.get("request").user
            for object in obj.members.all():
                if object != user:
                    return UserLessInformationSerializers(object, read_only=True ,many= False).data
        except:
            return "error"
        
    def unread_function(self, obj):
        user = self.context.get("request").user
        return Message.objects.filter(Q(related_chat = obj) & Q(read = False) & ~Q(author=user)).count()

      
        
    contact = serializers.SerializerMethodField("contact_function")
    unread = serializers.SerializerMethodField("unread_function")
    class Meta:
        model = Chat
        fields= "__all__"

