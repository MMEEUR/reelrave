import { createRouter, createWebHistory } from 'vue-router';
import RegisterPage from '@/components/RegisterPage.vue';
import LoginPage from '@/components/LoginPage.vue';
import ProfilePage from '@/components/ProfilePage.vue';

const routes = [
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfilePage
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;