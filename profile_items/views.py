from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .filterset_class import *
from django_filters import rest_framework as filterSpecial  
from rest_framework import filters
from api.pagination import MyPagination


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

#TODO: unused api
class DestroyServiceApi(generics.DestroyAPIView):
    serializer_class = ServiceSerializers
    def get_queryset(self):
        return Services.objects.filter(author=self.request.user,pk=self.kwargs.get('pk'))




class AddService(generics.CreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializers
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
