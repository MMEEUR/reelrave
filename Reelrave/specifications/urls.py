from django.urls import path
from .views import GenreDetailView, GenreListView

app_name = 'spec'

urlpatterns = [
    path('genres/', GenreListView.as_view(), name='genres'),
    path('genres/<slug:slug>/', GenreDetailView.as_view(), name='genre_detail'),
]