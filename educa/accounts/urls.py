from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

auth_urlpatterns = [
    path('login/', auth_views.LoginView.as_view(extra_context={'page': 'auth'}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    path('course/mine/', views.ManageCourseListView.as_view(), name='manage_course_list'),
    path('course/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('course/<pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('course/<pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    path('course/<pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module_update'),

    path(
        'course/module/<int:module_id>/content/<model_name>/create/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_create'
    ),
    path(
        'course/module/<int:module_id>/content/<model_name>/<id>/',
        views.ContentCreateUpdateView.as_view(),
        name='module_content_update'
    ),

    path(
        'course/content/<int:id>/delete/',
        views.ContentDeleteView.as_view(),
        name='module_content_delete'
    ),

    path(
        'course/module/<int:module_id>/',
        views.ModuleContentListView.as_view(),
        name='module_content_list'
    ),

    path(
        'course/module/order/',
        views.ModuleOrderView.as_view(),
        name='module_order'
    ),
    path(
        'course/content/order/',
        views.ContentOrderView.as_view(),
        name='content_order'
    ),

    path(
        'courses/',
        views.StudentCourseListView.as_view(),
        name='student_course_list'
    ),
    path(
        'course/<pk>/',
        views.StudentCourseDetailView.as_view(),
        name='student_course_detail'
    ),
    path(
        'course/<pk>/<module_id>/',
        views.StudentCourseDetailView.as_view(),
        name='student_course_detail_module',
    ),
    path('course/module-comment/<pk>', views.add_module_comment, name='add_module_comment'),

    path('blog/posts/', views.UserPostListView.as_view(), name='user_post_list'),
    path('blog/post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('blog/post/<pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('blog/post/<pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    path('messages/inbox/', views.inbox_messages, name='inbox_messages'),
    path('messages/sent/', views.sent_messages, name='sent_messages'),
    path('messages/<pk>/show/', views.read_message, name='read_message'),
    path('messages/create/', views.create_message, name='create_message'),

    path('instructor/register/', views.instructor_register, name='instructor_register'),
    path('instructor/<pk>/show', views.instructor_show, name='instructor_show'),

    path('contact-us/', views.contact_us, name='contact_us'),
] + auth_urlpatterns
