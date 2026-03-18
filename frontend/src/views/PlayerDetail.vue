<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPlayer } from '@/api/players'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const route = useRoute()
const router = useRouter()

interface Player {
  id: number
  team_id: number
  name: string
  number: number | null
  position: string | null
  age: number | null
  club: string | null
  stats?: Record<string, unknown> | null
}

const player = ref<Player | null>(null)
const loading = ref(false)

const playerId = computed(() => Number(route.params.id))

const positionLabel = computed(() => {
  if (!player.value?.position) return '未知'
  const map: Record<string, string> = {
    GK: '门将',
    DF: '后卫',
    MF: '中场',
    FW: '前锋',
  }
  return map[player.value.position] || player.value.position
})

const positionClass = computed(() => {
  if (!player.value?.position) return 'bg-gray-100 text-gray-600'
  const map: Record<string, string> = {
    GK: 'bg-yellow-100 text-yellow-700',
    DF: 'bg-blue-100 text-blue-700',
    MF: 'bg-green-100 text-green-700',
    FW: 'bg-red-100 text-red-700',
  }
  return map[player.value.position] || 'bg-gray-100 text-gray-600'
})

// 世界杯数据中文标签
const statsLabelMap: Record<string, string> = {
  goals: '进球',
  assists: '助攻',
  appearances: '出场',
  yellow_cards: '黄牌',
  red_cards: '红牌',
  shots: '射门',
  passes: '传球',
  minutes_played: '出场时间(分钟)',
}

// 核心数据（进球/助攻/出场）
const coreStats = computed(() => {
  if (!player.value?.stats) return []
  const s = player.value.stats as Record<string, number>
  return [
    { key: 'goals', label: '进球', value: s.goals ?? 0, color: 'text-red-500' },
    { key: 'assists', label: '助攻', value: s.assists ?? 0, color: 'text-blue-500' },
    { key: 'appearances', label: '出场', value: s.appearances ?? 0, color: 'text-green-600' },
  ]
})

// 详细数据（其余字段）
const detailStats = computed(() => {
  if (!player.value?.stats) return []
  const s = player.value.stats as Record<string, unknown>
  const coreKeys = new Set(['goals', 'assists', 'appearances'])
  return Object.entries(s)
    .filter(([k]) => !coreKeys.has(k))
    .map(([k, v]) => ({ key: k, label: statsLabelMap[k] || k, value: v }))
})

onMounted(async () => {
  loading.value = true
  try {
    const res = await getPlayer(playerId.value)
    player.value = res.data
  } catch {
    player.value = null
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <LoadingSpinner v-if="loading" text="加载球员信息..." />

    <template v-else-if="player">
      <!-- Player header -->
      <section class="bg-gradient-to-br from-gray-800 to-gray-900 px-4 py-8 text-white">
        <div class="mx-auto max-w-screen-lg">
          <!-- Back button -->
          <button
            class="mb-4 flex items-center gap-1 text-sm text-gray-400 transition-colors hover:text-white"
            @click="router.back()"
          >
            <svg
              class="h-4 w-4"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" d="M15 19l-7-7 7-7" />
            </svg>
            返回
          </button>

          <div class="flex items-center gap-5">
            <!-- Photo placeholder -->
            <div class="relative h-24 w-24 flex-shrink-0">
              <div
                class="flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-gray-600 to-gray-700"
              >
                <svg class="h-12 w-12 text-gray-500" fill="currentColor" viewBox="0 0 24 24">
                  <path
                    d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"
                  />
                </svg>
              </div>
              <span
                v-if="player.number !== null"
                class="absolute -bottom-1 -right-1 flex h-10 w-10 items-center justify-center rounded-full bg-primary-500 text-lg font-bold text-white shadow-lg"
              >
                {{ player.number }}
              </span>
            </div>

            <div>
              <h1 class="text-2xl font-bold">
                {{ player.name }}
              </h1>
              <div class="mt-2 flex flex-wrap items-center gap-3">
                <span class="rounded-full px-2.5 py-1 text-xs font-medium" :class="positionClass">
                  {{ positionLabel }}
                </span>
                <span v-if="player.age" class="text-sm text-gray-400">{{ player.age }} 岁</span>
              </div>
              <p v-if="player.club" class="mt-1 text-sm text-gray-400">
                {{ player.club }}
              </p>
            </div>
          </div>
        </div>
      </section>

      <div class="mx-auto max-w-screen-lg space-y-6 px-4 py-6">
        <!-- Player info card -->
        <section class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm">
          <h2 class="border-b border-gray-100 bg-gray-50 px-4 py-3 text-sm font-bold text-gray-700">
            基本信息
          </h2>
          <div class="divide-y divide-gray-50">
            <div class="flex items-center justify-between px-4 py-3">
              <span class="text-sm text-gray-500">姓名</span>
              <span class="text-sm font-medium text-gray-800">{{ player.name }}</span>
            </div>
            <div v-if="player.number !== null" class="flex items-center justify-between px-4 py-3">
              <span class="text-sm text-gray-500">球衣号码</span>
              <span class="text-sm font-medium text-gray-800">{{ player.number }}</span>
            </div>
            <div class="flex items-center justify-between px-4 py-3">
              <span class="text-sm text-gray-500">位置</span>
              <span
                class="text-sm font-medium"
                :class="positionClass.replace('bg-', 'text-').split(' ')[1]"
              >
                {{ positionLabel }}
              </span>
            </div>
            <div v-if="player.age" class="flex items-center justify-between px-4 py-3">
              <span class="text-sm text-gray-500">年龄</span>
              <span class="text-sm font-medium text-gray-800">{{ player.age }}</span>
            </div>
            <div v-if="player.club" class="flex items-center justify-between px-4 py-3">
              <span class="text-sm text-gray-500">所属俱乐部</span>
              <span class="text-sm font-medium text-gray-800">{{ player.club }}</span>
            </div>
          </div>
        </section>

        <!-- 世界杯数据统计 -->
        <section v-if="player.stats && Object.keys(player.stats).length > 0">
          <div class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm">
            <h2
              class="border-b border-gray-100 bg-gray-50 px-4 py-3 text-sm font-bold text-gray-700"
            >
              世界杯数据
            </h2>

            <!-- 核心数据卡片 -->
            <div class="grid grid-cols-3 gap-px bg-gray-100">
              <div v-for="item in coreStats" :key="item.key" class="bg-white p-3 text-center">
                <p class="text-xl font-bold" :class="item.color">
                  {{ item.value }}
                </p>
                <p class="mt-1 text-xs text-gray-400">
                  {{ item.label }}
                </p>
              </div>
            </div>

            <!-- 详细数据 -->
            <div class="divide-y divide-gray-50">
              <div
                v-for="item in detailStats"
                :key="item.key"
                class="flex items-center justify-between px-4 py-3"
              >
                <span class="text-sm text-gray-500">{{ item.label }}</span>
                <span class="text-sm font-medium text-gray-800">{{ item.value }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- Team link -->
        <section class="pb-4">
          <router-link
            :to="{ name: 'team-detail', params: { id: player.team_id } }"
            class="block w-full rounded-xl border border-gray-200 bg-white py-3 text-center text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50"
          >
            查看所属球队
          </router-link>
        </section>
      </div>
    </template>

    <EmptyState v-else message="球员不存在" action-text="返回首页" @action="router.push('/')" />
  </div>
</template>
