from django import forms
from django.forms import ModelForm

from apps.blog.models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

