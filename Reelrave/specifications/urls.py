from django.urls import path
from .views import (
    GenreDetailView, GenreListView,
    CountryListView, CountryDetailView,
    UpdateDeleteCommentView, CommentLikeDisLikeView
)

app_name = 'spec'

urlpatterns = [
    path('genres/', GenreListView.as_view(), name='genres'),
    path('countries/', CountryListView.as_view(), name='countries'),
    path('comment/<int:comment_id>/', UpdateDeleteCommentView.as_view(), name='comment_update_delete'),
    path('comment/<int:comment_id>/like_or_dislike/', CommentLikeDisLikeView.as_view(), name='comment_like_or_dislike'),
]