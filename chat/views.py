from django.shortcuts import render
from rest_framework import generics
from .serializers import ChatSerializer
from .models import Chat,Message
from account.models import User
from django.shortcuts import get_object_or_404
from rest_framework import filters


# Create your views here.


class ChatList(generics.ListAPIView):
    serializer_class = ChatSerializer
    def get_queryset(self):
        return [ x for x in  Chat.objects.filter(members = self.request.user).order_by('updated_at') if Message.objects.filter(related_chat = x.id).exists()]

class Search(generics.ListAPIView):
    serializer_class = ChatSerializer
    filter_backends = [filters.SearchFilter,]
    search_fields = ["members__username","members__first_name","members__last_name"]

    def get_queryset(self):
        return Chat.objects.filter(members = self.request.user).order_by('updated_at')


class ChatRetrieve(generics.RetrieveAPIView):
    serializer_class = ChatSerializer
    def get_queryset(self):
        user= User.objects.get(username = self.kwargs.get('username'))
        result = Chat.objects.filter(members__in = [user.id]).filter(members__in = [self.request.user.id])
        if len(result) == 0 :
            result = Chat.objects.create(room_name = f'{user}_{self.request.user}')
            result.members.set([user.id,self.request.user.id])
            result.save()
        else : result = result[0]
        return result
    def get_object(self):
        queryset = self.get_queryset()
        return queryset