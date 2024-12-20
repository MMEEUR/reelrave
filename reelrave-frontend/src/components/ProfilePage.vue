<template>
    <v-app style="background-color: #222831; min-height: 100vh;">
      <v-container>
        <v-row justify="center" class="pa-5">
          <v-col cols="12" md="8" lg="6">
            <v-card elevation="3" class="pa-3" style="background-color: #393E46;">
              <v-card-title class="d-flex justify-space-between">
                <span class="text-h5" style="color: #FFD369">Profile</span>
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
                      <v-list-item v-for="(item, index) in user.watchlist" :key="index">
                        <v-list-item-avatar>
                          <img :src="item.content_object.baner" alt="Movie Poster" />
                        </v-list-item-avatar>
                        <v-list-item-content>
                          <v-list-item-title style="color: #FFFFFF">{{ item.content_object.name }}</v-list-item-title>
                          <v-list-item-subtitle style="color: #FFD369">
                            {{ item.content_object.genre.map(genre => genre.name).join(', ') }}
                          </v-list-item-subtitle>
                          <v-list-item-subtitle style="color: #FFFFFF">
                            {{ item.content_object.release_date }} | {{ item.content_object.time }} | Rating: {{ item.content_object.average_rating }}
                          </v-list-item-subtitle>
                        </v-list-item-content>
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
      }
    },
    mounted() {
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
