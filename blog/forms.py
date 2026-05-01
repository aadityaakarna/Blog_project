from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):
  class Meta:
    model=Post
    fields=['title','content']

class CommentForm(forms.ModelForm):
  class Meta:
    model=Comment
    fields=['content']

  def clean_content(self):
    data=self.cleaned_data['content']
    if not data.strip():
      raise forms.ValidationError('Comments cannot be empty')
    return data

