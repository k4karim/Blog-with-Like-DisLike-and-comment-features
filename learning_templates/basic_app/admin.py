from django.contrib import admin

# Register your models here.
from .models import Post,Comment,UserProfileInfo,Upvotes,Downvotes

admin.site.register(Post)

admin.site.register(Comment)

admin.site.register(UserProfileInfo)

admin.site.register(Upvotes)

admin.site.register(Downvotes)
