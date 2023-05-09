from django.db.models import QuerySet
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from shows.models import Show, Episode
from movies.models import Movie


def search_content(query: str) -> QuerySet | None:
    
    if query:
        search_query = SearchQuery(query, search_type="websearch")
        search_vector = SearchVector("name", weight="A") + SearchVector("description", weight="B")

        shows = (
            Show.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(rank__gte=0.4)
            .values("id", "name", "baner", "release_date", "search", "rank")
        )
        
        movies = (
            Movie.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(rank__gte=0.4)
            .values("id", "name", "baner", "release_date", "search", "rank")
        )
        
        episodes = (
            Episode.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(rank__gte=0.4)
            .values("id", "name", "baner", "release_date", "search", "rank")
        )

        qs = shows.union(movies, episodes).order_by("-rank")

        return qs

    else:
        return None