from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import PostForm
from .models import Post, Group, User
from django.conf import settings
from django.core.paginator import Paginator


def index(request):
    title = 'Последние обновления на сайте'
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, settings.PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': title
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_list.html'
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, settings.PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    author = User.objects.get(username=username)
    template = 'posts/profile.html'
    posts = Post.objects.filter(author=author.id)
    paginator = Paginator(posts, settings.PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = posts.count()
    context = {
        'author': author,
        'page_obj': page_obj,
        'count': count
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    template = 'posts/post_detail.html'
    count = Post.objects.filter(author__username=post.author).count()
    context = {
        'post': post,
        'count': count
    }
    return render(request, template, context)


def post_create(request):
    template = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return HttpResponseRedirect(f'/profile/{request.user.username}/')
        return render(request, template, {'form': form})
    form = PostForm()
    return render(request, template, {'form': form})


def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    if post.author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(f'/profile/{request.user.username}/')
            return render(request, template, {'form': form, 'is_edit': is_edit})
    else:
        return HttpResponseRedirect(f'/posts/{post_id}/')
    form = PostForm(instance=post)
    return render(request, template, {'form': form})
