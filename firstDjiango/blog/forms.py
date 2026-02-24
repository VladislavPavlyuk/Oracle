from django import forms
from blog.models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["author", "text"]
        widgets = {
            "author": forms.TextInput(attrs={"class": "form-control", "placeholder": "Author"}),
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Write your post"}),
        }
