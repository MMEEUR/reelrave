from django.urls import path
from .views import ShowListView, ShowDetailView

app_name = 'shows'

urlpatterns = [
    path('', ShowListView.as_view(), name='show_list'),
    path('<slug:slug>/', ShowDetailView.as_view(), name='show_detail')
]