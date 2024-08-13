from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth import get_user_model
from .models import CustomUser, Message, InstructorRequest, ContactUs
from courses.models import Course, Module, ModuleComment


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('image', 'phone_number', 'description',)

    def clean_email(self):
        data = self.cleaned_data['email']
        if CustomUser.objects.filter(email=data).exists():
            raise forms.ValidationError('هذا البريد الإلكتروني مستخدم بالفعل.')
        return data


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class UserRegistrationForm(UserCreationForm):
    # for validation
    first_name = forms.CharField(required=True, min_length=3, max_length=255)
    last_name = forms.CharField(required=True, min_length=3, max_length=255)
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'phone_number', 'email',)  # for save value

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'block w-full rounded-full border-0 px-4 py-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-green-500 sm:text-sm sm:leading-6 outline-none'

    def clean_email(self):
        data = self.cleaned_data['email']
        if CustomUser.objects.filter(email=data).exists():
            raise forms.ValidationError('هذا البريد الإلكتروني مستخدم بالفعل.')
        return data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'image',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'education',
            'location',
            'skills',
            'notes',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def clean_email(self):
        data = self.cleaned_data['email']
        if CustomUser.objects.filter(email=data).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('هذا البريد الإلكتروني مستخدم بالفعل.')
        return data


ModuleFormSet = inlineformset_factory(
    Course,
    Module,
    fields=['title', 'description'],
    extra=2,
    can_delete=True
)

class ModuleCommentForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.HiddenInput,
    )
    module = forms.ModelChoiceField(
        queryset=Module.objects.all(),
        widget=forms.HiddenInput,
    )

    class Meta:
        model = ModuleComment
        fields = [
            'module',
            'user',
            'description',
        ]

class MessageForm(forms.ModelForm):
    sender_user = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.HiddenInput,
    )

    class Meta:
        model = Message
        fields = [
            'sender_user',
            'recipient_user',
            'subject',
            'description',
        ]

class InstructorRequestForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.HiddenInput,
    )

    class Meta:
        model = InstructorRequest
        fields = [
            'user',
            'subject',
            'description',
        ]

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = [
            'name',
            'email',
            'description',
        ]