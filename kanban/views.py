from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models.query_utils import Q
from .models import *
from rest_framework import generics
from .serializers import *



# Create your views here.
class Kanban_api(generics.ListAPIView):
    serializer_class = KanbanSerializers
    def get_queryset(self):
        return Kanban.objects.filter(Q(id = self.kwargs["pk"]) & (Q(members=self.request.user) | Q(observer=self.request.user)))


class KanbanListDestroyApi(generics.DestroyAPIView):
    serializer_class = KanbanListSerializers
    def get_queryset(self):
        # check kanban author
        data = Kanban.objects.get(lists__id=self.kwargs.get('pk'))
        if data.members.filter(id = self.request.user ).exists() :
            return KanbanList.objects.filter(pk=self.kwargs.get('pk'))

class KanbanListItemCreateApi(generics.CreateAPIView):
    queryset=KanbanListItem.objects.all()
    serializer_class = KanbanListItemSerializers
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    

class KanbanListItemCreateApi(generics.CreateAPIView):
    queryset=KanbanListItem.objects.all()
    serializer_class = KanbanListItemSerializers
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class KanbanListItemDestroyApi(generics.DestroyAPIView):
    serializer_class = KanbanListItemSerializers
    def get_queryset(self):
        list_object = KanbanList.objects.get(items__id=self.kwargs.get('pk'))
        kanban_object= Kanban.objects.get(lists__id=list_object)
        if kanban_object.members.filter(id = self.request.user ).exists()  :
            return KanbanListItem.objects.filter(pk=self.kwargs.get('pk'))


