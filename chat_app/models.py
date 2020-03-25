from django.db import models
from django.utils import timezone


class Message(models.Model):
    username = models.CharField(max_length=150)
    message = models.TextField()
    message_type = models.CharField(choices=[('notification', 'notification'), ('chat_message', 'chat_message')],
                                    max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)
