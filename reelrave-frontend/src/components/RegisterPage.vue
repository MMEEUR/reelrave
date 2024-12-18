<template>
  <v-container class="d-flex justify-center align-center" style="height: 100vh">
    <v-card class="pa-6" elevation="3" style="background-color: #222831; width: 400px;">
      <v-card-title class="justify-center" style="color: #EEEEEE;">
        <h2>Register</h2>
      </v-card-title>

      <v-card-text>
        <v-form ref="form" v-model="valid">
          <!-- Username -->
          <v-text-field
            v-model="formData.username"
            label="Username"
            outlined
            :rules="[rules.required, rules.username]"
            style="color: #FFD369"
            @input="debounceCheck"
          />

          <!-- Email -->
          <v-text-field
            v-model="formData.email"
            label="Email"
            outlined
            :rules="[rules.required, rules.email, rules.checkEmailUsage]"
            style="color: #FFD369"
            @input="debounceCheck"
          />

          <!-- Password -->
          <v-text-field
            v-model="formData.password"
            label="Password"
            type="password"
            outlined
            :rules="[rules.required, rules.min(6)]"
            style="color: #FFD369"
          />

          <!-- Confirm Password -->
          <v-text-field
            v-model="formData.confirm_password"
            label="Confirm Password"
            type="password"
            outlined
            :rules="[rules.required, rules.matchPassword(formData.password)]"
            style="color: #FFD369"
          />

          <!-- Email Code -->
          <v-text-field
            v-model="formData.email_code"
            label="Email Code"
            outlined
            :rules="[rules.required]"
            style="color: #FFD369"
          />

          <!-- Error Message -->
          <v-alert
            v-if="error"
            type="error"
            class="mt-3"
            style="background-color: #393E46; color: white"
          >
            {{ error }}
          </v-alert>

          <!-- Register Button -->
          <v-btn
            block
            class="mt-4"
            elevation="2"
            style="background-color: #FFD369; color: #222831"
            :disabled="!valid"
            @click="register"
          >
            Register
          </v-btn>
        </v-form>

        <v-divider class="my-4" style="background-color: #EEEEEE;"></v-divider>

        <!-- Resend Code Section -->
        <v-btn
          block
          class="mt-2"
          elevation="2"
          style="background-color: #393E46; color: white"
          @click="resendCode"
        >
          Resend Code
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";
import debounce from "lodash/debounce";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export default {
  data() {
    return {
      valid: false,
      error: "",
      formData: {
        username: "",
        email: "",
        password: "",
        confirm_password: "",
        email_code: "",
      },
      rules: {
        required: (value) => !!value || "This field is required.",
        email: (value) =>
          /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) || "Invalid email format.",
        username: (value) => !this.usernameTaken || "The username is already in use.",
        checkEmailUsage: (value) => !this.emailTaken || "The email is already in use.",
        min: (minLength) => (value) =>
          value.length >= minLength || `Minimum ${minLength} characters required.`,
        matchPassword: (password) => (value) =>
          value === password || "Passwords must match.",
      },
      usernameTaken: false,
      emailTaken: false,
      debounceCheck: null,
    };
  },
  created() {
    this.debounceCheck = debounce(this.checkUsernameEmail, 500);
  },
  methods: {
    async register() {
      try {
        const response = await axiosInstance.post("/accounts/register/", this.formData);
        alert("Registration successful!");
        this.$router.push("/login");
      } catch (error) {
        if (Array.isArray(error.response?.data)) {
          this.error = error.response.data.join(", ");
        } else if (error.response?.data && typeof error.response.data === "object") {
          this.error = Object.values(error.response.data)
            .flat()
            .join(", ");
        } else {
          this.error = "An unexpected error occurred. Please try again later.";
        }
        this.clearErrorAfterDelay();
      }
    },
    async resendCode() {
      try {
        await axiosInstance.post("/accounts/resend-code/", {
          email: this.formData.email,
        });
        alert("Code sent to your email.");
      } catch (error) {
        if (Array.isArray(error.response?.data)) {
          this.error = error.response.data.join(", ");
        } else if (error.response?.data && typeof error.response.data === "object") {
          this.error = Object.values(error.response.data)
            .flat()
            .join(", ");
        } else {
          this.error = "An unexpected error occurred. Please try again later.";
        }
        this.clearErrorAfterDelay();
      }
    },
    async checkUsernameEmail() {
      try {
        const response = await axiosInstance.post("/accounts/check-username-email/", {
          username: this.formData.username,
          email: this.formData.email,
        });

        this.usernameTaken = response.data.username || false;
        this.emailTaken = response.data.email || false;
      } catch (error) {
        this.error = "Error checking username or email.";
        this.clearErrorAfterDelay();
      }
    },
    clearErrorAfterDelay() {
      setTimeout(() => {
        this.error = "";
      }, 2000);
    },
  },
};
</script>

<style>
body {
  background-color: #222831;
  font-family: "Roboto", sans-serif;
}
</style>
