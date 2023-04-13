from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import Post
from .forms import PostForm
import random

# Create your views here.


@login_required(login_url='/login')
def post_page(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'post.html', {'post': post})


@login_required(login_url='/login')
def home(request):
    if request.method == 'GET':
        if request.path == '/latest':
            posts = Post.objects.all().order_by('-id')
        elif request.path == '/oldest':
            posts = Post.objects.all().order_by('id')
        else:
            posts = Post.objects.all().order_by('?')

    if request.method == 'POST':
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()

    return render(request, 'home.html', {'posts': posts})


@login_required(login_url='/login')
def profile(request, user_id):
    user_id = User.objects.get(username=user_id)
    friend = request.POST.get('friend')
    user_post = Post.objects.filter(author=user_id)
    friends_list = []
    randm = random.randint(1, 10)
    limit = 10

    if request.method == 'POST':
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()

    for x in range(limit):
        random_user_object = random.choice(User.objects.all())
        random_username = random_user_object.username
        if random_user_object == request.user:
            limit += 1
        else:
            if random_username not in friends_list:
                friends_list.append(random_username)
            else:
                limit += 1

    return render(request, 'profile.html', {'user_id': user_id,
                                            'friends_list': friends_list,
                                            'friend': friend,
                                            'user_post': user_post,
                                            'random': randm})


def sign_up(request):
    if request.method == 'POST':
        usr = request.POST
        username = usr['username']
        email = usr['email']
        password = usr['password']
        if User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists():
            messages.info(request, 'Username and Email Already exists')
            return redirect('/sign_up')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Already exists')
            return redirect('/sign_up')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'User Already exists')
            return redirect('/sign_up')
        else:
            usr_details = User.objects.create_user(
                username=username, email=email, password=password)
            usr_details.save()
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('/login')

    return render(request, 'registration/sign_up.html')


@login_required(login_url='/login')
def createpost(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/')
    else:
        form = PostForm()

    return render(request, 'create-post.html', {'form': form})
