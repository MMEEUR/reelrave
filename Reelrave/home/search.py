from typing import List
from django.contrib.postgres.search import TrigramSimilarity
from shows.models import Show, Episode
from movies.models import Movie


def search_content(query: str) -> List:
    shows = Show.objects.annotate(
        similarity=TrigramSimilarity("name", query),
    ).filter(similarity__gt=0.1)

    movies = Movie.objects.annotate(
        similarity=TrigramSimilarity("name", query),
    ).filter(similarity__gt=0.1)

    episodes = Episode.objects.annotate(
        similarity=TrigramSimilarity("name", query),
    ).filter(similarity__gt=0.1)

    results = []

    for obj in (movies, shows, episodes):
        for item in obj:
            results.append(
                {
                    "object_id": item.id,
                    "object_type": obj.model.__name__.lower(),
                    "name": item.name,
                    "baner": item.baner,
                    "release_date": item.release_date,
                    "get_absolute_url": item.get_absolute_url,
                    "similarity": item.similarity,
                }
            )

    results = sorted(results, key=lambda x: x["similarity"], reverse=True)

    return results