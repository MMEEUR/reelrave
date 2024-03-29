from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.functional import cached_property
from django.contrib.contenttypes.fields import GenericRelation
from persons.models import Person
from specifications.models import Genre, Country, Photo, Video, Comment, Rating, WatchList

RATINGS = (
    ('TV-Y', 'TV-Y'),
    ('TV-Y7', 'TV-Y7'),
    ('TV-G', 'TV-G'),
    ('TV-PG', 'TV-PG'),
    ('TV-14', 'TV-14'),
    ('TV-MA', 'TV-MA')
)


class Show(models.Model):
    def get_baner_filename(instance, filename):
        return f"shows/{instance.name}/baners/{filename}"

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    baner = models.ImageField(upload_to=get_baner_filename)
    release_date = models.DateField()
    ending_date = models.DateField(null=True)
    content_rating = models.CharField(max_length=5, choices=RATINGS)
    genre = models.ManyToManyField(Genre, related_name='genre_shows')
    creators = models.ManyToManyField(Person, related_name='creators_shows')
    actors = models.ManyToManyField(Person, related_name='actor_shows')
    description = models.CharField(max_length=250)
    storyline = models.TextField()
    country_of_origin = models.ManyToManyField(Country, related_name='country_shows')
    pictures = GenericRelation(Photo)
    videos = GenericRelation(Video)
    comments = GenericRelation(Comment)
    ratings = GenericRelation(Rating)
    watchlist = GenericRelation(WatchList)
    
    class Meta:
        ordering = ('-release_date',)
        
    @property
    def season_count(self):
        return self.seasons.count()
    
    @property
    def episode_count(self):
        episode_count = 0
        
        for season in self.seasons.all():
            episode_count += season.episodes.count()
            
        return episode_count
    
    @property
    def get_absolute_url(self):
        return reverse("shows:show_detail", kwargs={"slug": self.slug})
    
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

    def __str__(self) -> str:
        return self.name
    

class Season(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='seasons')
    number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('show', 'number')
        ordering = ['number']

    def __str__(self) -> str:
        return f"'{self.show}' Season {self.number}"


class Episode(models.Model):
    def get_baner_filename(instance, filename):
        return f"shows/{instance.season.show}/Season {instance.season.number}/Episode-{instance.number}/baner/{filename}"

    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")
    number = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=100)
    content_rating = models.CharField(max_length=5, choices=RATINGS)
    director = models.ManyToManyField(Person, related_name='director_episodes')
    writers = models.ManyToManyField(Person, related_name='writer_episodes')
    actors = models.ManyToManyField(Person, related_name='actor_episodes')
    genre = models.ManyToManyField(Genre, related_name='genre_episodes')
    time = models.DurationField()
    baner = models.ImageField(upload_to=get_baner_filename)
    description = models.CharField(max_length=250)
    storyline = models.TextField()
    release_date = models.DateField()
    pictures = GenericRelation(Photo)
    videos = GenericRelation(Video)
    comments = GenericRelation(Comment)
    ratings = GenericRelation(Rating)
    watchlist = GenericRelation(WatchList)
    
    class Meta:
        unique_together = ('season', 'number')
        ordering = ('release_date',)
        
    @property
    def title(self):
        return f"{self.season} Episode {self.number} '{self.name}'"
        
    @property
    def get_absolute_url(self):
        return reverse("shows:episode_detail", kwargs={"slug": self.season.show.slug, "episode_id": self.id})
    
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

    def __str__(self) -> str:
        return f"{self.season} Episode {self.number} \"{self.name}\""