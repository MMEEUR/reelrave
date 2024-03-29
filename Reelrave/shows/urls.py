from django.urls import path
from .views import (
    ShowListView,
    ShowDetailView,
    ShowCreateCommentView,
    ShowRatingView,
    ShowWatchListView,
    EpisodeListView,
    EpisodeDetailView,
    EpisodeCreateCommentView,
    EpisodeRatingView,
    EpisodeWatchListView,
    ShowGenreView,
    ShowCountryView,
    TopShowsView,
)

app_name = 'shows'

urlpatterns = [
    path('', ShowListView.as_view(), name='show_list'),
    path('top/', TopShowsView.as_view(), name='top_shows'),
    path('top/<slug:genre>/', TopShowsView.as_view(), name='top_shows_by_genre'),
    path('<slug:slug>/', ShowDetailView.as_view(), name='show_detail'),
    path('<slug:slug>/comment/', ShowCreateCommentView.as_view(), name='show_create_comment'),
    path('<slug:slug>/rating/', ShowRatingView.as_view(), name='show_rating'),
    path('<slug:slug>/watchlist/', ShowWatchListView.as_view(), name='show_watchlist'),
    path('<slug:slug>/episodes/', EpisodeListView.as_view(), name='episode_list'),
    path('<slug:slug>/episodes/<int:episode_id>/', EpisodeDetailView.as_view(), name='episode_detail'),
    path('<slug:slug>/episodes/<int:episode_id>/comment/', EpisodeCreateCommentView.as_view(), name='episode_create_comment'),
    path('<slug:slug>/episodes/<int:episode_id>/rating/', EpisodeRatingView.as_view(), name='episode_rating'),
    path('<slug:slug>/episodes/<int:episode_id>/watchlist/', EpisodeWatchListView.as_view(), name='episode_watchlist'),
    path('genre/<slug:genre>/', ShowGenreView.as_view(), name='show_by_genre'),
    path('country/<slug:country>/', ShowCountryView.as_view(), name='show_by_country'),
]