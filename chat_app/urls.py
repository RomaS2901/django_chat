from django.urls import path
from chat_app import views

urlpatterns = [
    path('', views.chat_room, name='chat-room')
]