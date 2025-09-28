from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "title": "Post Title",
            "body": "Content",
            "published": "Publish Now",
        }
        help_texts = {
            "title": "Enter the title of your post.",
            "content": "Write the content of your post here.",
            "published": "Check to publish immediately.",
        }
        error_messages = {
            "title": {
                "max_length": "The title is too long.",
                "required": "The title field is required.",
            },
            "content": {
                "required": "The content field cannot be empty.",
            },
        }
    def clean_title(self):
        title = self.cleaned_data.get("title")
        if "badword" in title.lower():
            raise forms.ValidationError("Inappropriate word found in title.")
        return title