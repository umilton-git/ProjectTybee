import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'setup',
      component: () => import('../views/SetupView.vue')
    },
    {
      path: '/session',
      name: 'session',
      component: () => import('../views/SessionView.vue')
    }
  ]
})

export default router