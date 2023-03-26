from django.db import models
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from persons.models import Person
from specifications.models import Genre, Country, Photo, Video, Comment

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

    def get_trailer_filename(instance, filename):
        return f"shows/{instance.name}/trailer/{filename}"

    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True, editable=False)
    baner = models.ImageField(upload_to=get_baner_filename)
    trailer = models.FileField(upload_to=get_trailer_filename, null=True, blank=True)
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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Season(models.Model):
    show = models.ForeignKey(
        Show, on_delete=models.CASCADE, related_name='seasons')
    number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('show', 'number')
        ordering = ['number']

    def __str__(self) -> str:
        return f"\"{self.show}\" Season {self.number}"


class Episode(models.Model):
    def get_baner_filename(instance, filename):
        return f"shows/{instance.season.show}/Season {instance.season.number}/Episode-{instance.number}/baner/{filename}"

    def get_trailer_filename(instance, filename):
        return f"shows/{instance.season.show}/Season {instance.season.number}/Episode-{instance.number}/trailer/{filename}"

    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name="episodes")
    number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)
    content_rating = models.CharField(max_length=5, choices=RATINGS)
    director = models.ManyToManyField(Person, related_name='director_episodes')
    writers = models.ManyToManyField(Person, related_name='writer_episodes')
    actors = models.ManyToManyField(Person, related_name='actor_episodes')
    genre = models.ManyToManyField(Genre, related_name='genre_episodes')
    time = models.DurationField()
    baner = models.ImageField(upload_to=get_baner_filename)
    trailer = models.FileField(upload_to=get_trailer_filename, null=True, blank=True)
    description = models.CharField(max_length=250)
    storyline = models.TextField()
    released = models.DateField()
    pictures = GenericRelation(Photo)
    videos = GenericRelation(Video)
    comments = GenericRelation(Comment)

    class Meta:
        unique_together = ('season', 'number')
        ordering = ['number']

    def __str__(self) -> str:
        return f"{self.season} Episode {self.number} \"{self.title}\""