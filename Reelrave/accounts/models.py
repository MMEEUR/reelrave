from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from movies.models import Movie
from shows.models import Show

# Create your models here.
class Profile(models.Model):
    def get_image_filename(instance, filename):
        return f"users/{instance.user.username}/photos/{filename}"
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to=get_image_filename)
    favorite_movies = models.ManyToManyField(Movie, related_name="movie_fans")
    favorite_shows = models.ManyToManyField(Show, related_name='show_fans')
    
    def __str__(self) -> str:
        return self.user.username
    
class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_comments')
    body = models.TextField()
    email = models.EmailField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    active = models.BooleanField(default=False)