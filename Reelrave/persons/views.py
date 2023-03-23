from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person, Role
from .serializers import PersonListSerializer, PersonDetailSerializer, RoleSerializer

# Create your views here.
@api_view(['GET'])
def person_list(request):
    persons = Person.objects.all()
    roles = Role.objects.all()

    data = {
        "Persons": PersonListSerializer(persons, many=True).data,
        "Roles": RoleSerializer(roles, many=True).data
    }

    return Response(data)

@api_view(['GET'])
def person_detail(request, id):
    person = get_object_or_404(Person, id=id)
    serializer = PersonDetailSerializer(person)
    
    return Response(serializer.data)