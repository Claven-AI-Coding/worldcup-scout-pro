<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getDailyTasks, signIn } from '@/api/tasks'
import { useUserStore } from '@/stores/user'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const userStore = useUserStore()

interface Task {
  id: number
  task_type: string
  completed: boolean
  points_reward: number
}

const tasks = ref<Task[]>([])
const loading = ref(false)
const signedIn = ref(false)
const signInPoints = ref(0)

const taskLabels: Record<string, string> = {
  daily_sign_in: '每日签到',
  view_schedule: '查看赛程',
  share_content: '分享内容',
  join_circle: '加入圈子',
  predict_match: '参与竞猜',
}

const taskIcons: Record<string, string> = {
  daily_sign_in: '📝',
  view_schedule: '📅',
  share_content: '📤',
  join_circle: '👥',
  predict_match: '🎯',
}

async function loadTasks() {
  loading.value = true
  try {
    const res = await getDailyTasks()
    tasks.value = res.data.items
  } catch {
    // 加载失败
  } finally {
    loading.value = false
  }
}

async function handleSignIn() {
  try {
    const res = await signIn()
    signedIn.value = true
    signInPoints.value = res.data.points_earned
    await userStore.fetchUser()
    await loadTasks()
  } catch {
    signedIn.value = true // 已签到
  }
}

onMounted(loadTasks)
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="mx-auto max-w-screen-lg px-4 py-4">
      <!-- 签到卡片 -->
      <div class="mb-4 rounded-xl bg-gradient-to-r from-green-500 to-green-600 p-6 text-white">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-lg font-bold">每日签到</h2>
            <p class="mt-1 text-sm text-white/70">
              {{ signedIn ? `已获得 ${signInPoints} 积分` : '签到领取积分奖励' }}
            </p>
          </div>
          <button
            class="rounded-full px-6 py-2 text-sm font-bold transition-all"
            :class="
              signedIn ? 'bg-white/30 text-white/70' : 'bg-white text-green-600 hover:bg-green-50'
            "
            :disabled="signedIn"
            @click="handleSignIn"
          >
            {{ signedIn ? '已签到' : '签到' }}
          </button>
        </div>
        <div class="mt-3 text-sm text-white/60">当前积分：{{ userStore.user?.points || 0 }}</div>
      </div>

      <!-- 每日任务列表 -->
      <div class="rounded-xl bg-white p-4">
        <h3 class="mb-3 text-sm font-bold text-gray-700">每日任务</h3>

        <LoadingSpinner v-if="loading" text="加载任务..." />

        <div v-else class="space-y-3">
          <div
            v-for="task in tasks"
            :key="task.id"
            class="flex items-center justify-between border-b border-gray-50 py-2 last:border-0"
          >
            <div class="flex items-center gap-3">
              <span class="text-lg">{{ taskIcons[task.task_type] || '📋' }}</span>
              <div>
                <p class="text-sm text-gray-700">
                  {{ taskLabels[task.task_type] || task.task_type }}
                </p>
                <p class="text-xs text-gray-400">+{{ task.points_reward }} 积分</p>
              </div>
            </div>
            <span
              class="rounded-full px-3 py-1 text-xs"
              :class="task.completed ? 'bg-gray-100 text-gray-400' : 'bg-green-100 text-green-600'"
            >
              {{ task.completed ? '已完成' : '待完成' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
