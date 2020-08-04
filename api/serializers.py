from rest_framework import serializers
from core.models import Comment, Photo, Album
from users.models import User

class PhotoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    comments = serializers.StringRelatedField(many=True, read_only=True)
    favorited_by = serializers.StringRelatedField(many=True, read_only=True)

    class Meta: 
        model = Photo
        fields = [
            "owner",
            "favorited_by",
            "title",
            "caption",
            "uploaded_on",
            "is_public",
            "is_pinned",
            "photo",
            "comments",
        ]


class AlbumSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    photos = PhotoSerializer(many=True, read_only=True)
    cover_photo = PhotoSerializer(read_only=True)

    class Meta:
        model = Album
        fields = [
            "title",
            "owner",
            "cover_photo",
            "photos",
            "is_public",
        ]


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    photo = PhotoSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "owner",
            "photo",
            "body", 
            "created_on",
        ]