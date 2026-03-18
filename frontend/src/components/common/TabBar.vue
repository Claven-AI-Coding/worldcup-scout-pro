<script setup lang="ts">
import { useRoute } from 'vue-router'

const route = useRoute()

interface TabItem {
  name: string
  label: string
  path: string
  icon: string
}

// PRD 底部 Tab：首页 | 赛程 | 数据 | 社交 | 我的
const tabs: TabItem[] = [
  { name: 'home', label: '首页', path: '/', icon: 'home' },
  { name: 'schedule', label: '赛程', path: '/schedule', icon: 'schedule' },
  { name: 'data', label: '数据', path: '/data', icon: 'data' },
  { name: 'social', label: '社交', path: '/social', icon: 'social' },
  { name: 'profile', label: '我的', path: '/profile', icon: 'profile' },
]

function isActive(tab: TabItem): boolean {
  if (tab.path === '/') return route.path === '/'
  return route.path.startsWith(tab.path)
}
</script>

<template>
  <nav
    class="safe-area-bottom fixed bottom-0 left-0 right-0 z-50 border-t border-gray-200 bg-white"
  >
    <div class="mx-auto flex h-16 max-w-screen-lg items-center justify-around">
      <router-link
        v-for="tab in tabs"
        :key="tab.name"
        :to="tab.path"
        class="flex h-full flex-1 flex-col items-center justify-center transition-colors"
        :class="isActive(tab) ? 'text-green-600' : 'text-gray-400 hover:text-gray-600'"
      >
        <!-- 首页 -->
        <svg
          v-if="tab.icon === 'home'"
          class="h-6 w-6"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M3 9.5L12 3l9 6.5V20a1 1 0 01-1 1H4a1 1 0 01-1-1V9.5z"
          />
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 21V12h6v9" />
        </svg>

        <!-- 赛程 -->
        <svg
          v-else-if="tab.icon === 'schedule'"
          class="h-6 w-6"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          viewBox="0 0 24 24"
        >
          <rect x="3" y="4" width="18" height="18" rx="2" />
          <path stroke-linecap="round" d="M16 2v4M8 2v4M3 10h18" />
          <circle cx="12" cy="16" r="1.5" fill="currentColor" />
        </svg>

        <!-- 数据 -->
        <svg
          v-else-if="tab.icon === 'data'"
          class="h-6 w-6"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M3 3v18h18" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M7 16l4-5 4 3 5-7" />
        </svg>

        <!-- 社交 -->
        <svg
          v-else-if="tab.icon === 'social'"
          class="h-6 w-6"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"
          />
        </svg>

        <!-- 我的 -->
        <svg
          v-else-if="tab.icon === 'profile'"
          class="h-6 w-6"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          viewBox="0 0 24 24"
        >
          <circle cx="12" cy="8" r="4" />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"
          />
        </svg>

        <span class="mt-1 text-xs font-medium">{{ tab.label }}</span>
      </router-link>
    </div>
  </nav>
</template>

<style scoped>
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom, 0px);
}
</style>
