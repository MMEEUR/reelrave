from django.db import models

# Create your models here.
class Person(models.Model):
    ROLES = (('Director', 'Director'), ('Actor', 'Actor'), ('Writer', 'Writer'))
    
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=8, choices=ROLES)
    birthday = models.DateField()
    height_centimeter = models.DecimalField(max_digits=3, decimal_places=0)
    picture = models.ImageField(upload_to="actors/")
    
    def __str__(self):
        return self.name