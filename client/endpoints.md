# Endpoitns

This file contains endpoints and http methods for **Frontend Developer**

## Movies

- **/movies/**:

> **GET**
> Get 10 of all movies per page
> _file: [movie_list](json/movies/movie_list.json)_

- **/movies/(slug)/**:

> **GET**
> Detail of a movie (you can request by get_absolute_url of a movie)
> _file: [movie_detail](json/movies/movie_detail.json)_

- **/movies/genre/(genre)/**:

> **GET**
> Get 10 movies by the genre per page (you must request with slug of a genre in url)
> _file: [movie_by_genre](json/movies/movie_by_genre.json)_

- **/movies/country/(country)/**:

> **GET**
> Get 10 movies by the country per page (you must request with slug of a country in url)
> _file: [movie_by_country](json/movies/movie_by_country.json)_

- **/movies/top/**:

> **GET**
> Get top 250 movies
> _file: [top_movies](json/movies/top_movies.json)_

- **/movies/top/(genre)/**:

> **GET**
> Get top 250 movies by the genre (you must request with slug of a genre in url)
> _file: [top_movies_by_genre](json/movies/top_movies.json)_

## Shows

- **/shows/**:

> **GET**
Get 10 of all shows per page
*file: [show_list](json/shows/shows_list.json)*

- **/shows/(slug)/**:

> **GET**
Detail of a show (you can request by get_absolute_url of a show)
*file: [show_detail](json/shows/show_detail.json)*
 
- **/shows/episodes/**:

> **GET**
List of a show's episodes
*file: [episode_list](json/shows/episode_list.json)*
 
- **/shows/episodes/(id)/**:

> **GET**
Detail of a episode (you can request by get_absolute_url of a episode)
*file: [episode_detail](json/shows/episode_detail.json)*

- **/shows/genre/(genre)/**:

> **GET**
Get 10 shows by the genre per page (you must request with slug of a genre in url)
*file: [show_by_genre](json/shows/show_by_genre.json)*

- **/shows/country/(country)/**:

> **GET**
Get 10 shows by the country per page (you must request with slug of a country in url)
*file: [show_by_country](json/shows/show_by_country.json)*

- **/shows/top/**:

> **GET**
Get top 250 shows
*file: [top_shows](json/shows/top_shows.json)* 

- **/shows/top/(genre)/**:

> **GET**
Get top 250 shows by the genre (you must request with slug of a genre in url)
*file: [top_shows_by_genre](json/shows/top_shows.json)* 

## Persons

- **/persons/**

> **GET**
Get 10 of all persons per page
*file: [person_list](json/persons/person_list.json)*

- **/persons/(id)/**

> **GET**
Get details of a person (you must request with id of a person)
*file: [person_detail](json/persons/person_detail.json)*

- **/persons/role/(role)/**

> **GET**
Get 10 of all persons filtered by role per page
*file: [person_list_by_role](json/persons/person_list_by_role.json)*

- **/persons/search/**

> **GET**
Search a person (you must add /?q="query" to url)
*file: [person_search](json/persons/person_search.json)*

## Specifications

- **/videos/**

> **GET**
Get 10 of latest videos per page
*file: [videos](json/specifications/videos.json)*

- **/photos/**

> **GET**
Get 10 of latest photos per page
*file: [photos](json/specifications/photos.json)*

- **/genres/**

> **GET**
Get all of the genres that have movie or show
*file: [genres](json/specifications/genres.json)*

- **/countries/**

> **GET**
Get all of the countries that have movie or show
*file: [countries](json/specifications/countries.json)*

- **/comment/(comment_id)/**

> **PATCH**
Update a comment (you must request with id of a comment and the header must have access token of jwt)
*files: [comment_update](json/specifications/comment_update.json)*

> **DELETE**
Delete a comment (you must request with id of a comment and the header must have access token of jwt)
*no files*

- **/comment/(comment_id)/like_or_dislike/**

>  **POST**
Like or dislike a comment (you must request with id of a comment and the header must have access token of jwt)
*file: [comment_like_or_dislike](json/specifications/comment_like_or_dislike.json)*

> **PATCH**
Change like to dislike or ... (you must request with id of a comment and the header must have access token of jwt)
*file: [comment_like_or_dislike](json/specifications/comment_like_or_dislike.json)*

> **DELETE**
Delete the opinion on the comment (you must request with id of a comment and the header must have access token of jwt)
*no files*

## Home

- **/**

> **GET**
Get featured_movies, latest_trailers, latest_episodes, latest_movies
*file: [home](json/home/home.json)*

- **/search/**

> **GET**
Search among the all movies, shows and episodes (you must add /?q="query" to url)
*file: [search](json/home/search.json)*