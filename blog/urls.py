from django.urls import path
from . import views
from .views import PostUpdateView, PostDeleteView

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/new/', views.post_create, name='post-create'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:pk>/like/', views.like_post, name='post-like'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]