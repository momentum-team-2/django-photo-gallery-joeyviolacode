from django.shortcuts import render
from .serializers import PhotoSerializer, AlbumSerializer, CommentSerializer
from core.models import Photo, Album, Comment
from users.models import User
from rest_framework import generics, permissions, status


# Create your views here.
class PhotosList(generics.ListAPIView):
    queryset = Photo.objects.all().filter(is_public=True)
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]


class PhotoDetail(generics.RetrieveAPIView):
    queryset = Photo.objects.all().filter(is_public=True)
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]


class AlbumsList(generics.ListAPIView):
    queryset = Album.objects.all().filter(is_public=True)
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]


class AlbumDetail(generics.RetrieveAPIView):
    queryset = Album.objects.all().filter(is_public=True)
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated]