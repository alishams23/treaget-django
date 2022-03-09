from main.views import deleteDuplicate
from django.http import request
from rest_framework.authtoken.models import Token
from wallet.views import wallet
from rest_framework.filters import OrderingFilter
from api import filterset_class
from api.filterset_class import *
from extensions.notification import notificationAdd
from account.models import Message, Notification
from itertools import chain
import json
from django.utils.html import json_script
from rest_framework import status
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.query_utils import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics
from main.models import *
from .serializers import *
from rest_framework import viewsets
from django_filters import rest_framework as filterSpecial  
from rest_framework import filters
from api.pagination import MyPagination
from wallet.models import *
import random
import requests
# Create your views here.


    
class AddLikeView(APIView):
    def get(self, request):
        # get data with ?Picture=pk in url
        picturePk = self.request.GET['Picture']
        pictureInstance = Picture.objects.get(pk=picturePk)
        if request.user not in pictureInstance.like.all():
            request.user.like.add(pictureInstance)
            pictureInstance.like.add(request.user)   #add like
            # TODO : check this result
            if request.user != pictureInstance.author:
                notificationAdd(receiver=pictureInstance.author, title="پست شما را لایک کرد", url=f"/account/post/{pictureInstance.pk}/"
                    , user=request.user)
            return Response(status=status.HTTP_200_OK)
        else:   
            request.user.like.remove(pictureInstance)
            pictureInstance.like.remove(request.user)   #remove like
            return Response(status=status.HTTP_200_OK)

    
class Code_check(APIView):
    def get(self, request):
        code = self.request.GET['code']
        if str(request.user.verify_phone_code ) == str(code):
            userInstance= request.user
            userInstance.verify_phone = True
            userInstance.save()
            
            return Response(status=status.HTTP_200_OK)
        else:   
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    
class Send_code(APIView):
    def get(self, request):  
        if request.user.count_sms < 10 :
            userInstance= request.user
            userInstance.verify_phone_code = random.randint(10000, 99999) 
            userInstance.save()
            try:
                newURL = 'https://console.melipayamak.com/api/send/shared/1806bb276635474486b7c380b2b0fbcb'
                newHeaders = {'Content-type': 'application/json; utf-8', 'Accept': 'application/json'}
                newBody = {
                    "bodyId": 72447, 
                    "to": f"{request.user.phone_number}",
                    "args": [f"{request.user.verify_phone_code}"],
                    }
                response = requests.post( newURL , data = json.dumps(newBody) , headers = newHeaders)
                print( response.json())
                userInstance= request.user
                userInstance.count_sms += 1
                userInstance.save()
                return Response({"result":response.json()},status=status.HTTP_200_OK)
            except: 
                return Response(status=status.HTTP_410_GONE)
           
    
   

class HomeApiView(viewsets.ModelViewSet):
    def list(self, request):
        firstData = Picture.objects.filter(
        Q(author__id__in=request.user.following.all()) | Q(author=request.user)).order_by("-pk")
        secondData = Request.objects.filter(Q(author__id__in=request.user.following.all()) | Q(author=request.user)).order_by("-pk")
        result_list = sorted(
            chain(firstData, secondData),
            key=attrgetter('createdAdd'), reverse=True)
        if len(result_list) == 0 :
            result_list = Picture.objects.all().order_by("-pk")
        results = list()
        results_per_page = 5
        postnumber = self.request.GET['page']
        paginator = Paginator(result_list, results_per_page)
        try:
            result_list = paginator.page(int(postnumber))
        except PageNotAnInteger:
            result_list = paginator.page(1)
        except EmptyPage:
            result_list = []
        for entry in result_list:
            item_type = entry.__class__.__name__.lower()
            if isinstance(entry, Picture):
                serializer = PictureSerializer(entry,context={'request': request})
            if isinstance(entry, Request):
                serializer = RequestSerializer(entry,context={'request': request})
            data_dict = {'item': item_type, 'data': serializer.data}
            results.append(data_dict)
        return Response(results)


