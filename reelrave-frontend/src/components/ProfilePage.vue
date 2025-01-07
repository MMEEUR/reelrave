<template>
  <v-app style="background-color: #222831; min-height: 100vh;">
    <v-container>
      <v-row justify="center" class="pa-5">
        <v-col cols="12" md="8" lg="6">
          <v-card elevation="3" class="pa-3" style="background-color: #393E46;">
            <v-card-title class="d-flex justify-space-between">
              <span class="text-h5" style="color: #FFD369">Profile</span>
              <v-btn color="#FFD369" @click="logout">Logout</v-btn>
            </v-card-title>
            <v-card-subtitle class="mb-3" style="color: #EEEEEE">
              Manage your account details
            </v-card-subtitle>
            <v-card-text>
              <v-row>
                <v-col cols="12" >
                  <v-list dense style="background-color: #393E46;">
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title style="color: #FFD369">Username</v-list-item-title>
                        <v-list-item-subtitle style="color: #FFFFFF">{{ user.username }}</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-content>
                        <v-list-item-title style="color: #FFD369">Email</v-list-item-title>
                        <v-list-item-subtitle style="color: #FFFFFF">{{ user.email }}</v-list-item-subtitle>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-col>
              </v-row>
              <v-divider class="my-4"></v-divider>
              <v-row>
                <v-col cols="12">
                  <h3 style="color: #FFD369">Watchlist</h3>
                  <v-list style="background-color: #393E46;">
                    <v-list-item v-for="(item, index) in user.watchlist" :key="index" style="margin-bottom: 10px;">
                      <v-row>
                        <v-col cols="4">
                          <v-img :src="item.content_object.baner" alt="Movie Poster" contain></v-img>
                        </v-col>
                        <v-col cols="8" class="d-flex flex-column justify-center">
                          <v-list-item-title style="color: #FFFFFF; font-weight: bold;">{{ item.content_object.name }}</v-list-item-title>
                          <v-list-item-subtitle style="color: #FFD369; font-style: italic;">
                            {{ item.content_object.genre.map(genre => genre.name).join(', ') }}
                          </v-list-item-subtitle>
                          <v-list-item-subtitle style="color: #FFFFFF;">
                            {{ item.content_object.release_date }} | {{ item.content_object.time }} | Rating: {{ item.content_object.average_rating }}
                          </v-list-item-subtitle>
                          <v-btn color="#FF4C4C" x-small @click="removeFromWatchlist(item.content_object.get_absolute_url)">Remove</v-btn>
                        </v-col>
                      </v-row>
                    </v-list-item>
                  </v-list>
                </v-col>
              </v-row>
            </v-card-text>
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
      user: {
        username: '',
        email: '',
        watchlist: []
      }
    };
  },
  methods: {
    async checkIfLoggedIn() {
      const refreshToken = localStorage.getItem('refreshToken');
      if (!refreshToken) {
        this.$router.replace('/login');
        return;
      }
      try {
        const response = await axios.post("http://127.0.0.1:8000/accounts/token/refresh/", {
          refresh: refreshToken,
        });
        if (response.status !== 200 || !response.data.access) {
          this.$router.replace('/login');
        }
      } catch (error) {
        console.log("Token refresh failed. Token may be expired or invalid.", error);
        this.$router.replace('/login');
      }
    },
    async fetchProfile() {
      try {
        const tokenResponse = await axios.post('http://127.0.0.1:8000/accounts/token/refresh/', {
          refresh: localStorage.getItem('refreshToken')
        });

        const accessToken = tokenResponse.data.access;
        const profileResponse = await axios.get('http://127.0.0.1:8000/accounts/profile/', {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });

        this.user = profileResponse.data;
        this.user.watchlist.forEach(item => {
          item.content_object.baner = `http://127.0.0.1:8000${item.content_object.baner}`;
        });
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async removeFromWatchlist(movieUrl) {
      try {
        const tokenResponse = await axios.post('http://127.0.0.1:8000/accounts/token/refresh/', {
          refresh: localStorage.getItem('refreshToken')
        });
        const accessToken = tokenResponse.data.access;

        await axios.delete(`http://127.0.0.1:8000${movieUrl}watchlist/`, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        });

        // Extract slug from get_absolute_url
        const slug = movieUrl.split('/').filter(Boolean).pop();

        // Remove from localStorage
        const watchlist = JSON.parse(localStorage.getItem('watchlist') || '{}');
        delete watchlist[slug];
        localStorage.setItem('watchlist', JSON.stringify(watchlist));

        this.fetchProfile();
      } catch (error) {
        console.error('Error removing movie from watchlist:', error);
      }
    },
    logout() {
      localStorage.removeItem('refreshToken');
      window.location.reload();
    }
  },
  mounted() {
    this.checkIfLoggedIn();
    this.fetchProfile();
  }
};
</script>

<style scoped>
.v-card {
  background-color: #393E46;
  color: #FFFFFF;
}
</style>
