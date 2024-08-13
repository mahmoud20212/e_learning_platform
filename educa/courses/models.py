from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.urls import reverse

from .fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=255, verbose_name='العنوان')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='العنوان المميز')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    LEVELS = (
        ('junior', 'مبتدئ'),
        ('intermediate', 'متوسط'),
        ('professional', 'محترف'),
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='المالك', related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, verbose_name='التصنيف', related_name='courses', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='courses/images', verbose_name='الصورة')
    title = models.CharField(max_length=255, verbose_name='العنوان')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='العنوان المميز')
    caption = models.CharField(max_length=255, verbose_name='التسمية التوضيحية')
    overview = models.TextField(verbose_name='الملخص')
    level = models.CharField(choices=LEVELS, default='junior', max_length=15, verbose_name='المستوى')
    # price = models.DecimalField(
    #     max_digits=10,
    #     decimal_places=2,
    #     null=True,
    #     blank=True,
    #     verbose_name='السعر',
    #     help_text='إذا كنت تريد أن تجعل هذه الدورة مجانية، فاترك هذا الحقل فارغًا.'
    # )
    available = models.BooleanField(default=True, verbose_name='متاح')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses_joined', blank=True, verbose_name='الطلاب')
    # users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses_liked', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_detail', args=[self.slug])


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE, verbose_name='الدورة')
    title = models.CharField(max_length=255, verbose_name='العنوان')
    description = models.TextField(blank=True, verbose_name='الوصف')
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'

class ModuleComment(models.Model):
    module = models.ForeignKey(Module, related_name='module_comments', on_delete=models.CASCADE, verbose_name='الوحدة')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_module_comments', on_delete=models.CASCADE, verbose_name='المستخدم')
    description = models.TextField(verbose_name='الوصف')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} علق على ({self.module})'

    class Meta:
        ordering = ['-created']


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE, verbose_name='الوحدة')
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in': (
                'text',
                'video',
                'image',
                'file'
            )
        }
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_related', on_delete=models.CASCADE, verbose_name='المالك')
    title = models.CharField(max_length=255, verbose_name='العنوان')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self}
        )


class Text(ItemBase):
    content = models.TextField(verbose_name='النص')


class File(ItemBase):
    file = models.FileField(upload_to='files', verbose_name='الملف')


class Image(ItemBase):
    file = models.FileField(upload_to='images', verbose_name='الصورة')


class Video(ItemBase):
    url = models.URLField(verbose_name='رابط الفيديو')


class CourseComment(models.Model):
    RATE_CHOICES = (
        ('1', '1 ⭐'),
        ('2', '2 ⭐'),
        ('3', '3 ⭐'),
        ('4', '4 ⭐'),
        ('5', '5 ⭐'),
    )
    course = models.ForeignKey(Course, related_name='course_comments', on_delete=models.CASCADE, verbose_name='الدورة')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_course_comments', on_delete=models.CASCADE, verbose_name='المستخدم')
    description = models.TextField(verbose_name='الوصف')
    rating = models.CharField(choices=RATE_CHOICES, max_length=5, default='1', verbose_name='التقييم')
    active = models.BooleanField(default=False, verbose_name='فعال')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.user} علق على ({self.course})'



class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name='السؤال')
    answer = models.TextField(verbose_name='الإجابة')

    def __str__(self):
        return self.question
