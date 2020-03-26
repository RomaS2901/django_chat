from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .models import Message


@login_required()
def chat_room(request):
    messages = Message.objects.all().order_by('-timestamp')
    users = get_user_model().objects.all().values('id', 'username')
    return render(request, 'chat_app/chat_room.html', context={
        'messages': messages,
        'users': users
    })
