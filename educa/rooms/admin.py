from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        'course',
        'id',
        'status',
        'available',
    ]
    search_fields = ['id']
