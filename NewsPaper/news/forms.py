from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=200)

    class Meta:
        model = Post
        fields = [
            'author',
            'category',
            'title',
            'text',
        ]