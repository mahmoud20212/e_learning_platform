from django.db import models
from django.conf import settings
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='الكاتب')
    image = models.ImageField(upload_to='blog/images', verbose_name='الصورة')
    title = models.CharField(max_length=255, verbose_name='العنوان')
    content = models.TextField(verbose_name='المحتوى')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.pk])


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE, verbose_name='التدوينة')
    name = models.CharField(max_length=255, verbose_name='الإسم')
    email = models.EmailField(verbose_name='البريد الإلكتروني')
    description = models.TextField(verbose_name='الوصف')
    active = models.BooleanField(default=False, verbose_name='فعال')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} علق على التدوينة ({self.post})'

    class Meta:
        ordering = ['-created']
