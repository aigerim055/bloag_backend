from django.contrib import admin
from .models import (
    Post, 
    Rating, 
    Tag, 
    PostImage, 
    Like
)


admin.site.register([Post, Tag, Rating, PostImage, Like])