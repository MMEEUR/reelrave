from django.urls import path
from .views import (
    GenreDetailView, GenreListView,
    CountryListView, CountryDetailView,
    UpdateDeleteCommentView, UpdateDeleteRatingView, CommentLikeDisLikeView
)

app_name = 'spec'

urlpatterns = [
    path('genres/', GenreListView.as_view(), name='genres'),
    path('genres/<slug:slug>/', GenreDetailView.as_view(), name='genre_detail'),
    path('countries/', CountryListView.as_view(), name='countries'),
    path('countries/<slug:slug>/', CountryDetailView.as_view(), name='country_detail'),
    path('comment/<int:comment_id>/', UpdateDeleteCommentView.as_view(), name='comment_update_delete'),
    path('comment/<int:comment_id>/like_or_dislike/', CommentLikeDisLikeView.as_view(), name='comment_like_or_dislike'),
    path('rating/<int:rating_id>/', UpdateDeleteRatingView.as_view(), name='rating_update_delete'),
]