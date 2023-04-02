from django.db import models
from django.utils.text import slugify
from django.utils.functional import cached_property
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model


class Photo(models.Model):
    def get_photo_filename(instance, filename):
        content_type_name = instance.content_type.model
        return f"{content_type_name.lower()}s/{instance.content_object.name}/photo/{filename}"

    title = models.CharField(max_length=30)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={"model__in": ('show', 'movie', 'episode')})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=get_photo_filename)
    released = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title


class Video(models.Model):
    def get_video_filename(instance, filename):
        content_type_name = instance.content_type.model
        return f"{content_type_name.lower()}s/{instance.content_object.name}/videos/{filename}"

    title = models.CharField(max_length=30)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={"model__in": ('show', 'movie', 'episode')})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    video = models.FileField(upload_to=get_video_filename, validators=[FileExtensionValidator(allowed_extensions=['mov', 'avi', 'mp4', 'webm', 'mkv'])])
    released = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.title} \"{self.content_object}\""


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_comments')
    body = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={"model__in": ('show', 'movie', 'episode')})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ('-updated',)
        
    @cached_property
    def likes_count(self):
        return self.comment_likes_dislikes.filter(like_or_dislike=True).count()
    
    @cached_property
    def dislikes_count(self):
        return self.comment_likes_dislikes.filter(like_or_dislike=False).count()
        
    def __str__(self) -> str:
        return f"{self.user} on {self.content_object}"
    
class CommentLikeDisLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes_dislikes')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_comment_like_dislikes')
    like_or_dislike = models.BooleanField()
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-updated',)
        unique_together = ('user', 'comment')
        verbose_name_plural = 'Comment Likes & Dislikes'
        
    @property
    def opinion(self):
        return "Liked" if self.like_or_dislike else "DisLiked"
    
    def __str__(self) -> str:
        return f"{self.user} {self.opinion} {self.comment}"


class Rating(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_ratings')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={"model__in": ('show', 'movie', 'episode')})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-updated',)
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self) -> str:
        return f"{self.user} {self.rating} for \"{self.content_object}\""
    
    
class WatchList(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='watchlist')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={"model__in": ('show', 'movie', 'episode')})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        unique_together = ('user', 'content_type', 'object_id')
        
    def __str__(self) -> str:
        return f"{self.user} added {self.content_object}"


class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=20, unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Country(models.Model):
    def get_country_filename(instance, filename):
        return f"countries/{instance.name}/{filename}"

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, editable=False)
    flag = models.ImageField(upload_to=get_country_filename)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name