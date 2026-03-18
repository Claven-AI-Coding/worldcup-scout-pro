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
    <div class="mx-auto max-w-screen-lg px-4 py-4">
      <h2 class="mb-4 text-lg font-bold text-gray-800">设置</h2>

      <!-- 设置项 -->
      <div class="mb-6 overflow-hidden rounded-xl bg-white">
        <div
          v-for="(item, idx) in settings"
          :key="item.label"
          class="flex cursor-pointer items-center justify-between px-4 py-3.5 transition-colors hover:bg-gray-50"
          :class="idx > 0 ? 'border-t border-gray-50' : ''"
          @click="item.action"
        >
          <span class="text-sm" :class="item.danger ? 'text-red-500' : 'text-gray-700'">{{
            item.label
          }}</span>
          <svg
            class="h-4 w-4 text-gray-300"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </div>

      <!-- 退出登录 -->
      <button
        class="w-full rounded-xl border border-red-200 bg-white py-3 text-sm font-medium text-red-500 transition-colors hover:bg-red-50"
        @click="handleLogout"
      >
        退出登录
      </button>

      <!-- 版本信息 -->
      <p class="mt-6 text-center text-xs text-gray-400">球探 Pro V1.0 MVP</p>
    </div>
  </div>
</template>
