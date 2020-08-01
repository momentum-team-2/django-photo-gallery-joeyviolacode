from django.shortcuts import render
from .models import Album, Comment, Photo
from .forms import AlbumForm, CommentForm, PhotoForm
from users.models import User
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse



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


class ShowPhoto(View):

    def get(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        return render(request, "core/show_photo.html", {"photo": photo})

    

#  Change this to start from a picture, so that picture can be the cover.  Need to add PK later.
class CreateAlbum(View):
    
    def get(self, request):
        form = AlbumForm()
        return render(request, 'core/create_album.html', {"form" : form})

    def post(self, request):
        form = AlbumForm(data=request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = request.user
            album.save()
            pk = album.pk
        return redirect(to="show_album", pk=pk)


class ShowAlbum(View):
    
    def get(self, request, pk):
        album = get_object_or_404(Album, pk=pk)
        photos = Photo.objects.all().filter(owner=request.user).order_by("-uploaded_on")
        return render(request, "core/show_album.html", {"album": album, "photos": photos})


@method_decorator(csrf_exempt, name="dispatch")
class TogglePhotoInAlbum(View):
    def post(self, request, album_pk, photo_pk):
        album = get_object_or_404(Album, pk=album_pk)
        photo = get_object_or_404(Photo, pk=photo_pk)
        if photo in album.photos.all():
            album.photos.remove(photo)
            return JsonResponse({"inAlbum": False})
        else:
            album.photos.add(photo)
            return JsonResponse({"inAlbum": True})



class ShowUserPhotos(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        photos = user.photos.all().order_by("-uploaded_on")
        return render(request, "core/show_user_photos.html", {"photos":photos})