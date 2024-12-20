<template>
  <v-app style="background-color: #222831; min-height: 100vh;">
    <v-container class="login-page" style="color: #EEEEEE; min-height: 100vh;">
      <v-row justify="center" align="center" style="min-height: 100%;">
        <v-col cols="12" sm="8" md="6" lg="4">
          <v-card class="pa-5" style="background-color: #393E46; color: #EEEEEE;">
            <v-card-title class="justify-center">Login</v-card-title>
            <v-card-text>
              <v-form ref="loginForm" v-model="valid">
                <v-text-field
                  v-model="username"
                  label="Username or Email"
                  outlined
                  dense
                  :rules="[rules.required]"
                ></v-text-field>
                <v-text-field
                  v-model="password"
                  label="Password"
                  type="password"
                  outlined
                  dense
                  :rules="[rules.required]"
                ></v-text-field>
                <v-btn
                  :disabled="!valid"
                  block
                  color="#FFD369"
                  class="mt-4"
                  @click="login"
                >
                  Login
                </v-btn>
              </v-form>
            </v-card-text>
            <v-alert v-if="error" type="error" class="mt-3">
              {{ error }}
            </v-alert>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      valid: false,
      error: null,
      rules: {
        required: (v) => !!v || "This field is required",
      },
    };
  },
  methods: {
    async login() {
      this.error = null;
      try {
        const response = await axios.post("http://127.0.0.1:8000/accounts/login/", {
          username: this.username,
          password: this.password,
        });
        const { refresh, access, activity } = response.data;

        localStorage.setItem("refreshToken", refresh);
        localStorage.setItem("accessToken", access);

        localStorage.setItem("userActivity", JSON.stringify(activity));

        window.location.reload();
      } catch (err) {
        this.error = err.response?.data?.detail || "Login failed. Please try again.";
      }
    },
    async checkIfLoggedIn() {
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const response = await axios.post("http://127.0.0.1:8000/accounts/token/refresh/", {
            refresh: refreshToken,
          });
          if (response.status === 200 && response.data.access) {
            this.$router.replace("/profile");
          }
        } catch (error) {
          console.log("Token refresh failed. Token may be expired or invalid.", error);
        }
      }
    },
  },
  mounted() {
    this.checkIfLoggedIn();
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
</style>