class PicturePostDestroyRetrive(generics.RetrieveDestroyAPIView):
    queryset = Picture.objects.all()
    serializer_class= PictureSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)



class RequestPostDestroyRetrive(generics.RetrieveDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class= RequestSerializer
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
    
    

class ExploreApiView (generics.ListAPIView):
    queryset = Picture.objects.filter(status="p").order_by("?")[0:25]
    serializer_class = PictureSerializer
    permission_classes = (AllowAny, )

class ExploreProjectApiView (generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    pagination_class = MyPagination
    permission_classes = (AllowAny, )
    
#send data ?username=admin 
class timelineRetrieveApiView(generics.ListAPIView):
    serializer_class = TimeLineserializers
    def get_queryset(self):
        return Timeline.objects.filter(person__username=self.request.GET['username']).order_by("pk")


class timelineCreateApi(generics.CreateAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimeLineserializers
    def perform_create(self, serializer):
        serializer.save(person=self.request.user)

class SpamCreateApi(generics.CreateAPIView):
    queryset = Spam.objects.all()
    serializer_class = SpamSerializers
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
class timelineDeleteApi(APIView):
    def delete(self, request, pk):
        timelineInstance=Timeline.objects.get(pk=pk)
        if timelineInstance.person == request.user:
            timelineInstance.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class MassageApi(APIView):

    def get(self, request):
        messages_User = Message.objects.filter(author=User.objects.get(username=request.GET["user"]),
                receiver=request.user,read=False).order_by('pk')
        listMessage=[]
        for  message in messages_User:
            message.read = True
            message.save()
            MessageSerializersInstance=MessageSerializers(message)
            listMessage.append(MessageSerializersInstance.data)
        return Response(listMessage,status=status.HTTP_200_OK)

    def put(self, request):
        # for data in request.data:
        # print(request.data)
        # data = json.loads(request.data) 
        String_2 = request.data["text"].strip()
        if String_2 != "":
            Message(text=request.data["text"],author=request.user,receiver=User.objects.get(username=request.data["receiver"])).save()
        return Response(status=status.HTTP_200_OK)

class AllMassageApi(APIView):
    def get(self, request):
        messages_User = Message.objects.filter(author=request.user,
                                               receiver=User.objects.get(username=request.GET["user"])) | Message.objects.filter(
                author=User.objects.get(username=request.GET["user"]), receiver=request.user).order_by('pk')
        listMessage=[]
        for  message in messages_User:
            if message.receiver == request.user :
                message.read = True
                message.save()
            MessageSerializersInstance=MessageSerializers(message)
            listMessage.append(MessageSerializersInstance.data)
        return Response(listMessage,status=status.HTTP_200_OK)

    def post(self, request):
        for data in request.data:
            data = json.loads(data) 
        Message(text=data["text"],author=request.user,receiver=User.objects.get(username=data["receiver"])).save()
        return Response(status=status.HTTP_200_OK)

class FollowUnfollowApi(APIView):
    def get(self,request,username):
            UserInstance = User.objects.get(username=username)
            if UserInstance in request.user.following.all() :
                request.user.following.remove(UserInstance)
                UserInstance.followers.remove(request.user)
            else:
                request.user.following.add(UserInstance)
                UserInstance.followers.add(request.user)
                notificationAdd(receiver=UserInstance, title="شما را دنبال کرد", url=f"/p/{request.user.username}/"
                                , user=request.user)
            return Response(status=status.HTTP_200_OK)


class ServiceListApi(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class= ServiceSerializers
    def get_queryset(self):
        return Service.objects.filter(author=User.objects.get(username=self.kwargs.get('username'))).order_by("-pk")



class ServiceSearchApi(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class= ServiceSerializers
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,filterSpecial.DjangoFilterBackend]
    filterset_class = ServiceFilter
    ordering_fields  = ['price',"hour"]
    search_fields = ["specialName","nameProduct__title"]
    pagination_class= MyPagination


class DestroyServiceApi(generics.DestroyAPIView):
    serializer_class = ServiceSerializers
    def get_queryset(self):
        return Service.objects.filter(author=self.request.user,pk=self.kwargs.get('pk'))



class UserSettingApi(generics.RetrieveUpdateAPIView):
    queryset=User.objects.all()
    serializer_class = UserSettingSerializers
    def get_object(self):
        queryset = self.get_queryset()
        obj = self.request.user
        return obj
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user:
            serializer = self.get_serializer(instance,data=request.data,partial=True)
            if serializer.is_valid() :
                self.perform_update(serializer)
                return Response(serializer.data)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class UserRetrieveApi(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    lookup_field="username"
    permission_classes = (AllowAny, )
    


class UserSearchListApi(generics.ListAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializers
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,]
    ordering_fields = ['?']
    filterset_fields = ['category__title']
    search_fields = ["username","first_name","last_name","bio"]
    pagination_class = MyPagination
    def get_queryset(self):
        if "image" in self.request.GET:return User.objects.filter(~Q(image=""))
        else : return User.objects.all()

    


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersRegisterSerializer
    permission_classes = (AllowAny, )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token, created = Token.objects.get_or_create(user_id=response.data["id"])
        response.data["token"] = str(token)
        return response

#TODO : inside serializer.save
class AddPostPictureApi(generics.CreateAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AddOptionService(generics.CreateAPIView):
    queryset = ServiceOptionMain.objects.all()
    serializer_class = ServiceFacilitiesSerializers
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AddService(generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AddRequestApi(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    def perform_create(self, serializer):
        serializer.save(author=self.request.user,subcategories=[])

class AddAcceptRequestApi(generics.CreateAPIView):
    queryset = Accept.objects.all()
    serializer_class = AcceptSerializers
    def perform_create(self, serializer):
        requestData = Request.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user != requestData.author:
            data = serializer.save(author=self.request.user)
            requestData.subcategories.add(data)
        


        
class DestroyRequestApi(generics.DestroyAPIView):
    serializer_class = RequestSerializer
    def get_queryset(self):
        return Request.objects.filter(author=self.request.user,pk=self.kwargs.get('pk'))

class RequestSearchApi(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter,filterSpecial.DjangoFilterBackend]
    filterset_class = RequestFilter
    search_fields = ["title","body","author__username","author__first_name","author__last_name"]
    ordering_fields = ["createdAdd"]
    pagination_class = MyPagination


class PictureSearchApi(generics.ListAPIView):
    queryset = Picture.objects.all().order_by("?")
    serializer_class = PictureSerializer
    # ordering_fields  = ["?"]
    filter_backends = [filters.SearchFilter,filterSpecial.DjangoFilterBackend]
    search_fields = ["alt","category__title"]
    pagination_class = MyPagination


class NotificationApi(generics.ListAPIView):
    serializer_class = NotificationSerializers
    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)
    pagination_class = MyPagination


class CashApi(generics.ListAPIView):
    serializer_class = CashSerializers
    def get_queryset(self):
        return [self.request.user]


class PaymentWalletApi(generics.ListAPIView):
    def get_queryset(self):
        return PaymentWalletB.objects.filter(user=self.request.user)
    serializer_class = PaymentWalletSerializers



class favoritesApi(generics.ListAPIView):
    def get_queryset(self):
        return User.objects.get(username=self.kwargs.get('username')).like.all()
    serializer_class = PictureSerializer


class TrelloApi(generics.ListAPIView):
    serializer_class = TrelloSerializers
    def get_queryset(self):
        return Trello.objects.filter(Q(forSafePayment__pk = self.kwargs["pk"]) & (Q(forSafePayment__receiver=self.request.user) | Q(forSafePayment__sender=self.request.user)))


class SafePaymentApi(generics.ListAPIView):
    serializer_class = SafePaymentSerializer
    def get_queryset(self):
        return SafePayment.objects.filter(Q(receiver__username= self.request.user) | Q(sender__username= self.request.user)) 

# TODO : check it
class AcceptSafePaymentApi(APIView):
    def get(self, request):
        safePaymentResult = SafePayment.objects.get(pk=self.request.GET['pk'])
        if request.user == safePaymentResult.sender:
            if safePaymentResult.paymentBoolean:
                userResult = safePaymentResult.receiver
                userResult.cash += safePaymentResult.price
                userResult.save()
            safePaymentResult.senderBoolean = True
            safePaymentResult.save()
            return Response(status=status.HTTP_200_OK)

        elif request.user == safePaymentResult.receiver:
            if safePaymentResult.senderBoolean:
                userResult = safePaymentResult.receiver
                userResult.cash += safePaymentResult.price
                userResult.save()
            safePaymentResult.paymentBoolean = True
            safePaymentResult.save()
            return Response(status=status.HTTP_200_OK) 
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


# TODO : check it
class RefuseSafePaymentApi(APIView):
    def get(self, request):
        safePaymentResult = SafePayment.objects.get(pk=self.request.GET['pk'])
        if request.user == safePaymentResult.receiver:
            if safePaymentResult.senderBoolean is False and safePaymentResult.paymentBoolean is not None:
                userResult = safePaymentResult.sender
                userResult.cash += safePaymentResult.price
                userResult.save()
                safePaymentResult.paymentBoolean = None
                safePaymentResult.save()
                return Response(status=status.HTTP_200_OK) 
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class TrelloDestroyApi(generics.DestroyAPIView):
    serializer_class = TrelloSerializers
    def get_queryset(self):
        return Trello.objects.filter((Q(forSafePayment__receiver=self.request.user) | Q(forSafePayment__sender=self.request.user)) &
                Q(pk=self.kwargs.get('pk')))
                


class SubsetTrelloDestroyApi(generics.DestroyAPIView):
    serializer_class = SubsetTrelloSerializers
    def get_queryset(self):
        return SubsetTrello.objects.filter(author=self.request.user,pk=self.kwargs.get('pk'))



class DisputeApi(generics.ListAPIView):
    serializer_class = DisputeSerializer
    def get_queryset(self):
        return Dispute.objects.filter(Q(safePayment__receiver=self.request.user) | Q(safePayment__sender=self.request.user))



class DisputeDestroyApi(generics.DestroyAPIView):
    serializer_class = DisputeSerializer
    def get_queryset(self):
        return Dispute.objects.filter(author = self.request.user, pk=self.kwargs['pk']) 
    


class OrderApi(generics.ListAPIView):
    serializer_class = OrderSerializers
    def get_queryset(self):
        return OrderUser.objects.filter(Q(designer=self.request.user) | Q(author=self.request.user)).order_by("-pk")


class AddOrderApi(generics.CreateAPIView):
    serializer_class = OrderSerializers
    def perform_create(self, serializer):
        serializer.save(author=self.request.user,designer=User.objects.get(username=self.kwargs["username"]))


class OrderTrueApi(APIView):
    def get(self,request):
        OrderUserInstance = OrderUser.objects.get(pk=self.request.GET['pk'])
        if OrderUserInstance.author == request.user or OrderUserInstance.designer == request.user:
            OrderUserInstance.accept = True
            OrderUserInstance.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderFalseApi(APIView):
    def get(self,request):
        OrderUserInstance = OrderUser.objects.get(pk=self.request.GET['pk'])
        if OrderUserInstance.author == request.user or OrderUserInstance.designer == request.user:
            OrderUserInstance.accept = False
            OrderUserInstance.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CheckToken(APIView):
    permission_classes = (AllowAny, )
    def get(self,request):
        is_tokened = Token.objects.filter(key=self.request.GET['token'])
        print(is_tokened)
        if len(is_tokened) != 0 :
            return Response(status=status.HTTP_200_OK)
        else :
            return Response(status=status.HTTP_404_NOT_FOUND)


class PicturePostListApi(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PictureSerializer
    def get_queryset(self):
        return Picture.objects.filter(author = User.objects.get(username=self.kwargs.get('username'))).order_by('createdAdd')[::-1]
    

class CountReadStatus(APIView):
    def get(self,request):
        notification = Notification.objects.filter(readingStatus=False,receiver=request.user)
        message = Message.objects.filter(read=False,receiver=request.user)
        return Response({"message":len(message),"notification":len(notification),"verify_phone":request.user.verify_phone},status=status.HTTP_200_OK)


class ListUserMessageApi(APIView):
    def get(self, request):
        result=list()
        messages = Message.objects.filter(Q(author=request.user) | Q(receiver=request.user))
        userlist = []
        for message in messages:
            if message.receiver == self.request.user:
                userlist.append(message.author)
            elif message.author == self.request.user:
                userlist.append(message.receiver)
        deleteDuplicateData = deleteDuplicate(userlist)
        for data in deleteDuplicateData:
            serializerData = UserSerializers(data,context={'request':request})
            dictData={'user':serializerData.data,
                'number':len(Message.objects.filter(receiver=request.user,read=False,author=data))}
            result.append(dictData)
        return Response(result,status=status.HTTP_200_OK)

    
class RequestListApi(generics.ListAPIView):
    serializer_class = RequestSerializer
    def get_queryset(self):
        return Request.objects.filter(author__username=self.kwargs.get('username')).order_by("-pk")

    
class User_suggestion(generics.ListAPIView):
    serializer_class = UserLessInformationSerializers
    def get_queryset(self):
        print(User.objects.filter(~Q(followers=self.request.user) & ~Q(image="")).order_by("?")[0:8])
        return User.objects.filter(~Q(followers=self.request.user) & ~Q(image="")).order_by("?")[0:8]


class RulesListApi(generics.ListAPIView):
    serializer_class = RulesSerializer
    queryset = Rules.objects.all()
    permission_classes = (AllowAny, )
    

class DeskApi(APIView):

    def get(self, request):
        context = {}
        if request.user.ServiceProvider:
            context = {
                "pictureCheck": False,
                "timelineCheck": False,
                "serviceCheck": False,
                "numberSafePayment": SafePayment.objects.filter(receiver=request.user).count(),
                "numberOrders": OrderUser.objects.filter(designer=request.user).count(),
                "numberPicture": Picture.objects.filter(author=request.user).count(),
                "numberDoProject": SafePayment.objects.filter(receiver=request.user, senderBoolean=True
                                                            , paymentBoolean=True).count(),
                "numberDoingProject": SafePayment.objects.filter(receiver=request.user, paymentBoolean=False).count(),
                "numberService": Service.objects.filter(author=request.user).count(),

            }
            print((len(Picture.objects.filter(author=request.user))))
            if len(Picture.objects.filter(author=request.user)) == 0:
                context.update({"pictureCheck": True})
            if len(Timeline.objects.filter(person=request.user)) == 0:
                context.update({"timelineCheck": True})
            if len(Service.objects.filter(author=request.user)) == 0:
                context.update({"serviceCheck": True})
        else:
            context = {
                "pictureCheck": False,
                "timelineCheck": False,
                "serviceCheck": False,
                "numberSafePayment": SafePayment.objects.filter(sender=request.user).count(),
                "numberOrders": OrderUser.objects.filter(author=request.user).count(),
                "numberRequest": Request.objects.filter(author=request.user).count(),
                "numberDoProject": SafePayment.objects.filter(sender=request.user, senderBoolean=True
                                                            , paymentBoolean=True).count(),
                "numberDoingProject": SafePayment.objects.filter(sender=request.user, paymentBoolean=False).count(),

            }
        
        return Response(context,status=status.HTTP_200_OK)
    
    
    
class Check_username(APIView):
    def get(self, request):
        # get data with ?Picture=pk in url
        username = self.request.GET['username']
        if not User.objects.filter(username=username).exists():
            return Response(status=status.HTTP_200_OK)
        else:   
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)