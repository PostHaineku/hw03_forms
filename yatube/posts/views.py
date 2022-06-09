from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Group
from django.core.paginator import Paginator
from .forms import New_post_form


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
    context = {
        'page_obj': page_obj,
    }

    return render(request, "posts/group_list.html", context)

def profile(request, username):
    posts_profile = Post.objects.select_related('author').filter(author__username=username)
    template = 'posts/profile.html'
    paginator = Paginator(posts_profile, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_cnt = Post.objects.filter(author__username=username).count()
    context = {
        'title': f'Профайл пользователя {username}',
        'page_obj': page_obj,
        'posts_profile': posts_profile,
        'posts_cnt': posts_cnt
    }
    return render(request, template, context)


def post_detail(request, post_id):
    id = post_id
    post = get_object_or_404(Post, pk=id)
    context = {
        'post': post
    }
    return render(request, 'posts/post_detail.html', context) 

def post_create(request):
    form = New_post_form(request.POST)
    if request.method == "POST":
        form = New_post_form(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            print('работает')
            return redirect("posts:profile", request.user.username)
        groups = Group.objects.all()
        context = {
            'form': form,
            'groups': groups
        }
        print(form.errors)
        return render(request, 'posts/create_post.html', context)
    form = New_post_form()
    groups = Group.objects.all()
    context = {
            'form': form,
            'groups': groups
        }
    print(form.errors)
    return render(request, 'posts/create_post.html', context)

def post_edit(request, post_id):
    is_edit = get_object_or_404(Post, post_id)
    if is_edit.author is request.user:
        if request.method == 'POST':
            form = New_post_form(request.POST or None, instance=is_edit)
            if form.is_valid():
                is_edit.save()
                return reverse('posts:post_detail', post_id=post_id)
            return render(request, 'posts/create_post.html', {'form':form})
    form = New_post_form(instance=is_edit)
    return render(request, 'posts/post_create.html', {'form':form})
