from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.files.images import ImageFile
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from PIL import Image


class Profile(models.Model):
    def get_image_filename(instance, filename):
        return f"users/{instance.user.username}/photos/{filename}"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to=get_image_filename, null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])
    
    @cached_property
    def comments_count(self):
        return self.user.user_comments.filter(active=True).count()

    def __str__(self) -> str:
        return self.user.username
    
    def clean(self):
        super().clean()
        
        if self.photo:
            try:
                image = ImageFile(self.photo)
                
                if image.width > 1920 or image.height > 1080:
                    raise ValidationError(_('Image dimensions should not exceed 1920x1080.'))
                
                if self.photo.size > 1024*1024*2:
                    raise ValidationError(_('Image size should not exceed 2 MB.'))
                
            except OSError:
                raise ValidationError(_('Invalid image file.')) 
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.photo:
            image = ImageFile(self.photo)
            
            if image.width > 1920 or image.height > 1080:
                image.thumbnail((1920, 1080), resample=Image.LANCZOS)
                image.save(self.photo.path)