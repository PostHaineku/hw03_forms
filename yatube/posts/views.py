from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group
from django.core.paginator import Paginator
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all().order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = group.title
    description = group.description
    context = {
        'page_obj': page_obj,
        'title': title,
        'description': description
    }

    return render(request, "posts/group_list.html", context)


def profile(request, username):
    posts_profile = (Post.objects.select_related('author')
                     .filter(author__username=username))
    author = get_object_or_404(User, username=username)
    template = 'posts/profile.html'
    paginator = Paginator(posts_profile, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_cnt = Post.objects.filter(author__username=username).count()
    context = {
        'username': username,
        'page_obj': page_obj,
        'posts_profile': posts_profile,
        'posts_cnt': posts_cnt,
        'author': author
    }
    return render(request, template, context)


def post_detail(request, post_id):
    id = post_id
    post = get_object_or_404(Post, pk=id)
    context = {
        'post': post
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            author = request.user.username
            return redirect("posts:profile", author)
        groups = Group.objects.all()
        context = {
            'form': form,
            'groups': groups
        }
        return render(request, 'posts/create_post.html', context)
    form = PostForm()
    groups = Group.objects.all()
    context = {
        'form': form,
        'groups': groups
    }
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST or None, instance=post)
            is_edit = True
            context = {
                'form': form,
                'is_edit': is_edit,
                'id': post_id,
            }
            if form.is_valid():
                form.save()
                return redirect('posts:post_detail', post_id=post_id)
            return render(request, 'posts/create_post.html', context)
        form = PostForm(instance=post)
        is_edit = True
        context = {
            'form': form,
            'is_edit': is_edit,
            'id': post_id
        }
        return render(request, 'posts/create_post.html', context)
    return redirect('posts:post_detail', post_id=post_id)
