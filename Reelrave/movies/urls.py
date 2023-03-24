from django.urls import path
from .views import MovieListView, MovieDetailView, CreateCommentView

app_name = 'movies'

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('<slug:slug>/comment/', CreateCommentView.as_view(), name='create_comment'),
]