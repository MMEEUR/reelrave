import { createRouter, createWebHistory } from 'vue-router';
import RegisterPage from '@/components/RegisterPage.vue';
import LoginPage from '@/components/LoginPage.vue';
import ProfilePage from '@/components/ProfilePage.vue';
import MovieListPage from '@/components/MovieListPage.vue';
import MovieDetailPage from '@/components/MovieDetailPage.vue';

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
  },
  {
    path: '/movies',
    name: 'MoviesList',
    component: MovieListPage
  },
  {
    path: '/movies/:movie_slug',
    name: 'MovieDetail',
    component: MovieDetailPage
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;