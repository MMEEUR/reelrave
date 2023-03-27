from django.urls import path
from .views import (
    ShowListView,
    ShowDetailView,
    ShowCreateCommentView,
    ShowCreateRatingView,
    EpisodeListView,
    EpisodeDetailView,
    EpisodeCreateCommentView,
    EpisodeCreateRatingView,
)

app_name = 'shows'

urlpatterns = [
    path('', ShowListView.as_view(), name='show_list'),
    path('<slug:slug>/', ShowDetailView.as_view(), name='show_detail'),
    path('<slug:slug>/comment/', ShowCreateCommentView.as_view(), name='show_create_comment'),
    path('<slug:slug>/rating/', ShowCreateRatingView.as_view(), name='show_create_rating'),
    path('<slug:slug>/episodes/', EpisodeListView.as_view(), name='episode_list'),
    path('<slug:slug>/episodes/<int:episode_id>/', EpisodeDetailView.as_view(), name='episode_detail'),
    path('<slug:slug>/episodes/<int:episode_id>/comment/', EpisodeCreateCommentView.as_view(), name='episode_create_comment'),
    path('<slug:slug>/episodes/<int:episode_id>/rating/', EpisodeCreateRatingView.as_view(), name='episode_create_rating'),
]