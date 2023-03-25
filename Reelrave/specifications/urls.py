from django.urls import path
from .views import GenreDetailView, GenreListView, CountryListView, CountryDetailView, UpdateDeleteCommentView

app_name = 'spec'

urlpatterns = [
    path('genres/', GenreListView.as_view(), name='genres'),
    path('genres/<slug:slug>/', GenreDetailView.as_view(), name='genre_detail'),
    path('countries/', CountryListView.as_view(), name='countries'),
    path('countries/<slug:slug>/', CountryDetailView.as_view(), name='country_detail'),
    path('comment/<int:comment_id>/', UpdateDeleteCommentView.as_view(), name='comment_update_delete'),
]