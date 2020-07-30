from django.contrib import admin
from .models import Photo, Album, Comment

# Register your models here.
admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(Comment)