<template>
  <v-app style="background-color: #222831; min-height: 100vh;">
    <v-container>
      <!-- Movie Details Section -->
      <v-row class="mb-5" style="background-color: #2A2F38; padding: 40px; border-radius: 12px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);">
        <v-col cols="12" md="4">
          <v-img v-if="movie.baner" :src="`http://127.0.0.1:8000${movie.baner}`" contain class="movie-banner-box" style="border-radius: 16px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);"></v-img>
        </v-col>
        <v-col cols="12" md="8">
          <h1 v-if="movie.name" class="movie-title" style="color: #FFD369; font-weight: bold; margin-bottom: 20px;">{{ movie.name }}</h1>
          <p v-if="movie.description" class="movie-description" style="color: #EEEEEE; font-size: 1.2rem; margin-bottom: 20px;">{{ movie.description }}</p>

          <v-chip-group>
            <v-chip v-for="genre in movie.genre || []" :key="genre.slug" style="background-color: #FFD369; color: #222831; font-weight: bold; margin: 4px;">
              {{ genre.name }}
            </v-chip>
          </v-chip-group>

          <v-btn
            :color="isInWatchlist ? 'red' : 'green'"
            class="mt-4"
            @click="toggleWatchlist"
            style="color: #EEEEEE; font-weight: bold;"
          >
            {{ isInWatchlist ? 'Remove from Watchlist' : 'Add to Watchlist' }}
          </v-btn>

          <v-list class="mt-5" style="background-color: #393E46; padding: 20px; border-radius: 8px;">
            <v-list-item>
              <v-list-item-content>
                <strong style="color: #FFD369; font-size: 1.1rem;">Country of Origin:</strong>
                <v-img v-for="country in movie.country_of_origin || []" :key="country.slug" :src="`http://127.0.0.1:8000${country.flag}`" contain height="40" width="60" class="ml-2" style="border-radius: 8px; border: 2px solid #FFD369;"></v-img>
                <span v-if="movie.country_of_origin?.length" style="font-size: 1.1rem; margin-left: 8px; color: #EEEEEE;">{{ movie.country_of_origin[0].name }}</span>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <strong style="color: #FFD369; font-size: 1.1rem;">Director:</strong>
                <v-img v-for="director in movie.director || []" :key="director.name" :src="`http://127.0.0.1:8000${director.picture}`" circle height="40" width="40" class="ml-2" style="border: 2px solid #FFD369;"></v-img>
                <span v-if="movie.director?.length" style="font-size: 1.1rem; margin-left: 8px; color: #EEEEEE;">{{ movie.director[0].name }}</span>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <strong style="color: #FFD369; font-size: 1.1rem;">Writers:</strong>
                <v-img v-for="writer in movie.writers || []" :key="writer.name" :src="`http://127.0.0.1:8000${writer.picture}`" circle height="40" width="40" class="ml-2" style="border: 2px solid #FFD369;"></v-img>
                <span v-if="movie.writers?.length" style="font-size: 1.1rem; margin-left: 8px; color: #EEEEEE;">{{ movie.writers[0].name }}</span>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-content>
                <strong style="color: #FFD369; font-size: 1.1rem;">Actors:</strong>
                <v-img v-for="actor in movie.actors || []" :key="actor.name" :src="`http://127.0.0.1:8000${actor.picture}`" circle height="40" width="40" class="ml-2" style="border: 2px solid #FFD369;"></v-img>
                <span v-if="movie.actors?.length" style="font-size: 1.1rem; margin-left: 8px; color: #EEEEEE;">{{ movie.actors[0].name }}</span>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-rating v-if="movie.average_rating" :value="movie.average_rating" dense readonly></v-rating>
          <span v-if="movie.total_ratings" style="font-size: 1rem; margin-left: 8px; color: #EEEEEE;">({{ movie.total_ratings }} Ratings)</span>

          <p style="margin-top: 20px;">
            <strong v-if="movie.release_date" style="font-size: 1.1rem; color: #FFD369;">Release Date:    </strong>
            <span style="color: #EEEEEE;">{{ movie.release_date }}</span>
          </p>
          <p>
            <strong v-if="movie.content_rating" style="font-size: 1.1rem; color: #FFD369;">Content Rating:    </strong>
            <span style="color: #EEEEEE;">{{ movie.content_rating }}</span>
          </p>
          <p>
            <strong v-if="movie.time" style="font-size: 1.1rem; color: #FFD369;">Duration:    </strong>
            <span style="color: #EEEEEE;">{{ movie.time }}</span>
          </p>
        </v-col>
      </v-row>

      <!-- Storyline Section -->
      <v-row class="mb-5" style="background-color: #FFD369; padding: 20px; border-radius: 8px;">
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
              <v-icon small style="color: #FFD369; cursor: pointer;" @click="checkIfLoggedIn(() => handleLike(comment.id, true))">mdi-thumb-up</v-icon> {{ comment.likes_count }}
              <v-icon small style="color: #FFD369; cursor: pointer;" @click="checkIfLoggedIn(() => handleLike(comment.id, false))">mdi-thumb-down</v-icon> {{ comment.dislikes_count }}
            </v-card-actions>
          </v-card>

          <!-- Input Box for Logged-In Users -->
          <div v-if="isLoggedIn" class="mt-5" style="background-color: #222831; padding: 20px; border-radius: 8px;">
            <v-textarea
              v-model="newComment"
              label="Add a comment"
              outlined
              dense
              style="background-color: #393E46; color: #EEEEEE;"
            ></v-textarea>
            <v-btn color="#FFD369" class="mt-3" @click="submitComment" style="color: #222831; font-weight: bold;">Submit</v-btn>
          </div>
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
      comments: [],
      newComment: "",
      isLoggedIn: false,
      likedComments: JSON.parse(localStorage.getItem('likedComments')) || {},
      isInWatchlist: false,
    };
  },
  created() {
    this.checkLoginStatus();
    this.refreshPage();
  },
  watch: {
    movie: {
      handler() {
        this.checkWatchlistStatus();
      },
      immediate: true,
    },
  },
  methods: {
    async checkLoginStatus() {
      const refreshToken = localStorage.getItem('refreshToken');
      if (!refreshToken) {
        this.isLoggedIn = false;
        return;
      }
      try {
        const response = await axios.post("http://127.0.0.1:8000/accounts/token/refresh/", {
          refresh: refreshToken,
        });
        this.isLoggedIn = response.status === 200 && response.data.access;
      } catch (error) {
        this.isLoggedIn = false;
      }
    },
    async refreshPage() {
      const movieSlug = this.$route.params.movie_slug;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/movies/${movieSlug}/`);
        this.movie = response.data.movie || {};
        this.comments = response.data.comments || [];
      } catch (error) {
        console.error("Failed to refresh page data:", error);
      }
    },
    async submitComment() {
      if (!this.newComment.trim()) {
        alert("Comment cannot be empty.");
        return;
      }
      try {
        const tokenResponse = await axios.post("http://127.0.0.1:8000/accounts/token/refresh/", {
          refresh: localStorage.getItem("refreshToken"),
        });
        const accessToken = tokenResponse.data.access;
        const config = {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        };
        await axios.post(
          `http://127.0.0.1:8000/movies/${this.movie.slug}/comment/`,
          { body: this.newComment },
          config
        );
        this.newComment = "";
        this.refreshPage();
      } catch (error) {
        console.error("Failed to submit comment:", error);
        alert("Failed to submit your comment. Please try again later.");
      }
    },
    async checkIfLoggedIn(callback) {
      const refreshToken = localStorage.getItem('refreshToken');
      if (!refreshToken) {
        alert('Please log in to like or dislike comments.');
        this.$router.replace('/login');
        return;
      }
      try {
        const response = await axios.post("http://127.0.0.1:8000/accounts/token/refresh/", {
          refresh: refreshToken,
        });
        if (response.status !== 200 || !response.data.access) {
          alert('Session expired. Please log in again.');
          this.$router.replace('/login');
          return;
        }
        callback();
      } catch (error) {
        alert('Session expired. Please log in again.');
        console.log("Token refresh failed. Token may be expired or invalid.", error);
        this.$router.replace('/login');
      }
    },
    async handleLike(commentId, likeOrDislike) {
      const tokenResponse = await axios.post('http://127.0.0.1:8000/accounts/token/refresh/', {
        refresh: localStorage.getItem('refreshToken')
      });
      const accessToken = tokenResponse.data.access;
      const config = {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      };

      try {
        if (this.likedComments[commentId] === likeOrDislike) {
          await axios.delete(`http://127.0.0.1:8000/comment/${commentId}/like_or_dislike/`, config);
          this.likedComments[commentId] = undefined;
        } else {
          try {
            await axios.post(
              `http://127.0.0.1:8000/comment/${commentId}/like_or_dislike/`,
              { like_or_dislike: likeOrDislike },
              config
            );
            this.likedComments[commentId] = likeOrDislike;
          } catch (error) {
            if (error.response && error.response.status === 400) {
              await axios.patch(
                `http://127.0.0.1:8000/comment/${commentId}/like_or_dislike/`,
                { like_or_dislike: likeOrDislike },
                config
              );
              this.likedComments[commentId] = likeOrDislike;
            } else {
              throw error;
            }
          }
        }
        localStorage.setItem('likedComments', JSON.stringify(this.likedComments));
        this.refreshPage();
      } catch (error) {
        console.error("Failed to handle like/dislike:", error);
      }
    },
    checkWatchlistStatus() {
      const watchlist = JSON.parse(localStorage.getItem("watchlist")) || {};
      this.isInWatchlist = !!watchlist[this.movie.slug];
    },
    async toggleWatchlist() {
      const tokenResponse = await axios.post("http://127.0.0.1:8000/accounts/token/refresh/", {
        refresh: localStorage.getItem("refreshToken"),
      });
      const accessToken = tokenResponse.data.access;
      const config = {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      };

      try {
        if (this.isInWatchlist) {
          try {
            await axios.delete(`http://127.0.0.1:8000/movies/${this.movie.slug}/watchlist/`, config);
            this.updateWatchlist(false);
          } catch (error) {
            if (error.response && error.response.status === 404) {
              await axios.post(`http://127.0.0.1:8000/movies/${this.movie.slug}/watchlist/`, {}, config);
              this.updateWatchlist(true);
            } else {
              throw error;
            }
          }
        } else {
          try {
            await axios.post(`http://127.0.0.1:8000/movies/${this.movie.slug}/watchlist/`, {}, config);
            this.updateWatchlist(true);
          } catch (error) {
            if (error.response && error.response.status === 400) {
              await axios.delete(`http://127.0.0.1:8000/movies/${this.movie.slug}/watchlist/`, config);
              this.updateWatchlist(false);
            } else {
              throw error;
            }
          }
        }
      } catch (error) {
        console.error("Failed to toggle watchlist status:", error);
        alert("Failed to update watchlist. Please try again later.");
      }
    },
    updateWatchlist(status) {
      const watchlist = JSON.parse(localStorage.getItem("watchlist")) || {};
      if (status) {
        watchlist[this.movie.slug] = true;
      } else {
        delete watchlist[this.movie.slug];
      }
      localStorage.setItem("watchlist", JSON.stringify(watchlist));
      this.isInWatchlist = status;
    },
  },
};
</script>

<style scoped>
.movie-banner-box {
  width: 100%;
  border-radius: 16px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}
.movie-title {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #FFD369;
  font-weight: bold;
}
.movie-description {
  margin-bottom: 15px;
  color: #EEEEEE;
}
.movie-section-title {
  margin-bottom: 20px;
  color: #FFD369;
}
</style>
