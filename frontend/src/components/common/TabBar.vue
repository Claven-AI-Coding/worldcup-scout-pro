<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

interface TabItem {
  name: string
  label: string
  path: string
  icon: string
}

const tabs: TabItem[] = [
  {
    name: 'home',
    label: '首页',
    path: '/',
    icon: 'home',
  },
  {
    name: 'schedule',
    label: '赛程',
    path: '/schedule',
    icon: 'schedule',
  },
  {
    name: 'community',
    label: '圈子',
    path: '/community',
    icon: 'community',
  },
  {
    name: 'prediction',
    label: '竞猜',
    path: '/prediction',
    icon: 'prediction',
  },
  {
    name: 'profile',
    label: '我的',
    path: '/profile',
    icon: 'profile',
  },
]

function isActive(tab: TabItem): boolean {
  if (tab.path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(tab.path)
}
</script>

<template>
  <nav class="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-gray-200">
    <div class="flex items-center justify-around h-16 max-w-screen-lg mx-auto">
      <router-link
        v-for="tab in tabs"
        :key="tab.name"
        :to="tab.path"
        class="flex flex-col items-center justify-center flex-1 h-full transition-colors"
        :class="isActive(tab) ? 'text-primary-500' : 'text-gray-400 hover:text-gray-600'"
      >
        <!-- Home icon -->
        <svg v-if="tab.icon === 'home'" class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 9.5L12 3l9 6.5V20a1 1 0 01-1 1H4a1 1 0 01-1-1V9.5z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 21V12h6v9" />
        </svg>

        <!-- Schedule icon -->
        <svg v-else-if="tab.icon === 'schedule'" class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
          <rect x="3" y="4" width="18" height="18" rx="2" />
          <path stroke-linecap="round" d="M16 2v4M8 2v4M3 10h18" />
          <circle cx="12" cy="16" r="1.5" fill="currentColor" />
        </svg>

        <!-- Community icon -->
        <svg v-else-if="tab.icon === 'community'" class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a4 4 0 00-3-3.87M9 20H4v-2a4 4 0 013-3.87" />
          <circle cx="9" cy="7" r="4" />
          <circle cx="17" cy="7" r="4" />
        </svg>

        <!-- Prediction icon -->
        <svg v-else-if="tab.icon === 'prediction'" class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
        </svg>

        <!-- Profile icon -->
        <svg v-else-if="tab.icon === 'profile'" class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
          <circle cx="12" cy="8" r="4" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
        </svg>

        <span class="text-xs mt-1 font-medium">{{ tab.label }}</span>
      </router-link>
    </div>
  </nav>
</template>
