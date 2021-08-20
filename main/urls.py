from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from . import views
from account.views import cv, service, favourites

app_name="main"
urlpatterns = [
    path('', views.index,name="main"),
    path('explore/', views.explore,name="explore"),
    path('explore/lazy_load_posts/', views.lazyLoadExplore,name="lazy_load_posts"),
    path('contact/', views.Contact,name="contact"),
    path('p/<str:slug>/', views.profile , name="profile"),
    path('p/<str:slug>/cv', cv, name="cv"),
    path('p/<str:slug>/service', service , name="service"),
    path('p/<str:slug>/favourites', favourites, name="favourites"),
    path('search/', views.search , name="search"),
    path('Rules/', views.rules, name="Rules"),
    path('request/<int:pk>/', views.requestUser, name="request"),

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

