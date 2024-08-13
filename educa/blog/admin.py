from django.contrib import admin
from .models import Post, PostComment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass
