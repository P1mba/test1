from django import forms
from .models import Articles

class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'text', 'image', 'file', 'category', 'slug']