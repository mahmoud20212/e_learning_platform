from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.db.models import Count
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from .models import Subject, Course, FAQ, CourseComment
from .forms import CourseEnrollForm, CourseCommentForm
from blog.models import Post


def index(request):
    faqs = FAQ.objects.all()
    posts = Post.objects.all()[:6]
    courses = Course.objects.all()[:5]


    return render(
        request,
        'courses/index.html',
        {
            'page': 'index',
            'faqs': faqs,
            'posts': posts,
            'courses': courses,
        }
    )


class CourseListView(TemplateResponseMixin, View):
    template_name = 'courses/list.html'

    def get(self, request, subject=None):
        # level = request.GET.get('level')
        # print(level)
        # price = request.GET.get('price')
        # if level or price:
        #     pass

        subjects = Subject.objects.annotate(total_courses=Count('courses'))
        query = Course.objects.filter(available=True)
        random_courses = query.order_by('?')
        courses = query.annotate(total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)

        return self.render_to_response({
            'subjects': subjects,
            'subject': subject,
            'courses': courses,
            'random_courses': random_courses,
        })


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        context['course_comments'] = CourseComment.objects.filter(course=self.object, active=True)
        if self.request.user.is_authenticated:
            context['comment_form'] = CourseCommentForm(initial={'user': self.request.user, 'course': self.object})
        return context

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:student_course_detail', args=[self.course.id])

@login_required
def add_course_comment(request, slug):
    if request.method == 'POST':
        form = CourseCommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم اضافة تعليقك بنجاح. تعليقك الآن قيد المراجعة.')
            return redirect(reverse('courses:course_detail', args=[slug]))