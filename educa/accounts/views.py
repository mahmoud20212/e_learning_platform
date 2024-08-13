import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateResponseMixin, View
from django.forms.models import modelform_factory
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.urls import reverse_lazy, reverse
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from .forms import UserRegistrationForm, ModuleFormSet, ProfileForm, ModuleCommentForm, MessageForm, InstructorRequestForm, ContactUsForm
from courses.models import Course, Module, Content, ModuleComment, CourseComment
from blog.models import Post, PostComment
from .models import Message, InstructorRequest
from django.contrib.auth import get_user_model


def dashboard(request):
    hints = [
        'أن توقد شمعة خير لك من أن تقضي العمر وأنت تلعن الظلام.',
        'لا تعطني سمكة، بل علمني كيف أصطاد وأجلب قوت يومي.',
        'لا يسكن المستحيل سوى أدمغة العاجزين، ولا يقوم بالاستسلام سوى الضعفاء.',
        'ليس الفشل في التعثر والوقوع، بل يكمن الفشل في البقاء وعدم النهوض.',
        'الناجحون هم من يأخذون أحلامهم على محمل الجد، ويسعون إلى تحقيقها رغم كلمة مستحيل.',
        'قم بما تحب، أو لا تقم بأي شيء.',
        'قد يبدو الأمر مستحيلًا لأول وهلة، إلى أن يتمكن المرء من تحقيقه.',
        'اسع إلى النجاح من أجل نفسك ولمن يتمنون فشلك.',
        'إنسان بدون هدف كسفينة بدون دفة، كلاهما سوف ينتهي به الأمر على الصخور.',
        'الحياة بحر من التجارب، والحياة خير معلم.',
        'غير خطتك حين الفشل، لكن لا تغير أهدافك.',
        'اجعل رغبتك في النجاح أقوى من خوفك من الفشل.',
        'قد يبدو الأمر مستحيلًا لأول وهلة، إلى أن يتمكن المرء من تحقيقه.',
        'إن الإبداع ينتج عن ذكاء ممتع.',
        'الحكمة تأتي في صناعة الفرص عندما لا تكون متوفرة.',
    ]
    posts = Post.objects.filter(author=request.user)
    courses_comments = CourseComment.objects.filter(user=request.user)
    courses = Course.objects.filter(students__in=[request.user])
    my_messages = Message.objects.filter(recipient_user=request.user)
    
    return render(
        request,
        'accounts/dashboard.html',
        {
            'page': 'dashboard',
            'posts_count': posts.count(),
            'courses_count': courses.count(),
            'last_posts': posts[:3],
            'last_courses_comments': courses_comments[:3],
            'hint': random.choice(hints),
            'my_messages_count': my_messages.count(),
        }
    )


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم انشاء الحساب بنجاح... يمكنك تسجيل الدخول الآن.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(
        request,
        'registration/register.html',
        {
            'page': 'auth',
            'form': form,
        }
    )


def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث الملف الشخصي بنجاح!!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(
        request,
        'accounts/profile.html',
        {
            'form': form,
            'page': 'profile',
        }
    )


