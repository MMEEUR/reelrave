from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):  
    role = models.CharField(max_length=20, verbose_name=_("Role"))
    
    class Meta:
        verbose_name_plural = _("Roles")
    
    def __str__(self):
        return self.role
    
    
class Person(models.Model):
    def get_image_filename(instance, filename):
        return f"presons/{instance.name}/pictures/{filename}"
    
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    birthday = models.DateField(verbose_name=_("Birthday"))
    height_centimeter = models.DecimalField(max_digits=3, decimal_places=0, verbose_name=_("Height (cm)"))
    picture = models.ImageField(upload_to=get_image_filename, verbose_name=_("Picture"))
    roles = models.ManyToManyField(Role, related_name='persons', related_query_name='persons')
    
    class Meta:
        verbose_name_plural = _("Persons")
    
    def __str__(self):
        return self.name