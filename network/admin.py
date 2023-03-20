from django.contrib import admin
from network.models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("followers",)

class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ("users_liked",)

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)