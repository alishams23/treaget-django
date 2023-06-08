from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .filterset_class import *
from django_filters import rest_framework as filterSpecial  
from rest_framework import filters
from api.pagination import MyPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status





# Create your views here.

class SkillsList(generics.ListAPIView):
    serializer_class = SkillsSerializer
    queryset = Skills.objects.all()
    permission_classes = (AllowAny, )
     
class AddOptionService(generics.CreateAPIView):
    queryset = ServiceOptionMain.objects.all()
    serializer_class = ServiceFacilitiesSerializers
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class ServiceListApi(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class= ServiceSerializers
    def get_queryset(self):
        return Services.objects.filter(author=User.objects.get(username=self.kwargs.get('username'))).order_by("-pk")


#TODO: unused api
class ServiceSearchApi(generics.ListAPIView):
    queryset = Services.objects.all()
    serializer_class= ServiceSerializers
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,filterSpecial.DjangoFilterBackend]
    filterset_class = ServiceFilter
    ordering_fields  = ['price',"hour"]
    search_fields = ["specialName",]
    pagination_class= MyPagination


class DestroyServiceApi(generics.DestroyAPIView):
    serializer_class = ServiceSerializers
    def get_queryset(self):
        return Services.objects.filter(author=self.request.user,pk=self.kwargs.get('pk'))




class AddService(generics.CreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializers
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



#send data ?username=admin 
class timelineRetrieveApiView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = TimeLineSerializers
    def get_queryset(self):
        return Timeline.objects.filter(person__username=self.request.GET['username']).order_by("pk")


class timelineCreateApi(generics.CreateAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimeLineSerializers
    def perform_create(self, serializer):
        serializer.save(person=self.request.user)


        
class timelineDeleteApi(APIView):
    def delete(self, request, pk):
        timelineInstance=Timeline.objects.get(pk=pk)
        if timelineInstance.person == request.user:
            timelineInstance.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
