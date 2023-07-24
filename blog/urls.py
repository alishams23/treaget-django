from django.urls import path
from .views import *

urlpatterns = [
  path('Search_list_view/',SearchListView.as_view(),name="Search_list_view"),
  path('blog_retrieve_category/<int:pk>/',BlogRetrieveCategory.as_view(),name="blog_retrieve_category"),
  path('blog_retrieve/<int:pk>/',BlogRetrieve.as_view(),name="blog_retrieve"),
  path('Blog_List/',BlogList.as_view(),name="Blog_List"),
  path('List_category/',ListCategory.as_view(),name="List_category"),
  path('createBlog/',CreateBlog.as_view(),name="CreateBlog"),
  path('CreateImage/',CreateImage.as_view(),name="CreateImage"),
  path('AddLikeView/',AddLikeView.as_view(),name="AddLikeView"),
  path('BlogRemove/<int:pk>/', BlogRemove.as_view(), name="BlogRemove"),
  path('BlogUpdate/<int:pk>/', BlogUpdate.as_view(), name="BlogUpdate"),

]