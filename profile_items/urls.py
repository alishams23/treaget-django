
from django.urls import  path
from . import views



app_name = "profile_items"
urlpatterns = [
    path('SkillsList/', views.SkillsList.as_view(),name="SkillsList"),
    path('AddOptionService/', views.AddOptionService.as_view(),name="AddOptionService"),
         path('ServiceListApi/<str:username>/',
          views.ServiceListApi.as_view(), name="ServiceListApi"),
               path('ServiceSearchApi/', views.ServiceSearchApi.as_view(),
          name="ServiceSearchApi"),
               path('DestroyServiceApi/<int:pk>/',
          views.DestroyServiceApi.as_view(), name="DestroyServiceApi"),
               path('AddService/',
          views.AddService.as_view(), name="AddService"),
]


