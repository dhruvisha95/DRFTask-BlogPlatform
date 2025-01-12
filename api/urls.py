from django.urls import path, include
from users.views import LoginAPI, RegisterAPI

urlpatterns = [
    path('login/',LoginAPI.as_view()),
    path('register/',RegisterAPI.as_view()),
] 