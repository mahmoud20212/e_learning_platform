from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='accounts/images', default='defaults/default.jpg', verbose_name='صورة الملف الشخصي')
    phone_number = models.CharField(max_length=255, verbose_name='رقم الهاتف')
    education = models.CharField(max_length=255, verbose_name='التعليم', null=True, blank=True)
    location = models.CharField(max_length=255, verbose_name='السكن', null=True, blank=True)
    skills = models.CharField(max_length=255, verbose_name='المهارات', null=True, blank=True)
    notes = models.CharField(max_length=255, verbose_name='ملاحظات', null=True, blank=True)
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='الوصف',
        help_text='يمكنك كتابة أي شئ تريده هنا.'
    )

    def __str__(self):
        return self.get_full_name()

class InstructorRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='المستخدم',
    )
    subject = models.CharField(
        max_length=255,
        verbose_name='الموضوع',
    )
    description = models.TextField(verbose_name='الوصف')

    def __str__(self):
        return f'{self.user.get_full_name()} - @{self.user.username}'

class Message(models.Model):
    sender_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sender_user_messages',
        on_delete=models.CASCADE,
        verbose_name='المرسل',
    )
    recipient_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='recipient_user_messages',
        on_delete=models.CASCADE,
        verbose_name='المستلم',
    )
    subject = models.CharField(
        max_length=255,
        verbose_name='الموضوع',
    )
    description = models.TextField(verbose_name='الوصف')
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'من {self.sender_user} الى {self.recipient_user}'


class ContactUs(models.Model):
    name = models.CharField(max_length=255, verbose_name='الإسم')
    email = models.EmailField(verbose_name='البريد الإلكتروني')
    description = models.TextField(verbose_name='الوصف')

    def __str__(self):
        return f'{self.name} - {self.email}'