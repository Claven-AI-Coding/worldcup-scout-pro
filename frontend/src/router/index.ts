import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior(_to, _from, savedPosition) {
    return savedPosition || { top: 0 }
  },
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
      path: '/matches/:id',
      name: 'match-detail',
      component: () => import('@/views/MatchDetail.vue'),
    },
    // 数据 Tab
    {
      path: '/data',
      name: 'data',
      component: () => import('@/views/Data.vue'),
    },
    {
      path: '/rankings',
      name: 'rankings',
      component: () => import('@/views/Rankings.vue'),
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
    // 社交 Tab
    {
      path: '/social',
      name: 'social',
      component: () => import('@/views/Social.vue'),
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('@/views/Community.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/prediction',
      name: 'prediction',
      component: () => import('@/views/Prediction.vue'),
      meta: { requiresAuth: true },
    },
    // 工具
    {
      path: '/wallpaper',
      name: 'wallpaper',
      component: () => import('@/views/Wallpaper.vue'),
    },
    // 我的
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/Profile.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/tasks',
      name: 'task-center',
      component: () => import('@/views/TaskCenter.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/membership',
      name: 'membership',
      component: () => import('@/views/Membership.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/settings',
      name: 'settings',
      component: () => import('@/views/Settings.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue'),
      meta: { guest: true },
    },
    // 404 兜底
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      redirect: '/',
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')

  // 需要登录的页面 → 未登录跳转登录页，记录来源
  if (to.meta.requiresAuth && !token) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // 已登录用户访问登录页 → 跳转首页
  if (to.meta.guest && token) {
    next({ name: 'home' })
    return
  }

  next()
})

export default router
