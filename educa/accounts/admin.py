from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Message, InstructorRequest, ContactUs

fields = list(UserAdmin.fieldsets)
fields[1] = (
    'المعلومات الشخصية',
    {
        'fields': (
            'first_name',
            'last_name',
            'email',
            'image',
            'phone_number',
            'description',
        )
    }
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'username',
        'email',
        'get_full_name',
        'is_superuser',
        'is_staff',
        'is_active',
    ]
    fieldsets = tuple(fields)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('first_name', 'last_name', 'email', 'phone_number',)}),)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(InstructorRequest)
class InstructorRequestAdmin(admin.ModelAdmin):
    pass

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    pass