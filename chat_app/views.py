from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Message


@login_required()
def chat_room(request):
    messages = Message.objects.all().order_by('-timestamp')
    return render(request, 'chat_app/chat_room.html', context={'messages': messages})
