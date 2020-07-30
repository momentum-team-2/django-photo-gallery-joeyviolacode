from django.forms import ModelForm
from .models import Album, Photo, Comment

class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = [
            
        ]

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = [

        ]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            
        ]