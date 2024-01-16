import { createRouter, createWebHashHistory } from 'vue-router';
import Home from '../views/Home.vue';

const DEFAULT_TITLE = "Bond | The international development network";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: DEFAULT_TITLE },
  },
  {
    path: '/member/:id',
    name: 'Member',
    meta: { title: "Member | " + DEFAULT_TITLE },
    component: () => import('../views/Member.vue'),
  },
  {
    path: '/about',
    name: 'About',
    meta: { title: "About | " + DEFAULT_TITLE },
    component: () => import('../views/About.vue'),
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

router.beforeEach((to, from, next) => {
  if (to.name == "Home" && Object.values(to.query).filter((x) => x.length).length > 0) {
    document.title = "Search | " + DEFAULT_TITLE;
  } else {
    document.title = to.meta.title || DEFAULT_TITLE;
  }
  next();
});

export default router
