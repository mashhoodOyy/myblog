from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post
from .forms import PostForm, SignupForm

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '🎉 Post created successfully!')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, '❌ You can only edit your own posts!')
        return redirect('post_list')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Post updated successfully!')
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, '❌ You can only delete your own posts!')
        return redirect('post_list')
    if request.method == 'POST':
        post.delete()
        messages.success(request, '🗑️ Post deleted successfully!')
        return redirect('post_list')
    return render(request, 'blog/post_delete.html', {'post': post})

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'🎉 Welcome, {user.username}! Account created successfully!')
            return redirect('post_list')
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'👋 Welcome back, {username}!')
            return redirect('post_list')
        else:
            messages.error(request, '❌ Invalid username or password!')
            return render(request, 'blog/login.html')
    return render(request, 'blog/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, '👋 Logged out successfully!')
    return redirect('post_list')