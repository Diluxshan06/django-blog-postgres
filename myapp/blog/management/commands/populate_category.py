from blog.models import Post, Category
from django.core.management.base import BaseCommand
from typing import Any

        
class Command(BaseCommand):
    help = 'Populate category'
    
    def handle(self, *args, **kwargs):
        Category.objects.all().delete()
        
        Categories = ['Sports', 'Technology', 'Science', 'Art', 'Food']
        
        for category in Categories:
            Category.objects.create(name=category)
        
        self.stdout.write(self.style.SUCCESS("Category populated successfully!"))
        