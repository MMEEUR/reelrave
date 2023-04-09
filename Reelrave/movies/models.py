from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.functional import cached_property
from django.contrib.contenttypes.fields import GenericRelation
from persons.models import Person
from specifications.models import Genre, Country, Photo, Video, Comment, Rating, WatchList

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
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    baner = models.ImageField(upload_to=get_baner_filename)
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
    watchlist = GenericRelation(WatchList)
    
    class Meta:
        ordering = ('-release_date',)
        
    @property
    def get_absolute_url(self):
        return reverse("movies:movie_detail", kwargs={"slug": self.slug})
    
    @property
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
        
    average_rating.cache_timeout = 86400
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name