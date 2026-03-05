<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

interface SettingItem {
  label: string
  action: () => void
  danger?: boolean
}

const settings: SettingItem[] = [
  { label: '隐私政策', action: () => window.open('/api/v1/legal/privacy-policy') },
  { label: '用户协议', action: () => window.open('/api/v1/legal/user-agreement') },
  { label: '免责声明', action: () => window.open('/api/v1/legal/disclaimer') },
  { label: '关于球探 Pro', action: () => {} },
]

function handleLogout() {
  userStore.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-screen-lg mx-auto px-4 py-4">
      <h2 class="text-lg font-bold text-gray-800 mb-4">设置</h2>

      <!-- 设置项 -->
      <div class="bg-white rounded-xl overflow-hidden mb-6">
        <div
          v-for="(item, idx) in settings"
          :key="item.label"
          class="flex items-center justify-between px-4 py-3.5 cursor-pointer hover:bg-gray-50 transition-colors"
          :class="idx > 0 ? 'border-t border-gray-50' : ''"
          @click="item.action"
        >
          <span class="text-sm" :class="item.danger ? 'text-red-500' : 'text-gray-700'">{{ item.label }}</span>
          <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </div>

      <!-- 退出登录 -->
      <button
        class="w-full py-3 bg-white border border-red-200 text-red-500 rounded-xl text-sm font-medium hover:bg-red-50 transition-colors"
        @click="handleLogout"
      >
        退出登录
      </button>

      <!-- 版本信息 -->
      <p class="text-xs text-gray-400 text-center mt-6">球探 Pro V1.0 MVP</p>
    </div>
  </div>
</template>
