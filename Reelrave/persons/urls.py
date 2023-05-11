from django.urls import path
from .views import person_list, person_detail, person_search

app_name = 'persons'

urlpatterns = [
    path('', person_list, name='person_list'),
    path('<int:id>/', person_detail, name='person_detail'),
    path('role/<slug:role>/', person_list, name='person_list_by_role'),
    path('search/', person_search, name='person_search')
]