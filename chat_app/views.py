from django.shortcuts import render
from .models import Message


def chat_room(request):
    messages = Message.objects.all().order_by('-timestamp')
    return render(request, 'chat_app/chat_room.html', context={'messages': messages})
