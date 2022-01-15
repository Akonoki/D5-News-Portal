from django.forms import ModelForm
from .models import Post, Category, Author


class NewsForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category_type', 'author_relation', 'post_category_relation']