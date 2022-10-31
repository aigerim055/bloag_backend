from django.contrib import admin
from .models import (
    Post, 
    Rating, 
    Tag, 
    PostImage, 
    Like
)


admin.site.register([Tag, Rating, Like])


class TabularInlineImages(admin.TabularInline):
    model = PostImage
    extra = 3
    fields = ['image']


class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = [TabularInlineImages]


admin.site.register(Post, PostAdmin)