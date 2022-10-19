from django.contrib import admin

from network.models import Follow, Like, Post

admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Like)
