from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.posts, name='posts'),
    path('<pk>/', views.post_detail, name='post_detail'),
]