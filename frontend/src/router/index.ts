import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue'),
    },
    {
      path: '/schedule',
      name: 'schedule',
      component: () => import('@/views/Schedule.vue'),
    },
    {
      path: '/teams/:id',
      name: 'team-detail',
      component: () => import('@/views/TeamDetail.vue'),
    },
    {
      path: '/players/:id',
      name: 'player-detail',
      component: () => import('@/views/PlayerDetail.vue'),
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('@/views/Community.vue'),
    },
    {
      path: '/prediction',
      name: 'prediction',
      component: () => import('@/views/Prediction.vue'),
    },
    {
      path: '/wallpaper',
      name: 'wallpaper',
      component: () => import('@/views/Wallpaper.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/Profile.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue'),
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  const authRequired = ['profile', 'prediction']
  if (authRequired.includes(to.name as string) && !token) {
    next({ name: 'login' })
  } else {
    next()
  }
})

export default router
