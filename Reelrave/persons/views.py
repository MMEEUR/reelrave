from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.contrib.postgres.search import TrigramSimilarity
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Person, Role
from .serializers import PersonListSerializer, PersonDetailSerializer, RoleSerializer


@api_view(["GET"])
def person_list(request, role=None):
    if role:
        roles = get_object_or_404(Role, slug=role)
        role_serializer = RoleSerializer(roles)
        persons = roles.persons.all()

    else:
        roles = Role.objects.all()
        role_serializer = RoleSerializer(roles, many=True)
        persons = Person.objects.all()

    paginator = PageNumberPagination()
    paginator.page_size = 10
    page = paginator.paginate_queryset(persons, request)
    person_serializer = PersonListSerializer(page, many=True)

    data = {"Roles": role_serializer.data, "Persons": person_serializer.data}

    response = Response(data)
    response["X-Total-Count"] = paginator.page.paginator.count
    response["X-Page-Size"] = paginator.page_size
    response["X-Page"] = paginator.page.number

    return response


@api_view(["GET"])
def person_detail(request, id):
    person = get_object_or_404(Person, id=id)
    serializer = PersonDetailSerializer(person)

    return Response(serializer.data)


@api_view(["GET"])
def person_search(request):
    query = request.GET.get("q", "")

    # Check cache for results

    cache_key = f"search:{query}"
    cached_result = cache.get(cache_key)

    if cached_result:
        
        return Response(cached_result)

    if query:
        persons = Person.objects.annotate(
            similarity=TrigramSimilarity("name", query)
        ).filter(similarity__gt=0.1)

        data = {
            "query": query,
            "results": PersonListSerializer(persons, many=True).data,
        }

        cache.set(cache_key, data, 3600)
        
        return Response(data)

    return Response()