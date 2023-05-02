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