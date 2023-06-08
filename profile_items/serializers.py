
from rest_framework import serializers
from .models import *


class UserLessInformationSerializers(serializers.ModelSerializer):
    def get_author(self, obj):
        return  f"{obj.first_name + ' ' + obj.last_name}" 
    def position_page(self, obj):
        counter = 1
        for category in obj.category.all() :
            if category.position == 0 :
                counter = 0
        if len(obj.category.all()) == 0 :
            counter = 0
        return  counter
    def getFullName(self, obj):
            return f"{obj.first_name + ' ' + obj.last_name}"
    def is_followed_def (self , obj):
        try:
            user = self.context.get("request").user
            if user in obj.followers.all():
                return True
        except:
            #error :request forward
            print("")
        
        return False
    is_followed = serializers.SerializerMethodField("is_followed_def")
    full_name = serializers.SerializerMethodField("get_author")
    position_user = serializers.SerializerMethodField("position_page")
    get_full_name = serializers.SerializerMethodField("getFullName")
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name","full_name",
                  "image", "ServiceProvider","position_user","get_full_name",'is_followed',"bio")


class SkillsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"
        
  
class ServiceSubsetSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServiceSubset
        fields = "__all__"


class ServiceFacilitiesSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServiceOptionMain
        fields = "__all__"


class ServiceSerializers(serializers.ModelSerializer):
    author = UserLessInformationSerializers(required=False,read_only=True)

    class Meta:
        model = Services
        fields = "__all__"

    def to_representation(self, instance):
        self.fields['serviceOption'] =  ServiceFacilitiesSerializers(many=True,required=False,read_only=True)
        return super(ServiceSerializers, self).to_representation(instance)


    def validate(self, data):
       
        specialName = data.get('specialName', None)
        if not specialName:
            raise serializers.ValidationError("at least one date input required.")
        return data
    

class TimeLineSerializers(serializers.ModelSerializer):
    person = UserLessInformationSerializers(required=False,read_only=True)
    
    class Meta:
        model = Timeline
        fields = "__all__"

    def validate(self, data):
        body = data.get('body', None)
        if  not body:
            raise serializers.ValidationError("body required.")
        return data

