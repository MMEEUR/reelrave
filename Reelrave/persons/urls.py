from django.urls import path
from .views import person_list, person_detail

app_name = 'persons'

urlpatterns = [
    path('', person_list, name='person_list'),
    path('<int:id>/', person_detail, name='person_detail')
]
