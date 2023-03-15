from django.urls import path
from .views import movie_list, movie_detail, MovieCommentView

app_name = 'movies'

urlpatterns = [
    path('', movie_list, name='movie_list'),
    path('<slug:slug>/', movie_detail, name='movie_detail'),
    path('<slug:slug>/comments/', MovieCommentView.as_view(), name='movie_detail'),
]
