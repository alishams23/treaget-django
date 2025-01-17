from django.urls import  path
from . import views

app_name = "chat"
urlpatterns = [
     path('ChatList/',
          views.ChatList.as_view(), name="ChatList"),
     path('Search/',
          views.Search.as_view(), name="Search"),
     path('ChatRetrieve/<str:username>/',
          views.ChatRetrieve.as_view(), name="ChatRetrieve"),
]

