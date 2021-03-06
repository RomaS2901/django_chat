# Generated by Django 3.0.4 on 2020-03-25 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat_app', '0002_auto_20200325_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='mentioned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mentions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_type',
            field=models.CharField(choices=[('notification', 'notification'), ('chat_message', 'chat_message'), ('mention', 'mention')], max_length=50),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
