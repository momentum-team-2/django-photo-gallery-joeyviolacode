from django.db import models
from users.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Transpose

#Keep transpose in?  I don't know....
# Create your models here.
class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="photos")
    favorited_by = models.ManyToManyField(User, related_name="favorites", blank=True)
    title = models.CharField(max_length=255)
    caption = models.TextField(null=True, blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)
    
    photo = models.ImageField(upload_to="photos/", null=True, blank=True,)
    photo_thumbnail = ImageSpecField(
        source="photo",
        processors=[ResizeToFit(200, 200)],
        format="JPEG",
        options={"quality": 85},
    )
    photo_medium = ImageSpecField(
        source="photo",
        processors=[ResizeToFit(300, 300)],
        format="JPEG",
        options={"quality": 90},
    )
    photo_large = ImageSpecField(
        source="photo",
        processors=[ResizeToFit(800, 800)],
        format="JPEG",
        options={"quality": 100},
    )

    def __str__(self):
        return f'{self.title} by {self.owner.username}'


class Album(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="albums")
    photos = models.ManyToManyField(Photo, related_name="albums")
    cover_photo = models.ForeignKey(Photo, on_delete=models.DO_NOTHING, related_name="cover_for", null=True)
    title = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name="comments")
    created_on = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return f'{self.owner.username} on {self.photo}'

