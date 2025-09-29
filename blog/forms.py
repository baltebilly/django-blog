from django import forms
from .models import Post
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        remove_avatar = forms.BooleanField(required=False, initial=False, label="Remove current profile picture")
        fields = ["bio", "avatar", "website", "location", "birth_date", "remove_avatar"]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "remove_avatar": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "bio": "Biography",
            "avatar": "Profile Picture",
            "website": "Website",
            "location": "Location",
            "birth_date": "Birth Date",
            "remove_avatar": "Remove Profile Picture",
        }
        help_texts = {
            "bio": "Write a short biography about yourself.",
            "avatar": "Upload a profile picture.",
            "website": "Enter your personal or professional website.",
            "location": "Where are you located?",
            "birth_date": "Your date of birth.",
            "remove_avatar": "Check this box to remove your current profile picture.",

        }
        error_messages = {
            "website": {
                "invalid": "Enter a valid URL.",
            },
            "birth_date": {
                "invalid": "Enter a valid date.",
            },
        }

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