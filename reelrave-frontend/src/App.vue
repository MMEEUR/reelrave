<template>
  <v-app>
    <!-- Navbar -->
    <v-app-bar app color="#393E46" dark>
      <v-toolbar-title>ReelRave</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn text color="#FFD369" to="/">Home</v-btn>
      <v-btn text color="#FFD369" to="/movies">Movies</v-btn>
      <v-btn text color="#FFD369" to="/shows">Shows</v-btn>
      <v-btn text color="#FFD369" to="/persons">Persons</v-btn>
      <v-btn text color="#FFD369" to="/genres">Genres</v-btn>

      <template v-if="isLoggedIn">
        <v-btn text color="#FFD369" to="/profile">Profile</v-btn>
      </template>
      <template v-else>
        <v-btn text color="#FFD369" to="/register">Register</v-btn>
        <v-btn text color="#FFD369" to="/login">Login</v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      isLoggedIn: false,
    };
  },
  methods: {
    async checkIfLoggedIn() {
      const refreshToken = localStorage.getItem("refreshToken");
      if (refreshToken) {
        try {
          const response = await axios.post("http://127.0.0.1:8000/accounts/token/refresh/", {
            refresh: refreshToken,
          });
          if (response.status === 200 && response.data.access) {
            this.isLoggedIn = true;
          } else {
            this.isLoggedIn = false;
          }
        } catch (error) {
          console.log("Token refresh failed. Token may be expired or invalid.", error);
          this.isLoggedIn = false;
        }
      } else {
        this.isLoggedIn = false;
      }
    },
  },
  created() {
    this.checkIfLoggedIn();
  },
};
</script>

<style>
body {
  margin: 0;
  font-family: "Roboto", sans-serif;
  background-color: #222831;
  color: #EEEEEE;
}
</style>