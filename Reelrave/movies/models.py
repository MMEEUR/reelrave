from django.db import models
from django.utils.text import slugify
from django.utils.functional import cached_property
from django.contrib.contenttypes.fields import GenericRelation
from persons.models import Person
from specifications.models import Genre, Country, Photo, Video, Comment, Rating

RATINGS = (
    ('G', 'G'),
    ('PG', 'PG'),
    ('PG-13', 'PG-13'),
    ('R', 'R'),
    ('NC-17', 'NC-17')
)


class Movie(models.Model):
    def get_baner_filename(instance, filename):
        return f"movies/{instance.name}/baners/{filename}"
    
    def get_trailer_filename(instance, filename):
        return f"movies/{instance.name}/trailer/{filename}"
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    baner = models.ImageField(upload_to=get_baner_filename)
    trailer = models.FileField(upload_to=get_trailer_filename, null=True, blank=True)
    release_date = models.DateField()
    time = models.DurationField()
    content_rating = models.CharField(max_length=5, choices=RATINGS)
    genre = models.ManyToManyField(Genre, related_name='genre_movies')
    director = models.ManyToManyField(Person, related_name='director_movies')
    writers = models.ManyToManyField(Person, related_name='writer_movies')
    actors = models.ManyToManyField(Person, related_name='actor_movies')
    description = models.CharField(max_length=250)
    storyline = models.TextField()
    country_of_origin = models.ManyToManyField(Country, related_name='country_movies')
    pictures = GenericRelation(Photo)
    videos = GenericRelation(Video)
    comments = GenericRelation(Comment)
    ratings = GenericRelation(Rating)
    
    class Meta:
        ordering = ('-release_date',)
        
    @cached_property
    def total_ratings(self):
        ratings_count = self.ratings.exclude(rating=0).count()
        
        return ratings_count if ratings_count else None
    
    @cached_property
    def average_rating(self):
        ratings = self.ratings.exclude(rating=0).all()
        
        if ratings:
            return ratings.aggregate(models.Avg('rating'))['rating__avg']
        
        else:
            return None
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name