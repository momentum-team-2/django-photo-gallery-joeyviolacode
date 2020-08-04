from django.forms import ModelForm, Textarea
from .models import Album, Photo, Comment

class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = [
            "title"
        ]

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = [
            "title",
            "caption",
            "is_public",
            "is_pinned",
            "photo",
        ]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            "body",
        ]
        widgets = {
          'body': Textarea(attrs={'rows':4, 'cols':50},),
        }
        labels = {
            "body": ""
        }