from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Like, Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog-home')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = request.user

    like, created = Like.objects.get_or_create(post=post, user=user)

    if not created:
        like.delete()

    return redirect('post-detail', pk=post.id)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    comments = post.comments.all()

    # 🔥 Like status
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()

    # 🔥 Comment handling
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                return redirect('post-detail', pk=post.id)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'is_liked': is_liked
    }

    return render(request, 'blog/post_detail.html', context)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog-home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()