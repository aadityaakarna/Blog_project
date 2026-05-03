from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from blog.models import Post
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}! Your account was created.')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    # This page will be your "Edit Profile" page (professional)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    post_count = Post.objects.filter(author=request.user).count() # if Post.author = User

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'post_count': post_count
    }
    return render(request, 'users/profile.html', context)

def public_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')
    post_count = posts.count()

    return render(request, 'users/public_profile.html', {
        'profile_user': profile_user,
        'posts': posts,
        'post_count': post_count,
    })