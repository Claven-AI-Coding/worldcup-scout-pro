<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { getPointRecords } from '@/api/points'
import EmptyState from '@/components/common/EmptyState.vue'

const router = useRouter()
const userStore = useUserStore()
const user = computed(() => userStore.user)

// 记录Tab
type RecordTab = 'points' | 'predictions' | 'posts'
const activeTab = ref<RecordTab>('points')

// 积分记录
interface PointRecord {
  id: number
  amount: number
  reason: string
  detail: string | null
  created_at: string
}
const pointRecords = ref<PointRecord[]>([])
const loadingRecords = ref(false)

const reasonLabels: Record<string, string> = {
  sign_in: '签到',
  prediction: '竞猜',
  task: '任务',
  exchange: '兑换',
}

async function fetchPointRecords() {
  loadingRecords.value = true
  try {
    const res = await getPointRecords({ limit: 30 })
    pointRecords.value = res.data.items || res.data || []
  } catch {
    pointRecords.value = []
  } finally {
    loadingRecords.value = false
  }
}

function formatTime(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 菜单
interface MenuItem {
  label: string
  icon: string
  route?: string
  action?: string
}
const menuItems: MenuItem[] = [
  { label: '任务中心', icon: 'task', route: '/tasks' },
  { label: '我的竞猜', icon: 'prediction', route: '/prediction' },
  { label: '我的壁纸', icon: 'wallpaper', route: '/wallpaper' },
  { label: '会员中心', icon: 'member', route: '/membership' },
  { label: '设置', icon: 'settings', route: '/settings' },
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

onMounted(fetchPointRecords)
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 用户头部 -->
    <section class="bg-gradient-to-br from-primary-600 to-primary-700 px-4 pb-10 pt-6 text-white">
      <div class="mx-auto max-w-screen-lg">
        <div class="flex items-center gap-4">
          <div
            class="flex h-[72px] w-[72px] flex-shrink-0 items-center justify-center overflow-hidden rounded-full bg-white/20 ring-2 ring-white/30"
          >
            <img
              v-if="user?.avatar"
              :src="user.avatar"
              alt="avatar"
              class="h-full w-full object-cover"
            />
            <svg v-else class="h-9 w-9 text-white/60" fill="currentColor" viewBox="0 0 24 24">
              <path
                d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"
              />
            </svg>
          </div>
          <div class="min-w-0 flex-1">
            <h1 class="truncate text-xl font-bold">
              {{ user?.nickname || '未登录' }}
            </h1>
            <div v-if="user?.title" class="mt-1">
              <span
                class="rounded-full bg-white/20 px-2 py-0.5 text-xs font-medium backdrop-blur-sm"
                :class="titleColor(user.title)"
                >{{ user.title }}</span
              >
            </div>
            <p v-if="user?.is_member" class="mt-1 text-xs text-primary-200">VIP 会员</p>
          </div>
        </div>
      </div>
    </section>

    <div class="mx-auto -mt-6 max-w-screen-lg px-4">
      <!-- 数据卡片 -->
      <section class="mb-4 rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
        <div class="grid grid-cols-3 divide-x divide-gray-100">
          <div class="px-2 text-center">
            <p class="text-2xl font-bold text-gray-800">
              {{ user?.points ?? 0 }}
            </p>
            <p class="mt-1 text-xs text-gray-400">积分</p>
          </div>
          <div class="px-2 text-center">
            <div class="flex items-center justify-center gap-1">
              <p class="text-2xl font-bold text-gray-800">
                {{ user?.win_streak ?? 0 }}
              </p>
              <svg
                v-if="(user?.win_streak ?? 0) >= 3"
                class="h-5 w-5 text-orange-500"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path
                  d="M12 23c-4.97 0-9-3.58-9-8 0-3.07 2.13-5.64 3.5-7.13.39-.42 1.07-.17 1.1.4.12 2.14 1.23 3.8 2.4 4.46V12c0-4.56 3.93-8.86 5.47-10.37.38-.38 1.03-.14 1.08.39.33 3.7 2.88 6.78 3.95 8.48C21.67 12.4 21 14.81 21 15c0 4.42-4.03 8-9 8z"
                />
              </svg>
            </div>
            <p class="mt-1 text-xs text-gray-400">连胜</p>
          </div>
          <div class="px-2 text-center">
            <p class="text-2xl font-bold text-gray-800">
              {{ user?.fav_team_id ? '...' : '-' }}
            </p>
            <p class="mt-1 text-xs text-gray-400">关注球队</p>
          </div>
        </div>
      </section>

      <!-- 记录中心 -->
      <section class="mb-4 overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm">
        <div class="flex border-b border-gray-100">
          <button
            v-for="tab in [
              { key: 'points' as const, label: '积分记录' },
              { key: 'predictions' as const, label: '竞猜记录' },
              { key: 'posts' as const, label: '发布记录' },
            ]"
            :key="tab.key"
            class="flex-1 py-3 text-xs font-medium transition-colors"
            :class="
              activeTab === tab.key
                ? 'border-b-2 border-primary-500 text-primary-600'
                : 'text-gray-400'
            "
            @click="activeTab = tab.key"
          >
            {{ tab.label }}
          </button>
        </div>

        <div class="max-h-60 overflow-y-auto p-4">
          <!-- 积分记录 -->
          <template v-if="activeTab === 'points'">
            <div v-if="pointRecords.length > 0" class="space-y-2">
              <div
                v-for="r in pointRecords"
                :key="r.id"
                class="flex items-center justify-between text-sm"
              >
                <div>
                  <span class="text-gray-700">{{ reasonLabels[r.reason] || r.reason }}</span>
                  <span v-if="r.detail" class="ml-1 text-xs text-gray-400">{{ r.detail }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <span
                    :class="r.amount > 0 ? 'text-green-600' : 'text-red-500'"
                    class="font-medium"
                  >
                    {{ r.amount > 0 ? '+' : '' }}{{ r.amount }}
                  </span>
                  <span class="text-xs text-gray-300">{{ formatTime(r.created_at) }}</span>
                </div>
              </div>
            </div>
            <EmptyState v-else message="暂无积分记录" />
          </template>

          <!-- 竞猜/发布记录占位 -->
          <template v-else>
            <EmptyState message="暂无记录" />
          </template>
        </div>
      </section>

      <!-- 菜单 -->
      <section class="mb-6 overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm">
        <button
          v-for="(item, index) in menuItems"
          :key="item.label"
          class="flex w-full items-center justify-between px-4 py-3.5 text-left transition-colors hover:bg-gray-50"
          :class="index < menuItems.length - 1 ? 'border-b border-gray-50' : ''"
          @click="handleMenuClick(item)"
        >
          <span
            class="text-sm font-medium"
            :class="item.action === 'logout' ? 'text-red-500' : 'text-gray-700'"
            >{{ item.label }}</span
          >
          <svg
            class="h-4 w-4 text-gray-300"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </section>
    </div>
  </div>
</template>
