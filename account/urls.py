# The views used below are normally mapped in django.contrib.admin.urls.py
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.contrib.auth import views
from django.urls import path, include
from . import views as Function

app_name = "account"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('', Function.home, name='home'),
    path('picture/', Function.picture, name='picture'),
    path('post/<int:pk>/', Function.post, name='post'),
    path('lazy_load_posts/', Function.lazy_load_posts, name='lazy_load_posts'),
    path('logout/', Function.logout_view, name='logout'),
    path('addpicture/', Function.addPicture, name='addPicture'),
    path('addcv/', Function.addCv, name='addCv'),
    path('addsafepayment/<str:username>/',
         Function.addSafePayment, name='addSafePayment'),
    path('addSafePaymentOrder/<int:pk>/',
         Function.addSafePaymentOrder, name='addSafePaymentOrder'),
    path('deletecv/<int:pk>/', Function.deleteCv, name='deleteCv'),
    path('deleteservice/<int:pk>/', Function.deleteService, name='deleteService'),
    path('setting/', Function.profile, name='setting'),
    path('message/', Function.message, name='message'),
    path('message/<str:username>/', Function.message, name='messageUser'),
    path('register/', Function.register, name='register'),
    # path('OrderViews/', Function.OrderViews, name='OrderViews'),
    path('operate/', include('accounting.urls'), name="accounting"),
    path('addService/', Function.addService, name='addService'),
    path('LikePost/', Function.LikePost, name='LikePost'),
    path('follow/', Function.follow, name='follow'),
    path('follow/<str:username>/', Function.follow, name='follow_User'),
    path('p/<str:slug>/checkout/', Function.checkoutUser, name="checkoutUser"),
    path('p/<str:slug>/checkout/<int:service>/',
         Function.checkoutUser, name="checkoutUserService"),
    path('desk/', Function.desk, name="desk"),
    path('notification/', Function.notification, name="notification"),
    path('orders/', Function.orders, name="orders"),
    path('ordersTrue/<int:pk>/', Function.ordersTrue, name="ordersTrue"),
    path('ordersFalse/<int:pk>/', Function.ordersFalse, name="ordersFalse"),
    path('listSafePayment/', Function.listSafePayment, name="listSafePayment"),
    path('listDispute/', Function.listDispute, name="listDispute"),
    path('addDispute/<int:pk>/', Function.addDispute, name="addDispute"),
    path('SafePaymentRefuse/<int:pk>/',
         Function.SafePaymentRefuse, name="SafePaymentRefuse"),
    path('SafePaymentAccept/<int:pk>/',
         Function.SafePaymentAccept, name="SafePaymentAccept"),
    path('createSafePayment/<int:pk_request>/<int:pk_accept>/',
         Function.createSafePayment, name="createSafePayment"),
    path('addRequest/', Function.addRequest, name="addRequest"),
    path('addAcceptRequest/<int:pk>/',
         Function.addAcceptRequest, name="addAcceptRequest"),
    path('projectManagement/<int:pk>/',
         Function.projectManagement, name="projectManagement"),
    path('DeleteProjectManagement/<int:pk>/',
         Function.deleteSubsetTrello, name="deleteSubsetTrello"),
    path('DeleteProjectManagementMain/<int:pk>/',
         Function.deleteTrello, name="deleteTrello"),
    path('AddSubsetProjectManagement/<int:pk>/',
         Function.AddSubsetProjectManagement, name="AddSubsetProjectManagement"),
    path('AddProjectManagement/<int:pk>/',
         Function.AddProjectManagement, name="AddProjectManagement"),
    path('numberOfFollowers/<str:username>/',
         Function.numberOfFollowers, name="numberOfFollowers"),
    path('numberOfFollowing/<str:username>/',
         Function.numberOfFollowing, name="numberOfFollowing"),

    # path('change_picture/<int:pk>', change_picture, name='change-picture'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),

    # path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),


]
