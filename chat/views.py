from django.shortcuts import render
from rest_framework import generics
from .serializers import ChatSerializer
from .models import Chat
from account.models import User
from django.shortcuts import get_object_or_404

# Create your views here.


class ChatList(generics.ListAPIView):
    serializer_class = ChatSerializer
    def get_queryset(self):
        return Chat.objects.filter(members = self.request.user).order_by('updated_at')
    
class ChatRetrieve(generics.RetrieveAPIView):
    serializer_class = ChatSerializer
    def get_queryset(self):
        user= User.objects.get(username = self.kwargs.get('username'))
        result = Chat.objects.filter(members__in = [user.id,self.request.user.id])
        if len(result) == 0 :
            result = Chat.objects.create(members=[user.id,self.request.user.id],room_name = f'{user}-{self.request.user}')
        else : result = result[0]
        return result
    def get_object(self):
        queryset = self.get_queryset()
        return queryset