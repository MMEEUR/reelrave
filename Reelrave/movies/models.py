from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from persons.models import Person
from specifications.models import Genre, Country

# Create your models here.
class Movie(models.Model):
    def get_image_filename(instance, filename):
        return f"movies/{instance.name}/baners/{filename}"
    
    RATINGS = (('G', 'G'), ('PG', 'PG'), ('PG-13', 'PG-13'), ('R', 'R'), ('NC-17', 'NC-17'))
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True, editable=False)
    baner = models.ImageField(upload_to=get_image_filename)
    release_date = models.DateTimeField()
    time = models.DurationField()
    content_rating = models.CharField(max_length=5, choices=RATINGS)
    genre = models.ManyToManyField(Genre, related_name='genre_movies')
    director = models.ManyToManyField(Person, related_name='director_movies')
    writers = models.ManyToManyField(Person, related_name='writer_movies')
    actors = models.ManyToManyField(Person, related_name='actor_movies')
    description = models.CharField(max_length=250)
    storyline = models.TextField()
    country_of_origin = models.ManyToManyField(Country, related_name='country_movies')
    
    class Meta:
        ordering = ('-release_date',)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class Picture(models.Model):
    def get_image_filename(instance, filename):
        return f"movies/{instance.movie.name}/pictures/{filename}"
    
    title = models.CharField(max_length=30)
    movie = models.ForeignKey(Movie, related_name='pictures', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename)
    released = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return self.title

class Trailer(models.Model):
    def get_video_filename(instance, filename):
        return f"movies/{instance.movie.name}/trailers/{filename}"
    
    title = models.CharField(max_length=30)
    movie = models.ForeignKey(Movie, related_name='trailers', on_delete=models.CASCADE)
    video = models.FileField(upload_to=get_video_filename, validators=[FileExtensionValidator(allowed_extensions=['mov','avi','mp4','webm','mkv'])])
    released = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return self.title