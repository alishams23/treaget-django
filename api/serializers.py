
from typing import Counter
from django.core.exceptions import ValidationError
from django.db.models import fields, manager
from django.http import request
from rest_framework import serializers
from account.models import Message, Notification, User
from main.models import *
from rest_framework.validators import UniqueValidator
from main.views import Contact
from wallet.models import *

from profile_items.serializers import ServiceFacilitiesSerializers , ServiceSerializers


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


class CashSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("cash",)


class AcceptSerializers(serializers.ModelSerializer):
    author = UserLessInformationSerializers(required=False,read_only=True)

    class Meta:
        model = Accept
        fields = "__all__"


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["title"]


class ProductsSerializer (serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ['pk', "title"]
        
        
class ContactSerializer (serializers.ModelSerializer):
    class Meta:
        model = contact
        fields = "__all__"


class PictureSerializer(serializers.ModelSerializer):
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
    like = UserLessInformationSerializers(many=True, required=False)
    author = UserLessInformationSerializers(required=False,read_only=True)
    like_count = serializers.IntegerField(
        source='like.count',
        read_only=True
    )
    category = ProductsSerializer(many=True, required=False)

    class Meta:
        model = Picture
        exclude = ["Visitor", "position", "status"]
        # extra_kwargs = {"category": {"required": False, "allow_null": True}}


class RequestSerializer(serializers.ModelSerializer):
    # def get_author(self, obj):
    #     return {
    #         "username": obj.author.username,
    #         "first_name": obj.author.first_name,
    #         "last_name": obj.author.last_name,
    #         "full_name": f"{obj.author.first_name + ' ' + obj.author.last_name}"
    #     }
    subcategories = AcceptSerializers(many=True, required=False,read_only=True)
    author = UserLessInformationSerializers(required=False,read_only=True)

    class Meta:
        model = Request
        fields = '__all__'

class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rules
        fields = '__all__'





class MessageSerializers(serializers.ModelSerializer):
    author = UserLessInformationSerializers(required=False,read_only=True)
    receiver = UserLessInformationSerializers()

    class Meta:
        model = Message
        fields = "__all__"



  



class UserSettingSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "bio", "image", "category")


class UserSerializers(serializers.ModelSerializer):
    def getFullName(self, obj):
        return f"{obj.first_name + ' ' + obj.last_name}"

    def position_page(self, obj):
        counter = 1
        for category in obj.category.all() :
            if category.position == 0 :
                counter = 0
        if len(obj.category.all()) == 0 :
            counter = 0
        return  counter

    def position_page(self, obj):
        counter = 1
        for category in obj.category.all() :
            if category.position == 0 :
                counter = 0
        if len(obj.category.all()) == 0 :
            counter = 0
        return  counter
    
    def post_picture(self, obj):
        list_result = []
        list_data = Picture.objects.filter(author__username=obj.username)[0:7]
        for data in list_data:
            serializer = PictureSerializer(data,context={'request': self.context.get("request")})
            list_result.append(serializer.data)
        return   list_result

    def visitor_count(self, obj):
        user = None
        try:
            user = self.context.get("request").user
            return obj.numberVisitors.count()
        except:
            print("error :request forward")
            return 0
        
    def is_followed_def (self , obj):
        try:
            user = self.context.get("request").user
            if user in obj.followers.all():
                return True
        except:
            print("error :request forward")
        
        return False
    def numberFollow(self,obj):
        return {"followers":obj.followers.count(),"following":obj.following.count()}
    followers = UserLessInformationSerializers(many=True)
    following = UserLessInformationSerializers(many=True)
    postPicture=serializers.SerializerMethodField("post_picture")
    category = CategorySerializers(many=True)
    visitorCount = serializers.SerializerMethodField("visitor_count")
    get_full_name = serializers.SerializerMethodField("getFullName")
    is_followed = serializers.SerializerMethodField("is_followed_def")
    position_user = serializers.SerializerMethodField("position_page")
    number_follow = serializers.SerializerMethodField("numberFollow")
    

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "bio", "image", "category", "followers", "following",
                  "isVerified", "ServiceProvider", "is_special_user", "pk", "visitorCount", "get_full_name","position_user","is_followed","postPicture","number_follow")


class UsersRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ("id",'username', 'password', "ServiceProvider"
                  , 'first_name', 'last_name', "email",'phone_number')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_password(self, validated_data):
        if len(validated_data) < 8:
            raise ValidationError("password need to be more than 8 character")
        return validated_data

    def validate_username(self, validated_data):
        username = validated_data
        special_characters = "!@#$%^&*()-+?=,<>/"
        if any(c in special_characters for c in username):
            raise ValidationError("Username must don't have character")
        return username.lower()
    
    def validate_phone_number(self, validated_data):
        if validated_data:
            phoneCheck = User.objects.filter(phone_number=validated_data).exists()
            if phoneCheck:
                raise ValidationError("phone_number must don't have character")
        return validated_data


class NotificationSerializers(serializers.ModelSerializer):
    receiver = UserLessInformationSerializers()
    user = UserLessInformationSerializers()

    class Meta:
        model = Notification
        fields = "__all__"


class PaymentWalletSerializers(serializers.ModelSerializer):
    class Meta:
        model = PaymentWalletB
        fields = "__all__"


class SubsetTrelloSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubsetTrello
        fields = "__all__"


class TrelloSerializers(serializers.ModelSerializer):
    subsetTrello = SubsetTrelloSerializers(many=True, required=False)

    class Meta:
        model = Trello
        fields = "__all__"


class SafePaymentSerializer(serializers.ModelSerializer):
    receiver = UserLessInformationSerializers()
    sender = UserLessInformationSerializers()

    class Meta:
        model = SafePayment
        fields = "__all__"


class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = "__all__"
    def to_representation(self, instance):
        self.fields['safePayment'] =  SafePaymentSerializer(required=False,read_only=True)
        return super(DisputeSerializer, self).to_representation(instance)


class OrderSerializers(serializers.ModelSerializer):
    author = UserLessInformationSerializers(read_only=True)
    designer = UserLessInformationSerializers(read_only=True)
    safePayment = SafePaymentSerializer(read_only=True)
    accept=serializers.BooleanField(read_only=True)

    class Meta:
        model = OrderUser
        fields = "__all__"

    def to_representation(self, instance):
      
        self.fields['optionsServiceMain'] =  ServiceFacilitiesSerializers(many=True,required=False,read_only=True)
        
        self.fields['service'] =  ServiceSerializers(required=False,read_only=True)
        return super(OrderSerializers, self).to_representation(instance)


    def validate(self, data):
        service = data.get('service', None)
        title = data.get('title', None)
        accept = data.get('accept', None)
        if not service and not title:
            raise serializers.ValidationError("at least one date input (service,title) required.")
        if accept in [True,False]:
            raise serializers.ValidationError("accept need to be none")
        return data


class SpamSerializers(serializers.ModelSerializer):
    author = UserLessInformationSerializers(required=False,read_only=True)
    class Meta:
        model = Spam
        fields = "__all__"
        
    def to_representation(self, instance):
        self.fields['picture'] =  PictureSerializer(required=False,read_only=True)
        self.fields['request'] =  RequestSerializer(required=False,read_only=True)
        self.fields['user'] =  UserSerializers(required=False,read_only=True)
        return super(SpamSerializers, self).to_representation(instance)