from django.db import models
from users.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit


# Create your models here.
class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photos")
    favorited_by = models.ManyToManyField(User, related_name="favorites")
    caption = models.TextField()
    uploaded_on = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    
    photo = models.ImageField(upload_to="photos/", null=True, blank=True,)
    photo_thumbnail = ImageSpecField(
        source="photo",
        processors=[ResizeToFit(200, 200)],
        format="JPEG",
        options={"quality": 60},
    )
    photo_medium = ImageSpecField(
        source="photo",
        processors=[ResizeToFit(400, 400)],
        format="JPEG",
        options={"quality": 80},
    )
    photo_large = ImageSpecField(
        source="photo",
        processors=ResizeToFit(600, 600),
        format="JPEG",
        options={"quality": 95},
    )


class Album(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="albums")
    photos = models.ManyToManyField(Photo, related_name="albums")
    cover_photo = models.ForeignKey(Photo, on_delete=models.DO_NOTHING, related_name="cover_for")
    title = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="comments")
    created_on = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

