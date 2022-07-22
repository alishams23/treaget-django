from django.urls import path
from . import views
from account import views as Function




app_name = "projectManager"
urlpatterns = [
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

]


