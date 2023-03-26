from django.urls import path
from .views import ShowListView, ShowDetailView, CreateCommentView, EpisodeDetailView

app_name = 'shows'

urlpatterns = [
    path('', ShowListView.as_view(), name='show_list'),
    path('<slug:slug>/', ShowDetailView.as_view(), name='show_detail'),
    path('<slug:slug>/comment/', CreateCommentView.as_view(), name='create_comment'),
    path('<slug:slug>/episode/<int:episode_id>/', EpisodeDetailView.as_view(), name='episode_detail'),
]