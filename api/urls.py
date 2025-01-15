from django.urls import path, include
from users.views import LoginAPI, RegisterAPI
from blogs.views import BlogAPI, CommentAPI, CommentDeleteAPI, BlogGetUpdateDeleteAPI

urlpatterns = [
    path('login/',LoginAPI.as_view()),
    path('register/',RegisterAPI.as_view()),
    path('blogs/',BlogAPI.as_view()),
    path('comments/',CommentAPI.as_view()),
    path('comments/<int:comment_id>/',CommentDeleteAPI.as_view()),
    path('blogs/<int:blog_id>/',BlogGetUpdateDeleteAPI.as_view()),
] 