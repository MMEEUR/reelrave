# Endpoitns

This file contains endpoints and http methods for **Frontend Developer**

## Movies

- **/movies/**:

> **GET**
Get 10 of all movies per page
*file: [movie_list](json/movies/movie_list.json)*

- **/movies/(slug)/**:

> **GET**
 Detail of a movie (you can request by get_absolute_url of a movie)
 *file: [movie_detail](json/movies/movie_detail.json)*

- **/movies/genre/(genre)/**:

> **GET**
Get 10 movies by the genre per page (you must request with slug of a genre in url)
*file: [movie_by_genre](json/movies/movie_by_genre.json)*

- **/movies/country/(country)/**:

> **GET**
Get 10 movies by the country per page (you must request with slug of a country in url)
*file: [movie_by_country](json/movies/movie_by_country.json)*

- **/movies/top/**:

> **GET**
Get top 250 movies
*file: [top_movies](json/movies/top_movies.json)* 

- **/movies/top/(genre)/**:

> **GET**
Get top 250 movies by the genre (you must request with slug of a genre in url)
*file: [top_movies_by_genre](json/movies/top_movies.json)* 
