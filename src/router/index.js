import { createRouter, createWebHashHistory } from 'vue-router';
import { trackRouter } from "vue-gtag-next";
import Home from '../views/Home.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/member/:id',
    name: 'Member',
    component: () => import('../views/Member.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { left: 0, top: 0 }
    }
  },
});

trackRouter(router);

export default router
