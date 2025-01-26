<template>
    <v-app style="background-color: #222831; min-height: 100vh;">
      <v-container class="movies-list" fluid>
        <v-row>
          <v-col cols="12" md="4" v-for="movie in movies" :key="movie.id">
            <v-card elevation="2" class="movie-card">
              <v-img 
                :src="`http://127.0.0.1:8000/${movie.baner}`" 
                :alt="movie.name" 
                class="movie-image"
                height="300px"
              ></v-img>
              <v-card-title class="movie-title">
                {{ movie.name }}
              </v-card-title>
              <v-card-subtitle class="movie-subtitle">
                Release: {{ movie.release_date }}
              </v-card-subtitle>
              <v-card-text class="movie-details">
                <span>Time: {{ movie.time }}</span>
                <br />
                <span>Genres: {{ movie.genre.map(g => g.name).join(', ') }}</span>
              </v-card-text>
              <v-card-text class="movie-description">
                {{ movie.description.slice(0, 100) }}...
              </v-card-text>
              <v-card-actions>
                <v-btn 
                  color="primary"
                  :href="movie.get_absolute_url"
                  text
                >
                  View Details
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-app>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        movies: [],
        currentPage: 1,
        totalPages: 1,
      };
    },
    methods: {
      async fetchMovies() {
        try {
          const response = await axios.get(`http://127.0.0.1:8000/movies/`, {
            params: {
              page: this.currentPage,
            },
          });
          this.movies = response.data;
        } catch (error) {
          console.error('Error fetching movies:', error);
        }
      },
    },
    mounted() {
      this.fetchMovies();
    },
  };
  </script>
  
  <style scoped>
  .movies-list {
    background-color: #222831;
    color: #EEEEEE;
    min-height: 100vh;
    padding: 20px;
  }
  .movie-card {
    background-color: #393E46;
    color: #EEEEEE;
  }
  .movie-title {
    color: #FFD369;
    font-weight: bold;
  }
  .movie-subtitle {
    color: #EEEEEE;
    opacity: 0.8;
  }
  .movie-details {
    color: #EEEEEE;
    opacity: 0.9;
    margin-bottom: 10px;
  }
  .movie-description {
    color: #EEEEEE;
    opacity: 0.9;
  }
  .mt-4 {
    margin-top: 16px;
  }
  </style>
  