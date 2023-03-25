from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    def get_image_filename(instance, filename):
        return f"users/{instance.user.username}/photos/{filename}"
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to=get_image_filename, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user.username