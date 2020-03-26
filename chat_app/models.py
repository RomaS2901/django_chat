from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Message(models.Model):

    MESSAGE_TYPE_CHOICES = [
        ('notification', 'notification'),
        ('chat_message', 'chat_message'),
        ('mention', 'mention'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    mentioned = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True, related_name='mentions')
    message_type = models.CharField(choices=MESSAGE_TYPE_CHOICES, max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)
