# Endpoints

This file contains endpoints and http methods for **Frontend Developer**

## Movies

- **/movies/**:

> **GET**
> Get 10 of all movies per page
> _file: [movie_list](json/movies/movie_list.json)_

- **/movies/(movie_slug)/**:

> **GET**
> Detail of a movie (you can request by get_absolute_url of a movie)
> _file: [movie_detail](json/movies/movie_detail.json)_

- **/movies/(movie_slug)/comment/**:

> **POST**
> Create a comment (the header must have access token of jwt)
> _file: [movie_create_comment](json/specifications/comment.json)_

- **/movies/(movie_slug)/rating/**:

> **POST**
> Create a rating (the header must have access token of jwt) - (rating score must be between 0 and 10 zero meens just watched and no opinon)
> _file: [movie_create_rating](json/specifications/rating.json)_

> **PATCH**
> Update the rating score (the header must have access token of jwt) - (rating score must be between 0 and 10 zero meens just watched and no opinon)
> _file: [movie_update_rating](json/specifications/rating.json)_

> **DELETE**
> Delete a rating (the header must have access token of jwt)
> _no files_

- **/movies/(movie_slug)/watchlist/**:

> **POST**
> Create a watchlist (the header must have access token of jwt)
> _no files_

> **DELETE**
> Delete a watchlist (the header must have access token of jwt)
> _no files_

- **/movies/genre/(genre_slug)/**:

> **GET**
> Get 10 movies by the genre per page (you must request with slug of a genre in url)
> _file: [movie_by_genre](json/movies/movie_by_genre.json)_

- **/movies/country/(country_slug)/**:

> **GET**
> Get 10 movies by the country per page (you must request with slug of a country in url)
> _file: [movie_by_country](json/movies/movie_by_country.json)_

- **/movies/top/**:

> **GET**
> Get top 250 movies
> _file: [top_movies](json/movies/top_movies.json)_

- **/movies/top/(genre_slug)/**:

> **GET**
> Get top 250 movies by the genre (you must request with slug of a genre in url)
> _file: [top_movies_by_genre](json/movies/top_movies.json)_

## Shows

- **/shows/**:

> **GET**
> Get 10 of all shows per page
> _file: [show_list](json/shows/shows_list.json)_

- **/shows/(show_slug)/**:

> **GET**
> Detail of a show (you can request by get_absolute_url of a show)
> _file: [show_detail](json/shows/show_detail.json)_

- **/shows/(show_slug)/comment/**:

> **POST**
> Create a comment (the header must have access token of jwt)
> _file: [show_create_comment](json/specifications/comment.json)_

- **/shows/(show_slug)/rating/**:

> **POST**
> Create a rating (the header must have access token of jwt) - (rating score must be between 0 and 10 zero meens just watched and no opinon)
> _file: [show_create_rating](json/specifications/rating.json)_

> **PATCH**
> Update the rating score (the header must have access token of jwt) - (rating score must be between 0 and 10 zero meens just watched and no opinon)
> _file: [show_update_rating](json/specifications/rating.json)_

> **DELETE**
> Delete a rating (the header must have access token of jwt)
> _no files_

- **/shows/(show_slug)/watchlist/**:

> **POST**
> Create a watchlist (the header must have access token of jwt)
> _no files_

> **DELETE**
> Delete a watchlist (the header must have access token of jwt)
> _no files_

- **/shows/(show_slug)/episodes/**:

> **GET**
> List of a show's episodes
> _file: [episode_list](json/shows/episode_list.json)_

- **/shows/(show_slug)/episodes/(episode_id)/**:

> **GET**
> Detail of a episode (you can request by get_absolute_url of a episode)
> _file: [episode_detail](json/shows/episode_detail.json)_

- **/shows/(show_slug)/episodes/(episode_id)/comment/**:

> **POST**
> Create a comment (the header must have access token of jwt)
> _file: [episode_create_comment](json/specifications/comment.json)_

- **/shows/(show_slug)/episodes/(episode_id)/rating/**:

> **POST**
> Create a rating (the header must have access token of jwt) - (rating score must be between 0 and 10 zero meens just watched and no opinon)
> _file: [episode_create_rating](json/specifications/rating.json)_

> **PATCH**
> Update the rating score (the header must have access token of jwt) - (rating score must be between 0 and 10 zero meens just watched and no opinon)
> _file: [episode_update_rating](json/specifications/rating.json)_

> **DELETE**
> Delete a rating (the header must have access token of jwt)
> _no files_

- **/shows/(show_slug)/episodes/(episode_id)/watchlist/**:

> **POST**
> Create a watchlist (the header must have access token of jwt)
> _no files_

> **DELETE**
> Delete a watchlist (the header must have access token of jwt)
> _no files_

- **/shows/genre/(genre_slug)/**:

> **GET**
> Get 10 shows by the genre per page (you must request with slug of a genre in url)
> _file: [show_by_genre](json/shows/show_by_genre.json)_

- **/shows/country/(country_slug)/**:

> **GET**
> Get 10 shows by the country per page (you must request with slug of a country in url)
> _file: [show_by_country](json/shows/show_by_country.json)_

- **/shows/top/**:

> **GET**
> Get top 250 shows
> _file: [top_shows](json/shows/top_shows.json)_

- **/shows/top/(genre)/**:

> **GET**
> Get top 250 shows by the genre (you must request with slug of a genre in url)
> _file: [top_shows_by_genre](json/shows/top_shows.json)_

## Persons

- **/persons/**

> **GET**
> Get 10 of all persons per page
> _file: [person_list](json/persons/person_list.json)_

- **/persons/(person_id)/**

> **GET**
> Get details of a person (you must request with id of a person)
> _file: [person_detail](json/persons/person_detail.json)_

- **/persons/role/(role_slug)/**

> **GET**
> Get 10 of all persons filtered by role per page
> _file: [person_list_by_role](json/persons/person_list_by_role.json)_

- **/persons/search/**

> **GET**
> Search a person (you must add /?q="query" to url)
> _file: [person_search](json/persons/person_search.json)_

## Specifications

- **/videos/**

> **GET**
> Get 10 of latest videos per page
> _file: [videos](json/specifications/videos.json)_

- **/photos/**

> **GET**
> Get 10 of latest photos per page
> _file: [photos](json/specifications/photos.json)_

- **/genres/**

> **GET**
> Get all of the genres that have movie or show
> _file: [genres](json/specifications/genres.json)_

- **/countries/**

> **GET**
> Get all of the countries that have movie or show
> _file: [countries](json/specifications/countries.json)_

- **/comment/(comment_id)/**

> **PATCH**
> Update a comment (you must request with id of a comment and the header must have access token of jwt)
> _files: [comment_update](json/specifications/comment.json)_

> **DELETE**
> Delete a comment (you must request with id of a comment and the header must have access token of jwt)
> _no files_

- **/comment/(comment_id)/like_or_dislike/**

> **POST**
> Like or dislike a comment (you must request with id of a comment and the header must have access token of jwt)
> _file: [comment_like_or_dislike](json/specifications/comment_like_or_dislike.json)_

> **PATCH**
> Change like to dislike or ... (you must request with id of a comment and the header must have access token of jwt)
> _file: [comment_like_or_dislike](json/specifications/comment_like_or_dislike.json)_

> **DELETE**
> Delete the opinion on the comment (you must request with id of a comment and the header must have access token of jwt)
> _no files_

## Home

- **/**

> **GET**
> Get featured_movies, latest_trailers, latest_episodes, latest_movies
> _file: [home](json/home/home.json)_

- **/search/**

> **GET**
> Search among the all movies, shows and episodes (you must add /?q="query" to url)
> _file: [search](json/home/search.json)_