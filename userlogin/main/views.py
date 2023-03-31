from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Post
from .forms import PostForm
# Create your views here.


@login_required(login_url='/login')
def home(request):
    posts = Post.objects.all()

    if request.method == 'POST':
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()

    return render(request, 'home.html', {'posts': posts})


@login_required(login_url='/login')
def profile(request):
    return render(request, 'profile.html')


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
            if user is not None:
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
