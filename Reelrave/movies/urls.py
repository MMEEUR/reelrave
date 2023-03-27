from django.urls import path
from .views import MovieListView, MovieDetailView, MovieCreateCommentView, MovieCreateRatingView

app_name = 'movies'

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('<slug:slug>/comment/', MovieCreateCommentView.as_view(), name='movie_create_comment'),
    path('<slug:slug>/rating/', MovieCreateRatingView.as_view(), name='movie_create_rating'),
]