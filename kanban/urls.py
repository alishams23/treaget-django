from django.urls import path
from . import views




app_name = "kanban"
urlpatterns = [
     path('kanban/<int:pk>/', views.Kanban_api.as_view(), name="TrelloApi"),
#     path('SubsetTrelloDestroyApi/<int:pk>/',
#          views.KanbanList_item.as_view(), name="SubsetTrelloDestroyApi"),
]

