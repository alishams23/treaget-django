from rest_framework import serializers
from .models import *



class User_serializer(serializers.ModelSerializer):
    def getFullName(self, obj):
            return f"{obj.first_name + ' ' + obj.last_name}"
    get_full_name = serializers.SerializerMethodField("getFullName")
    class Meta:
        model = User
        fields = ['username','get_full_name','image']


class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model=ImageHeader
        fields="__all__"
        
        
class FileSerializers(serializers.ModelSerializer):
    class Meta:
        model=FileModel
        fields="__all__"


class BlogSerializers(serializers.ModelSerializer):
    def like_author(self, obj):
        user = None
        try:
            user = self.context.get("request").user
        except:
            print("error :request forward")
        if user in obj.like.all():
            return True
        else:
            return False
    likeAuthor = serializers.SerializerMethodField("like_author")
    like_count = serializers.IntegerField(
        source='like.count',
        read_only=True
    )
    imageBlog = ImageSerializers()
    file= FileSerializers(many=True)
    author= User_serializer()
    class Meta:
        model=Blog
        fields=["title","body","file","imageBlog","id",'author','like_count','likeAuthor']

class BlogCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields=["title","body","file","imageBlog",'author']

class ImageCreateSerializers(serializers.ModelSerializer):
   
    class Meta:
        model=ImageHeader
        fields=["title_for_photo","photo"]



class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"


class BlogUpdateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=Blog
        fields=["title","body",]
