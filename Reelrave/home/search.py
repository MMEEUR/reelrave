from django.db.models import QuerySet
from django.contrib.postgres.search import SearchQuery, TrigramSimilarity
from shows.models import Show, Episode
from movies.models import Movie


def search_content(query: str) -> QuerySet:
    
    search_query = SearchQuery(query)

    shows = (
        Show.objects.annotate(
            search=search_query, similarity=TrigramSimilarity('name', query),
        )
        .filter(similarity__gt=0.3)
        .values("id", "name", "baner", "release_date", "search", "similarity")
    )
    
    movies = (
        Movie.objects.annotate(
            search=search_query, similarity=TrigramSimilarity('name', query),
        )
        .filter(similarity__gt=0.3)
        .values("id", "name", "baner", "release_date", "search", "similarity")
    )
    
    episodes = (
        Episode.objects.annotate(
            search=search_query, similarity=TrigramSimilarity('name', query),
        )
        .filter(similarity__gt=0.3)
        .values("id", "name", "baner", "release_date", "search", "similarity")
    )

    qs = shows.union(movies, episodes).order_by("-similarity")

    return qs