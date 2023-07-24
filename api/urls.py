
from django.urls import  include, path,re_path
from . import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_view


router = routers.SimpleRouter()
router.register(r'HomeApiView', views.HomeApiView, basename="HomeApiView")


urlpatterns = [
# urls.py
     path('social/google/', include("social_django.urls", namespace='social')),
     path('blog/', include('blog.urls')),
     path('login/', auth_view.LoginView.as_view(), name='login'),
     path('token/', obtain_auth_token),
     path('CheckToken/', views.CheckToken.as_view(), name="CheckToken"),
     # path('token/', TokenObtainPairView.as_view(),name='token_obtain_pair'),
     # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('ExploreApiView/', views.ExploreApiView.as_view(), name="ExploreApiView"),
     path('ExploreProjectApiView/', views.ExploreProjectApiView.as_view(),
          name="ExploreProjectApiView"),
     path('AddLikeView/', views.AddLikeView.as_view(), name="AddLikeView"),
     path('MassageApi/', views.MassageApi.as_view(), name="MassageApi"),
     path('AllMassageApi/', views.AllMassageApi.as_view(), name="AllMassageApi"),
     path('FollowUnfollowApi/<str:username>/',
          views.FollowUnfollowApi.as_view(), name="FollowUnfollowApi"),



     # get data like this ?&min_price=50001&max_price=80000&search=logo&ordering=-price


     path('PicturePostDestroyRetrive/<int:pk>/',
          views.PicturePostDestroyRetrive.as_view(), name="PicturePostDestroyRetrive"),
     path('RequestPostDestroyRetrive/<int:pk>/',
          views.RequestPostDestroyRetrive.as_view(), name="RequestPostDestroyRetrive"),
     path('AddAcceptRequestApi/<int:pk>/',
          views.AddAcceptRequestApi.as_view(), name="AddAcceptRequestApi"),
     path('AddRequestApi/', views.AddRequestApi.as_view(), name="AddRequestApi"),
     path('RequestListApi/<str:username>/', views.RequestListApi.as_view(), name="RequestListApi"),
     path('DestroyRequestApi/<int:pk>/', views.DestroyRequestApi.as_view(), name="DestroyRequestApi"),
     path('RequestSearchApi/', views.RequestSearchApi.as_view(),name="RequestSearchApi"),
     path('PictureSearchApi/', views.PictureSearchApi.as_view(),
          name="PictureSearchApi"),
     path('UserSettingApi/',
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
     path('AddDisputeApi/',
          views.AddDisputeApi.as_view(), name="AddDisputeApi"),
     path('OrderApi/', views.OrderApi.as_view(), name="OrderApi"),
     path('AddOrderApi/<str:username>/', views.AddOrderApi.as_view(), name="AddOrderApi"),
     path('OrderTrueApi/',
          views.OrderTrueApi.as_view(), name="OrderTrueApi"),
     path('OrderFalseApi/',
          views.OrderFalseApi.as_view(), name="OrderFalseApi"),
     path('CountReadStatus/', views.CountReadStatus.as_view(), name="CountReadStatus"),
     path('PicturePostListApi/<str:username>/',
          views.PicturePostListApi.as_view(), name="PicturePostListApi"),
     path('ListUserMessageApi/', views.ListUserMessageApi.as_view(),
          name="ListUserMessageApi"),
     path('DeskApi/', views.DeskApi.as_view(),name="DeskApi"),
     path('AcceptSafePaymentApi/', views.AcceptSafePaymentApi.as_view(),name="AcceptSafePaymentApi"),
     path('RefuseSafePaymentApi/', views.RefuseSafePaymentApi.as_view(),name="RefuseSafePaymentApi"),
     path('RulesListApi/', views.RulesListApi.as_view(),name="RulesListApi"),
     path('SpamCreateApi/', views.SpamCreateApi.as_view(),name="SpamCreateApi"),
     path('UserSuggestion/', views.User_suggestion.as_view(),name="User_suggestion"),
     path('Send_code/', views.Send_code.as_view(),name="Send_code"),
     path('Code_check/', views.Code_check.as_view(),name="Code_check"),
     path('PostTagApi/', views.PostTagApi.as_view(),name="PostTagApi"),
     path('following/', views.following.as_view(),name="following"),
     path('followingList/', views.followingList.as_view(),name="followingList"),
     path('followersList/', views.followersList.as_view(),name="followersList"),
     path('ContactApi/', views.ContactApi.as_view(),name="ContactApi"),
]

urlpatterns += router.urls
