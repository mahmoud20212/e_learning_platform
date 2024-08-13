# Generated by Django 4.2.5 on 2024-04-26 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='description',
            field=models.TextField(verbose_name='الوصف'),
        ),
        migrations.AlterField(
            model_name='message',
            name='recipient_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_user_messages', to=settings.AUTH_USER_MODEL, verbose_name='المستلم'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_user_messages', to=settings.AUTH_USER_MODEL, verbose_name='المرسل'),
        ),
        migrations.AlterField(
            model_name='message',
            name='subject',
            field=models.CharField(max_length=255, verbose_name='الموضوع'),
        ),
    ]
