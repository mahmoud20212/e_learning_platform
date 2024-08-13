import uuid

from datetime import timedelta

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from courses.models import Course


def validate_datetime_in_future(value):
    # Add one day to the current time
    one_day_in_future = timezone.now() + timedelta(days=1)

    if value <= one_day_in_future:
        raise ValidationError('The date must be at least one day later.')


class Room(models.Model):
    ROOM_STATUS = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rooms_created', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='course_rooms', on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=ROOM_STATUS, default='active')
    available = models.BooleanField(default=True)
    start_date = models.DateTimeField(
        validators=[validate_datetime_in_future],
        help_text='The date must be at least one day later.'
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.course
