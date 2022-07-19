from django.urls import path
from . import views



app_name = "api"
urlpatterns = [
    path('projectManagerDelete/<int:pk>/',
         views.projectManagerDelete.as_view(), name="projectManagerDelete"),

]


