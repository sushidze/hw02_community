from django.shortcuts import render, get_object_or_404
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
    author = get_object_or_404(User, username=username)
    template = 'posts/profile.html'
    posts = author.posts.all()
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
    count = Post.objects.filter(author__username=post.author).count()
    context = {
        'post': post,
        'count': count
    }
    return render(request, 'posts/post_detail.html', context)
