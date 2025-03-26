from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    

# Register your models here.
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
