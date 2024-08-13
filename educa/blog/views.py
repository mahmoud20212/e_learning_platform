from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Post, PostComment
from .forms import PostCommentForm


def posts(request):
    posts = Post.objects.all()

    return render(
        request,
        'blog/list.html',
        {
            'page': 'blog',
            'posts': posts,
        }
    )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    latest_posts = Post.objects.all()[:5]
    comments = PostComment.objects.filter(post=post, active=True)
    if request.method == 'POST':
        form = PostCommentForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.post = post
            new_form.save()
            messages.success(request, 'تم اضافة التعليق بنجاح... التعليق حالياً قيد المراجعة.')
            return redirect('blog:post_detail', post.pk)
    else:
        form = PostCommentForm()
        if request.user.is_authenticated:
            form.initial = {
                'name': request.user.get_full_name(),
                'email': request.user.email,
            }
    return render(
        request,
        'blog/detail.html',
        {
            'page': 'blog',
            'post': post,
            'latest_posts': latest_posts,
            'comments': comments,
            'form': form,
        }
    )
