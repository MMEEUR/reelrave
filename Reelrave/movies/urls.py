from django.urls import path
from .views import (
MovieListView, MovieDetailView, 
MovieCreateCommentView, MovieRatingView, MovieWatchListView,
MovieGenreView, MovieCountryView
)

app_name = 'movies'

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('<slug:slug>/comment/', MovieCreateCommentView.as_view(), name='movie_create_comment'),
    path('<slug:slug>/rating/', MovieRatingView.as_view(), name='movie_rating'),
    path('<slug:slug>/watchlist/', MovieWatchListView.as_view(), name='movie_watchlist'),
    path('genre/<slug:genre>/', MovieGenreView.as_view(), name='movie_by_genre'),
    path('country/<slug:country>/', MovieCountryView.as_view(), name='movie_by_country'),
]