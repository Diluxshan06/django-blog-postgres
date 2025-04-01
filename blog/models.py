from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.


#category
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    img = models.ImageField(null=True, upload_to='post/images/')
    create_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    
    def formated_img(self):
        img = self.img if self.img.__str__().startswith(('http','https')) else self.img.url
        return img
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
   

class About_us(models.Model):
    content = models.TextField()
