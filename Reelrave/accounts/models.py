from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.files.images import ImageFile
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    def get_image_filename(instance, filename):
        return f"users/{instance.username}/photos/{filename}"

    email = models.EmailField(_("email address"))
    bio = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(
        upload_to=get_image_filename,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png"])],
    )

    @property
    def get_absolute_url(self):
        return reverse("accounts:global_profile", kwargs={"user_id": self.id})

    @property
    def comments_count(self):
        return self.user_comments.filter(active=True).count()

    def __str__(self) -> str:
        return self.username

    def clean(self):
        super().clean()

        if self.photo:
            try:
                image = ImageFile(self.photo)

                if image.width > 1920 or image.height > 1080:
                    raise ValidationError(
                        _("Image dimensions should not exceed 1920x1080.")
                    )

                if self.photo.size > 1024 * 1024 * 2:
                    raise ValidationError(_("Image size should not exceed 2 MB."))

            except OSError:
                raise ValidationError(_("Invalid image file."))