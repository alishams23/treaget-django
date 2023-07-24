from django.shortcuts import render
from rest_framework.response import Response
from blog.filtersets import BlogFilter
from .models import *
from .serializers import *
from rest_framework import generics,status
from rest_framework import filters
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from .pagination import *
from django_filters import rest_framework as filterSpecial  
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


# Create your views here.
class BlogList(ListAPIView):
    permission_classes = (AllowAny, )
    filter_backends = [filters.SearchFilter,]
    serializer_class =BlogSerializers
    queryset = Blog.objects.all()
    pagination_class= Pagination_one
    search_fields = ['title','body']


class SearchListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,filterSpecial.DjangoFilterBackend ]
    pagination_class = Pagination_one
    filterset_class = BlogFilter
    
    ordering = ["-pk"]
    search_fields = ['title', ]


class BlogRetrieveCategory(ListAPIView):
    serializer_class = BlogSerializers

    def get_queryset(self ):
        id = self.kwargs.get('pk', 'Default Value if not there')
        data = Blog.objects.filter(category__pk=id)
        return data
    pagination_class = Pagination_one
    
class BlogRetrieve(RetrieveAPIView):
    serializer_class = BlogSerializers
    queryset = Blog.objects.all()
    

    


class ListCategory(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = MainCategorySerializer


class CreateBlog(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateSerializers

    def create(self, request, *args, **kwargs):
        # Check if the user is a superuser
        if not request.user.is_superuser and  not request.user.is_author:
            return Response({'error': 'You do not have permission to create blogs.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        response_data['id'] = instance.id
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

class CreateImage(generics.CreateAPIView):
    queryset= ImageHeader.objects.all()
    serializer_class = ImageCreateSerializers
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = serializer.data
        response_data['id'] = instance.id
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
    

class AddLikeView(APIView):
    def get(self, request):
        # get data with ?Picture=pk in url
        blogPk = self.request.GET['id']
        blogInstance = Blog.objects.get(pk=blogPk)
        if request.user not in blogInstance.like.all():
            blogInstance.like.add(request.user)   #add like
            # TODO : check this result
            return Response(status=status.HTTP_200_OK)
        else:   
            blogInstance.like.remove(request.user)   #remove like
            return Response(status=status.HTTP_200_OK)


    
class BlogRemove(DestroyAPIView):
    serializer_class = BlogSerializers
    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user,pk=self.kwargs.get('pk'))

    

class BlogUpdate(generics.UpdateAPIView):
    serializer_class = BlogUpdateSerializer
    queryset= Blog.objects.all()
    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user , id= self.kwargs.get('pk'))
       