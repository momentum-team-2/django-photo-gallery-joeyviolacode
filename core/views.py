from django.shortcuts import render
from .models import Album, Comment, Photo
from .forms import AlbumForm, CommentForm, PhotoForm
from users.models import User
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def find_prev_and_next_index(queryset, current_index):
        set_size = len(queryset)        
        if current_index == 0:
            prev_index = set_size - 1
        else:
            prev_index = current_index - 1
        next_index = (current_index + 1) % set_size
        return prev_index, next_index


def filter_visible_photos(queryset, request):
    if request.user.is_authenticated:
        photos = queryset.filter(Q(owner=request.user)| Q(is_public = True)).order_by("-uploaded_on")
    else: 
        photos = queryset.filter(is_public=True)
    return photos


# Create your views here.
class ShowPhotos(View):
    def get(self, request):
        user = request.user
        photos = filter_visible_photos(Photo.objects.all(), request)
        return render(request, 'core/index.html', {"photos" : photos})


@method_decorator(login_required, name="dispatch")
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
    def get(self, request, pk, photo_index=None):
        photo = get_object_or_404(Photo, pk=pk)
        photos = filter_visible_photos(Photo.objects.all(), request)
        if photo_index == None:
            photo_index = list(photos).index(photo)
        photo = photos[photo_index]
        form = CommentForm()
        prev_index, next_index = find_prev_and_next_index(photos, photo_index)
        return render(request, "core/show_photo.html", 
                    {"photo": photo, 
                     "prev_index" : prev_index,
                     "next_index" : next_index,
                     "photo_index": photo_index,
                     "form": form})


#can be reorganized a bit regarding initial pk and the None check
class ShowAlbumPhoto(View):
    #  list(photos).index(photo)
    def get(self, request, album_pk, photo_pk, photo_index=None):
        photo = get_object_or_404(Photo, pk=photo_pk)
        album = get_object_or_404(Album, pk=album_pk)
        photos = filter_visible_photos(album.photos.all(), request)
        if photo_index == None:
            photo_index=list(photos).index(photo)
        photo = photos[photo_index]
        form = CommentForm()
        prev_index, next_index = find_prev_and_next_index(photos, photo_index)
        return render(request, 'core/show_album_photo.html', 
                    {"album": album,
                     "photo": photo,
                     "prev_index" : prev_index,
                     "next_index" : next_index,
                     "photo_index": photo_index,
                     "form": form})


class ShowUserPhoto(View):
    def get(self, request, user_pk, photo_pk, photo_index=None):
        photo = get_object_or_404(Photo, pk=photo_pk)
        user = get_object_or_404(User, pk=user_pk)
        photos = filter_visible_photos(user.photos.all(), request)
        if photo_index == None:
            photo_index=list(photos).index(photo)
        photo = photos[photo_index]
        form = CommentForm()
        prev_index, next_index = find_prev_and_next_index(photos, photo_index)
        return render(request, 'core/show_user_photo.html', 
                    {"user": user,
                     "photo": photo,
                     "prev_index" : prev_index,
                     "next_index" : next_index,
                     "photo_index": photo_index,
                     "form": form})


@method_decorator(login_required, name="dispatch")
class DeletePhoto(View):
    def get(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        if request.user == photo.owner:
            photo.delete()
            return redirect(to="show_user_photos", pk=request.user.pk)
        else: 
            return redirect(to="show_photo", pk=pk)


@method_decorator(login_required, name="dispatch")
class CreateAlbum(View): 
    def get(self, request, pk):
        form = AlbumForm()
        photo = get_object_or_404(Photo, pk=pk)
        if bool(Photo.objects.filter(owner=request.user, pk=pk).count()):
            return render(request, 'core/create_album.html', {"form" : form, "photo": photo})
        else: 
            return redirect(to="show_photo", pk=pk)

    def post(self, request, pk):
        form = AlbumForm(data=request.POST)
        photo = get_object_or_404(Photo, pk=pk)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = request.user
            album.cover_photo = photo
            album.save()
            album.photos.add(photo)
            album.save()
        return redirect(to="show_album", pk=album.pk)


class EditAlbum(View):
    def get(self, request, pk):
        album = get_object_or_404(Album, pk=pk)
        if request.user == album.owner:
            photos = Photo.objects.all().filter(owner=request.user).order_by("-uploaded_on")
            return render(request, "core/edit_album.html", {"album": album, "photos": photos})
        else:
            return redirect(to="show_album", pk=pk)


class ShowAlbum(View):
    def get(self, request, pk):
        album = get_object_or_404(Album, pk=pk)
        if request.user.is_authenticated:
            photos = album.photos.all().filter(Q(owner=request.user)| Q(is_public = True)).order_by("-uploaded_on")
        else:
            photos = album.photos.all().filter(is_public = True).order_by("-uploaded_on")
        return render(request, "core/show_album.html", {"album": album, "photos": photos})


class ListAlbums(View):
    def get(self, request):
        albums = Album.objects.all()
        return render(request, 'core/list_albums.html', {"albums": albums})


@method_decorator(login_required, name="dispatch")
@method_decorator(csrf_exempt, name="dispatch")
class TogglePhotoInAlbum(View):
    def post(self, request, album_pk, photo_pk):
        album = get_object_or_404(Album, pk=album_pk)
        photo = get_object_or_404(Photo, pk=photo_pk)
        if request.user == album.owner:
            if photo in album.photos.all():
                album.photos.remove(photo)
                return JsonResponse({"inAlbum": False})
            else:
                album.photos.add(photo)
                return JsonResponse({"inAlbum": True})
        else:
            return redirect(to="show_album", pk=album_pk)


@method_decorator(csrf_exempt, name="dispatch")
class FavoritePhoto(View):
    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        user = request.user
        if photo in user.favorites.all():
            user.favorites.remove(photo)
            return JsonResponse({"favorite": False})
        else:
            user.favorites.add(photo)
            return JsonResponse({"favorite": True})

@method_decorator(login_required, name="dispatch")
class AddComment(View):
    def post(self, request, pk):
        photo = get_object_or_404(Photo, pk=pk)
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.owner = request.user
            comment.save()
            return redirect(to="show_photo", pk=pk)


class ShowUserPhotos(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        photos = filter_visible_photos(user.photos.all(), request)
        albums = user.albums.all()
        return render(request, "core/show_user_photos.html", {"photos":photos, "albums": albums})