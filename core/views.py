from django.shortcuts import render
from .models import Album, Comment, Photo
from .forms import AlbumForm, CommentForm, PhotoForm
from users.models import User
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
class ShowPhotos(View):
        
    def get(self, request):
        user = request.user
        photos = Photo.objects.all().order_by("-uploaded_on")
        return render(request, 'core/index.html', {"photos" : photos})


class AddPhoto(View):
    
    def get(self, request):
        form = PhotoForm()
        return render(request, 'core/add_photo.html', {"form" : form})

    def post(self, request):
        form = PhotoForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.save()
        return redirect(to="list_photos")