from django.db import models

# Create your models here.
class Person(models.Model):
    def get_image_filename(instance, filename):
        return f"presons/{instance.name}/pictures/{filename}"
    
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    height_centimeter = models.DecimalField(max_digits=3, decimal_places=0)
    picture = models.ImageField(upload_to=get_image_filename)
    
    def __str__(self):
        return self.name
    
class Role(models.Model):  
    person = models.ManyToManyField(Person, related_name='roles')
    role = models.CharField(max_length=20)
    
    def __str__(self):
        return self.role