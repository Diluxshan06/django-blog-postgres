from django.contrib import admin
from .models import Post, Category, About_us


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    

# Register your models here.
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(About_us)
