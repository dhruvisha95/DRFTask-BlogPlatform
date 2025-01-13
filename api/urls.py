from django.urls import path, include
from users.views import LoginAPI, RegisterAPI
from blogs.views import BlogAPI, CommentAPI

urlpatterns = [
    path('login/',LoginAPI.as_view()),
    path('register/',RegisterAPI.as_view()),
    path('blogs/',BlogAPI.as_view()),
    path('comments/',CommentAPI.as_view())
] 