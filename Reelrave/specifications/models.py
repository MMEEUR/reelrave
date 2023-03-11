from django.db import models
from django.utils.text import slugify

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True, editable=False)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class Country(models.Model):
    def get_image_filename(instance, filename):
        return f"countries/{instance.name}/{filename}"
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True, editable=False)
    flag = models.ImageField(upload_to=get_image_filename)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name