class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin:
    def form_valid(self, form):
        # save owner of course
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = [
        'subject',
        'image',
        'title',
        'slug',
        'caption',
        'overview',
        'level',
        # 'price',
        'available',
    ]
    success_url = reverse_lazy('accounts:manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'accounts/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'accounts/manage/course/list.html'
    permission_required = 'courses.view_course'
    extra_context = {
        'page': 'mine',
    }


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'
    extra_context = {
        'page': 'mine',
    }


class CourseUpdateView(OwnerCourseEditMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'courses.change_course'
    success_message = 'تم تعديل "%(title)s" بنجاح !!'
    extra_context = {
        'page': 'mine',
    }


class CourseDeleteView(OwnerCourseMixin, SuccessMessageMixin, DeleteView):
    template_name = 'accounts/manage/course/delete.html'
    permission_required = 'courses.delete_course'
    # success_message = 'تم حذف "%(title)s" بنجاح !!'
    extra_context = {
        'page': 'mine',
    }


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'accounts/manage/module/formset.html'
    course = None
    

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, f'تمت عملية تعديل الوحدات "{self.course}" بنجاح !!')
            return redirect('accounts:manage_course_list')
        return self.render_to_response({'course': self.course, 'formset': formset, 'page': 'mine'})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'accounts/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES
        )

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module, item=obj)
            return redirect('accounts:module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('accounts:module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'accounts/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(
                id=id,
                course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(
                id=id,
                module__course__owner=request.user
            ).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'accounts/students/course/list.html'
    extra_context = {
        'page': 'my_courses',
    }

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'accounts/students/course/detail.html'
    extra_context = {
        'page': 'my_courses',
    }

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            module = course.modules.get(id=self.kwargs['module_id'])
        else:
            # get first module
            module = course.modules.all()[0]
        
        module_comments = ModuleComment.objects.filter(module=module)

        context['module'] = module
        context['module_comments'] = module_comments
        return context

@login_required
def add_module_comment(request, pk):
    if request.method == 'POST':
        form = ModuleCommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم اضافة تعليقك بنجاح.')
            return redirect(reverse('accounts:student_course_detail', args=[pk]))

class AuthorMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class AuthorEditMixin:
    def form_valid(self, form):
        # save owner of course
        form.instance.author = self.request.user
        return super().form_valid(form)


class AuthorPostMixin(AuthorMixin, LoginRequiredMixin):
    model = Post
    fields = [
        'image',
        'title',
        'content',
    ]
    success_url = reverse_lazy('accounts:user_post_list')


class AuthorPostEditMixin(AuthorPostMixin, AuthorEditMixin):
    template_name = 'accounts/blog/form.html'


class UserPostListView(CsrfExemptMixin, AuthorPostMixin, JsonRequestResponseMixin, ListView):
    template_name = 'accounts/blog/list.html'
    extra_context = {
        'page': 'blog_posts',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = PostComment.objects.filter(post__in=self.get_queryset())
        context['comments'] = comments
        return context

    def post(self, request, *args, **kwargs):
        PostComment.objects.filter(id=self.request_json['idChecked'])\
            .update(active=self.request_json['isChecked'])
        return self.render_json_response({'saved': 'OK'})


class PostCreateView(AuthorPostEditMixin, SuccessMessageMixin, CreateView):
    success_message = 'تم إنشاء "%(title)s" بنجاح !!'
    extra_context = {
        'page': 'blog_posts',
    }


class PostUpdateView(AuthorPostEditMixin, SuccessMessageMixin, UpdateView):
    success_message = 'تم تعديل "%(title)s" بنجاح !!'
    extra_context = {
        'page': 'blog_posts',
    }


class PostDeleteView(AuthorPostMixin, SuccessMessageMixin, DeleteView):
    template_name = 'accounts/blog/delete.html'
    success_message = 'تم حذف التدوينة بنجاح !!'
    extra_context = {
        'page': 'blog_posts',
    }

def inbox_messages(request):
    my_messages = Message.objects.filter(recipient_user=request.user)
    
    return render(
        request,
        'accounts/messages/inbox.html',
        {
            'page': 'inbox_messages',
            'my_messages': my_messages,
        }
    )

def sent_messages(request):
    my_messages = Message.objects.filter(sender_user=request.user)
    
    return render(
        request,
        'accounts/messages/sent.html',
        {
            'page': 'sent_messages',
            'my_messages': my_messages,
        }
    )

def read_message(request, pk):
    my_message = get_object_or_404(Message, pk=pk)

    if request.user == my_message.recipient_user:
        my_message.is_read = True
        my_message.save()

    return render(
        request,
        'accounts/messages/read.html',
        {
            'my_message': my_message,
        }
    )

def create_message(request, pk=None):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إرسال الرسالة بنجاح.')
            return redirect('accounts:sent_messages')
    else:
        if 'target_user' in request.GET:
            target_user_pk = request.GET.get('target_user')
            user = get_object_or_404(get_user_model(), pk=target_user_pk)
            form = MessageForm(
                initial={
                    'sender_user': request.user,
                    'recipient_user': user,
                }
            )
            form.fields['recipient_user'].widget.attrs['disabled'] = True

        else:
            user = None
            form = MessageForm(
                initial={
                    'sender_user': request.user,
                }
            )
    
    return render(
        request,
        'accounts/messages/new_msg.html',
        {
            'page': 'new_message',
            'form': form,
        }
    )

def instructor_register(request):
    if request.method == 'POST':
        form = InstructorRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تمت العملية بنجاح. سيتم مراجعة طلبك في أسرع وقت ممكن.')
            return redirect('accounts:dashboard')
    else:
        obj = InstructorRequest.objects.filter(user=request.user)
        if obj.exists():
            form = None
        else:
            form = InstructorRequestForm(initial={'user': request.user})
    
    
    return render(
        request,
        'accounts/instructor/register.html',
        {
            'form': form,
        }
    )

def instructor_show(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    
    form = ProfileForm(instance=user)
    form.fields.pop('image')
    for field_name, field in form.fields.items():
        field.widget.attrs['readonly'] = True

    return render(
        request,
        'accounts/profile.html',
        {
            'form': form,
            'user':user,
        }
    )

def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم إرسال الرسالة بنجاح!!')
            return redirect('accounts:dashboard')
    else:
        form = ContactUsForm()
    
    return render(
        request,
        'accounts/contact_us.html',
        {
            'form': form,
        }
    )