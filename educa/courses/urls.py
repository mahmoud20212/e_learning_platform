from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='courses_list'),
    path('enroll-course/', views.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('course-comments/<slug:slug>/', views.add_course_comment, name='add_course_comment'),
    path('subject/<slug:subject>/', views.CourseListView.as_view(), name='course_list_subject'),
    path('<slug:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
]
