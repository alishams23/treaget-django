from django.urls import path
from . import views
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token

router = routers.SimpleRouter()
router.register(r'HomeApiView', views.HomeApiView, basename="HomeApiView")

app_name = "api"
urlpatterns = [
    path('token/', obtain_auth_token),
    path('CheckToken/', views.CheckToken.as_view(), name="CheckToken"),
    # path('token/', TokenObtainPairView.as_view(),name='token_obtain_pair'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ExploreApiView/', views.ExploreApiView.as_view(), name="ExploreApiView"),
    path('ExploreProjectApiView/', views.ExploreProjectApiView.as_view(),
         name="ExploreProjectApiView"),
    path('AddLikeView/', views.AddLikeView.as_view(), name="AddLikeView"),
    path('timelineDeleteApi/<int:pk>/',
         views.timelineDeleteApi.as_view(), name="timelineDeleteApi"),
    path('timelineRetrieveApiView/', views.timelineRetrieveApiView.as_view(),
         name="timelineRetrieveApiView"),
    path('MassageApi/', views.MassageApi.as_view(), name="MassageApi"),
    path('AllMassageApi/', views.AllMassageApi.as_view(), name="AllMassageApi"),
    path('FollowUnfollowApi/<str:username>/',
         views.FollowUnfollowApi.as_view(), name="FollowUnfollowApi"),
    path('ServiceListApi/<str:username>/',
         views.ServiceListApi.as_view(), name="ServiceListApi"),
     path('AddOptionService/',
         views.AddOptionService.as_view(), name="AddOptionService"),
     path('AddService/',
         views.AddService.as_view(), name="AddService"),
    # get data like this ?&min_price=50001&max_price=80000&search=logo&ordering=-price
    path('ServiceSearchApi/', views.ServiceSearchApi.as_view(),
         name="ServiceSearchApi"),
    path('DestroyServiceApi/<int:pk>/',
         views.DestroyServiceApi.as_view(), name="DestroyServiceApi"),
    path('PicturePostDestroyRetrive/<int:pk>/',
         views.PicturePostDestroyRetrive.as_view(), name="PicturePostDestroyRetrive"),
    path('RequestPostDestroyRetrive/<int:pk>/',
         views.RequestPostDestroyRetrive.as_view(), name="RequestPostDestroyRetrive"),
    path('AddRequestApi/', views.AddRequestApi.as_view(), name="AddRequestApi"),
    path('DestroyRequestApi/<int:pk>/', views.DestroyRequestApi.as_view(), name="DestroyRequestApi"),
    path('RequestSearchApi/', views.RequestSearchApi.as_view(),
         name="RequestSearchApi"),
    path('UserSettingApi/<int:pk>/',
         views.UserSettingApi.as_view(), name="UserSettingApi"),
    path('UserRetrieveApi/<str:username>/',
         views.UserRetrieveApi.as_view(), name="UserRetrieveApi"),
    path('UserSearchListApi/', views.UserSearchListApi.as_view(),
         name="UserSearchListApi"),
    path('AddPostPictureApi/', views.AddPostPictureApi.as_view(),
         name="AddPostPictureApi"),
    path('UserCreate/', views.UserCreate.as_view(), name="UserCreate"),
    path('NotificationApi/', views.NotificationApi.as_view(), name="NotificationApi"),
    path('CashApi/', views.CashApi.as_view(), name="CashApi"),
    path('PaymentWalletApi/', views.PaymentWalletApi.as_view(),
         name="PaymentWalletApi"),
    path('favoritesApi/<str:username>/',
         views.favoritesApi.as_view(), name="favoritesApi"),
    path('SafePaymentApi/', views.SafePaymentApi.as_view(), name="SafePaymentApi"),
    path('TrelloApi/<int:pk>/', views.TrelloApi.as_view(), name="TrelloApi"),
    path('SubsetTrelloDestroyApi/<int:pk>/',
         views.SubsetTrelloDestroyApi.as_view(), name="SubsetTrelloDestroyApi"),
    path('DisputeApi/', views.DisputeApi.as_view(), name="DisputeApi"),
    path('DisputeDestroyApi/<int:pk>/',
         views.DisputeDestroyApi.as_view(), name="DisputeDestroyApi"),
    path('OrderApi/', views.OrderApi.as_view(), name="OrderApi"),
    path('AddOrderApi/<str:username>/', views.AddOrderApi.as_view(), name="AddOrderApi"),
    path('OrderTrueApi/<int:pk>/',
         views.OrderTrueApi.as_view(), name="OrderTrueApi"),
    path('OrderFalseApi/<int:pk>/',
         views.OrderFalseApi.as_view(), name="OrderFalseApi"),
    path('CountReadStatus/', views.CountReadStatus.as_view(), name="CountReadStatus"),
    path('PicturePostListApi/<str:username>/',
         views.PicturePostListApi.as_view(), name="PicturePostListApi"),
    path('ListUserMessageApi/', views.ListUserMessageApi.as_view(),
         name="ListUserMessageApi"),
]

urlpatterns += router.urls
