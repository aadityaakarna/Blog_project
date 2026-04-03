from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
  title=models.CharField(max_length=100)
  content=models.TextField()
  author=models.ForeignKey(User,on_delete=models.CASCADE)
  created_at=models.DateTimeField(auto_now_add=True)

  def get_absolute_url(self):
    return reverse('post-detail',kwargs={'pk':self.pk})

  def __str__(self):
    return self.title

class Comment(models.Model):
  post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  content=models.TextField()
  created_at=models.DateTimeField(auto_now_add=True)
   
  def __str__(self):
    return f'Comment by {self.user}'
  
class Like(models.Model):
  post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='Likes')
  user=models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    unique_together=('post','user')

  def __str__(self):
    return f'{self.user} likes {self.post}'