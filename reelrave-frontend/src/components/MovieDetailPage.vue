<template>
    <v-app style="background-color: #222831; min-height: 100vh;">
      <v-container>
        <!-- Movie Banner Section -->
        <v-row class="mb-5" style="background-color: #393E46; padding: 20px; border-radius: 8px;">
          <v-col cols="12">
            <v-img v-if="movie.baner" :src="`http://127.0.0.1:8000${movie.baner}`" class="movie-banner"></v-img>
          </v-col>
        </v-row>
  
        <!-- Movie Details Section -->
        <v-row class="mb-5" style="background-color: #FFD369; padding: 20px; border-radius: 8px;">
          <v-col cols="12" md="8">
            <h1 v-if="movie.name" class="movie-title" style="color: #222831;">{{ movie.name }}</h1>
            <p v-if="movie.description" class="movie-description" style="color: #393E46;">{{ movie.description }}</p>
  
            <v-chip-group>
              <v-chip v-for="genre in movie.genre || []" :key="genre.slug" style="background-color: #393E46; color: #EEEEEE;">
                {{ genre.name }}
              </v-chip>
            </v-chip-group>
  
            <v-list class="mb-3">
              <v-list-item>
                <v-list-item-content>
                  <strong style="color: #222831;">Country of Origin:</strong>
                  <v-img v-for="country in movie.country_of_origin || []" :key="country.slug" :src="`http://127.0.0.1:8000${country.flag}`" contain height="32" width="48" class="ml-2" style="border-radius: 50%;"></v-img>
                  <span v-if="movie.country_of_origin?.length">{{ movie.country_of_origin[0].name }}</span>
                </v-list-item-content>
              </v-list-item>
  
              <v-list-item>
                <v-list-item-content>
                  <strong style="color: #222831;">Director:</strong>
                  <v-img v-for="director in movie.director || []" :key="director.name" :src="`http://127.0.0.1:8000${director.picture}`" circle height="32" width="32" class="ml-2"></v-img>
                  <span v-if="movie.director?.length">{{ movie.director[0].name }}</span>
                </v-list-item-content>
              </v-list-item>
  
              <v-list-item>
                <v-list-item-content>
                  <strong style="color: #222831;">Writers:</strong>
                  <v-img v-for="writer in movie.writers || []" :key="writer.name" :src="`http://127.0.0.1:8000${writer.picture}`" circle height="32" width="32" class="ml-2"></v-img>
                  <span v-if="movie.writers?.length">{{ movie.writers[0].name }}</span>
                </v-list-item-content>
              </v-list-item>
  
              <v-list-item>
                <v-list-item-content>
                  <strong style="color: #222831;">Actors:</strong>
                  <v-img v-for="actor in movie.actors || []" :key="actor.name" :src="`http://127.0.0.1:8000${actor.picture}`" circle height="32" width="32" class="ml-2"></v-img>
                  <span v-if="movie.actors?.length">{{ movie.actors[0].name }}</span>
                </v-list-item-content>
              </v-list-item>
            </v-list>
  
            <v-rating v-if="movie.average_rating" :value="movie.average_rating" dense readonly></v-rating>
            <span v-if="movie.total_ratings">({{ movie.total_ratings }} Ratings)</span>
  
            <p><strong v-if="movie.release_date">Release Date:</strong> {{ movie.release_date }}</p>
            <p><strong v-if="movie.content_rating">Content Rating:</strong> {{ movie.content_rating }}</p>
            <p><strong v-if="movie.time">Duration:</strong> {{ movie.time }}</p>
          </v-col>
        </v-row>
  
        <!-- Storyline Section -->
        <v-row class="mb-5" style="background-color: #EEEEEE; padding: 20px; border-radius: 8px;">
          <v-col cols="12">
            <h2 v-if="movie.storyline" class="movie-section-title" style="color: #222831;">Storyline</h2>
            <p v-if="movie.storyline" class="movie-description" style="color: #393E46;">{{ movie.storyline }}</p>
          </v-col>
        </v-row>
  
        <!-- Comments Section -->
        <v-row style="background-color: #393E46; padding: 20px; border-radius: 8px;">
          <v-col cols="12">
            <h2 v-if="comments.length" class="movie-section-title" style="color: #FFD369;">Comments</h2>
            <v-card v-for="comment in comments" :key="comment.id" class="mb-3" style="background-color: #222831; color: #EEEEEE;">
              <v-card-title>
                <v-avatar size="32" style="background-color: #FFD369; color: #222831;">{{ comment.user?.username.charAt(0) }}</v-avatar>
                <span class="ml-2">{{ comment.user?.username }}</span>
                <v-spacer></v-spacer>
                <small>{{ new Date(comment.created).toLocaleDateString() }}</small>
              </v-card-title>
              <v-card-text>{{ comment.body }}</v-card-text>
              <v-card-actions>
                <v-icon small style="color: #FFD369;">mdi-thumb-up</v-icon> {{ comment.likes_count }}
                <v-icon small style="color: #FFD369;">mdi-thumb-down</v-icon> {{ comment.dislikes_count }}
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
        movie: {},
        comments: []
      };
    },
    created() {
      const movieSlug = this.$route.params.movie_slug;
      axios
        .get(`http://127.0.0.1:8000/movies/${movieSlug}/`)
        .then(response => {
          this.movie = response.data.movie || {};
          this.comments = response.data.comments || [];
        })
        .catch(err => console.error(err));
    }
  };
  </script>
  
  <style scoped>
  .movie-banner {
    width: 100%;
    height: 300px;
    object-fit: cover;
    margin-bottom: 20px;
    border-radius: 8px;
  }
  .movie-title {
    font-size: 2.5rem;
    margin-bottom: 20px;
  }
  .movie-description {
    margin-bottom: 15px;
  }
  .movie-section-title {
    margin-bottom: 20px;
  }
  </style>
  