<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const user = computed(() => userStore.user)

interface MenuItem {
  label: string
  icon: string
  route?: string
  action?: string
}

const menuItems: MenuItem[] = [
  { label: '我的竞猜', icon: 'prediction', route: '/prediction' },
  { label: '我的壁纸', icon: 'wallpaper', route: '/wallpaper' },
  { label: '设置', icon: 'settings' },
  { label: '退出登录', icon: 'logout', action: 'logout' },
]

function handleMenuClick(item: MenuItem) {
  if (item.action === 'logout') {
    userStore.logout()
    router.push({ name: 'login' })
  } else if (item.route) {
    router.push(item.route)
  }
}

function titleColor(title: string | null | undefined): string {
  if (!title) return ''
  if (title.includes('金')) return 'text-yellow-500'
  if (title.includes('银')) return 'text-gray-400'
  if (title.includes('铜')) return 'text-amber-600'
  return 'text-primary-500'
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- User header -->
    <section class="bg-gradient-to-br from-primary-600 to-primary-700 text-white px-4 pt-6 pb-10">
      <div class="max-w-screen-lg mx-auto">
        <div class="flex items-center gap-4">
          <!-- Avatar -->
          <div class="w-18 h-18 w-[72px] h-[72px] rounded-full bg-white/20 flex items-center justify-center overflow-hidden flex-shrink-0 ring-2 ring-white/30">
            <img
              v-if="user?.avatar"
              :src="user.avatar"
              alt="avatar"
              class="w-full h-full object-cover"
            />
            <svg v-else class="w-9 h-9 text-white/60" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
            </svg>
          </div>

          <div class="flex-1 min-w-0">
            <h1 class="text-xl font-bold truncate">{{ user?.nickname || '未登录' }}</h1>
            <div v-if="user?.title" class="mt-1">
              <span
                class="text-xs px-2 py-0.5 bg-white/20 backdrop-blur-sm rounded-full font-medium"
                :class="titleColor(user.title)"
              >
                {{ user.title }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div class="max-w-screen-lg mx-auto px-4 -mt-6">
      <!-- Stats cards -->
      <section class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-6">
        <div class="grid grid-cols-3 divide-x divide-gray-100">
          <!-- Points -->
          <div class="text-center px-2">
            <p class="text-2xl font-bold text-gray-800">{{ user?.points ?? 0 }}</p>
            <p class="text-xs text-gray-400 mt-1">积分</p>
          </div>

          <!-- Win streak -->
          <div class="text-center px-2">
            <div class="flex items-center justify-center gap-1">
              <p class="text-2xl font-bold text-gray-800">{{ user?.win_streak ?? 0 }}</p>
              <svg v-if="(user?.win_streak ?? 0) >= 3" class="w-5 h-5 text-orange-500" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 23c-4.97 0-9-3.58-9-8 0-3.07 2.13-5.64 3.5-7.13.39-.42 1.07-.17 1.1.4.12 2.14 1.23 3.8 2.4 4.46V12c0-4.56 3.93-8.86 5.47-10.37.38-.38 1.03-.14 1.08.39.33 3.7 2.88 6.78 3.95 8.48C21.67 12.4 21 14.81 21 15c0 4.42-4.03 8-9 8z" />
              </svg>
            </div>
            <p class="text-xs text-gray-400 mt-1">连胜</p>
          </div>

          <!-- Favorite team -->
          <div class="text-center px-2">
            <p class="text-2xl font-bold text-gray-800">
              {{ user?.fav_team_id ? '...' : '-' }}
            </p>
            <p class="text-xs text-gray-400 mt-1">关注球队</p>
          </div>
        </div>
      </section>

      <!-- Menu items -->
      <section class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <button
          v-for="(item, index) in menuItems"
          :key="item.label"
          class="w-full flex items-center justify-between px-4 py-4 hover:bg-gray-50 transition-colors text-left"
          :class="index < menuItems.length - 1 ? 'border-b border-gray-50' : ''"
          @click="handleMenuClick(item)"
        >
          <div class="flex items-center gap-3">
            <!-- Prediction icon -->
            <svg v-if="item.icon === 'prediction'" class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
            </svg>

            <!-- Wallpaper icon -->
            <svg v-else-if="item.icon === 'wallpaper'" class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <circle cx="8.5" cy="8.5" r="1.5" />
              <path d="M21 15l-5-5L5 21" />
            </svg>

            <!-- Settings icon -->
            <svg v-else-if="item.icon === 'settings'" class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="3" />
              <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 01-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z" />
            </svg>

            <!-- Logout icon -->
            <svg v-else-if="item.icon === 'logout'" class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4m7 14l5-5-5-5m5 5H9" />
            </svg>

            <span
              class="text-sm font-medium"
              :class="item.action === 'logout' ? 'text-red-500' : 'text-gray-700'"
            >
              {{ item.label }}
            </span>
          </div>

          <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </section>
    </div>
  </div>
</template>
