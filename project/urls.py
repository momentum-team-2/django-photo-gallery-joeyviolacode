"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from core import views as core_views
from api import views as api_views
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("registration.backends.simple.urls")),
    path('', core_views.ShowPhotos.as_view(), name="list_photos"),
    path('photo/add', core_views.AddPhoto.as_view(), name="add_photo"),
    path('photo/<int:pk>/delete', core_views.DeletePhoto.as_view(), name="delete_photo"),
    path('album/add/<int:pk>', core_views.CreateAlbum.as_view(), name="create_album"),
    path('album/<int:pk>', core_views.ShowAlbum.as_view(), name="show_album"),
    path('album/<int:pk>/edit', core_views.EditAlbum.as_view(), name="edit_album"),
    path('albums', core_views.ListAlbums.as_view(), name="list_albums"),
    path('photo/<int:pk>/add-comment', core_views.AddComment.as_view(), name="add_comment"),
    path('photo/<int:pk>/fave', core_views.FavoritePhoto.as_view(), name="photo_favorite"),
    path('album/<int:album_pk>/add-photo/<int:photo_pk>', core_views.TogglePhotoInAlbum.as_view(), name="a_r_photo"),
    path('photo/<int:pk>', core_views.ShowPhoto.as_view(), name="show_photo"),
    path('photo/<int:pk>/id/<int:photo_index>', core_views.ShowPhoto.as_view(), name="show_photo"),
    path('user/<int:pk>/photos', core_views.ShowUserPhotos.as_view(), name="show_user_photos"),
    path('user/<int:user_pk>/photo/<int:photo_pk>', core_views.ShowUserPhoto.as_view(), name="show_user_photo"),
    path('user/<int:user_pk>/photo/<int:photo_pk>/id/<int:photo_index>', core_views.ShowUserPhoto.as_view(), name="show_user_photo"),
    path('album/<int:album_pk>/photo/<int:photo_pk>/id/<int:photo_index>', core_views.ShowAlbumPhoto.as_view(), name="show_album_photo"),
    path('album/<int:album_pk>/photo/<int:photo_pk>', core_views.ShowAlbumPhoto.as_view(), name="show_album_photo"),
    path('api-auth/', include('rest_framework.urls')),
    path('api/photos', api_views.PhotosList.as_view(), name="api_show_photos"),
    path('api/photos/<int:pk>', api_views.PhotoDetail.as_view(), name="api_photo_detail"),
    path('api/albums', api_views.AlbumsList.as_view(), name='api_show_albums'),
    path('api/albums/<int:pk>', api_views.AlbumDetail.as_view(), name="api_album_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
