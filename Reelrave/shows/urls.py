from django.urls import path
from .views import ShowListView, ShowDetailView, ShowCreateCommentView, EpisodeListView, EpisodeDetailView

app_name = 'shows'

urlpatterns = [
    path('', ShowListView.as_view(), name='show_list'),
    path('<slug:slug>/', ShowDetailView.as_view(), name='show_detail'),
    path('<slug:slug>/comment/', ShowCreateCommentView.as_view(), name='show_create_comment'),
    path('<slug:slug>/episodes/', EpisodeListView.as_view(), name='episode_list'),
    path('<slug:slug>/episodes/<int:episode_id>/', EpisodeDetailView.as_view(), name='episode_detail'),
]