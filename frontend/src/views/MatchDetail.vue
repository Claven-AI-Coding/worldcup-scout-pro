<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getMatch, getMatchEvents } from '@/api/matches'
import { useToast } from '@/composables/useToast'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import AIPrediction from '@/components/match/AIPrediction.vue'
import ReminderSetting from '@/components/match/ReminderSetting.vue'
import LiveScore from '@/components/match/LiveScore.vue'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const matchId = Number(route.params.id)

interface Team {
  id: number
  name: string
  code: string
  flag_url: string | null
}

interface MatchEvent {
  id: number
  event_type: string
  minute: number
  player_id: number | null
  detail: string | null
}

interface MatchData {
  id: number
  stage: string
  group_name: string | null
  home_team: Team
  away_team: Team
  home_score: number | null
  away_score: number | null
  status: string
  start_time: string
  venue: string | null
  matchday: number | null
  events: MatchEvent[]
}

const match = ref<MatchData | null>(null)
const events = ref<MatchEvent[]>([])
const loading = ref(true)

const stageLabel = computed(() => {
  if (!match.value) return ''
  const map: Record<string, string> = {
    group: match.value.group_name ? `小组赛 ${match.value.group_name}组` : '小组赛',
    round_32: '32强赛',
    round_16: '16强赛',
    quarter: '1/4决赛',
    semi: '半决赛',
    third_place: '三四名决赛',
    final: '决赛',
  }
  return map[match.value.stage] || match.value.stage
})

const statusConfig = computed(() => {
  if (!match.value) return { label: '', class: '' }
  switch (match.value.status) {
    case 'live':
      return { label: '直播中', class: 'bg-red-100 text-red-600' }
    case 'finished':
      return { label: '已结束', class: 'bg-gray-100 text-gray-400' }
    default:
      return { label: '未开始', class: 'bg-green-100 text-green-600' }
  }
})

const formattedTime = computed(() => {
  if (!match.value) return ''
  const d = new Date(match.value.start_time)
  return `${d.getFullYear()}/${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
})

// 合并内嵌事件和独立请求的事件
const allEvents = computed(() => {
  if (events.value.length > 0) return events.value
  return match.value?.events || []
})

const eventIcon = (type: string) => {
  switch (type) {
    case 'goal':
      return '⚽'
    case 'card':
      return '🟨'
    case 'substitution':
      return '🔄'
    default:
      return '📋'
  }
}

async function loadData() {
  loading.value = true
  try {
    const [matchRes, eventsRes] = await Promise.allSettled([
      getMatch(matchId),
      getMatchEvents(matchId),
    ])
    if (matchRes.status === 'fulfilled') {
      match.value = matchRes.value.data
    } else {
      router.push({ name: 'schedule' })
      return
    }
    if (eventsRes.status === 'fulfilled') {
      events.value = eventsRes.value.data || []
    }
  } finally {
    loading.value = false
  }
}

function onReminderSuccess() {
  toast.success('提醒设置成功')
}

function goTeam(teamId: number) {
  router.push({ name: 'team-detail', params: { id: teamId } })
}

onMounted(loadData)
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="mx-auto max-w-screen-lg">
      <LoadingSpinner v-if="loading" text="加载比赛详情..." />

      <template v-else-if="match">
        <!-- 顶部比赛信息 -->
        <div class="bg-gradient-to-b from-green-600 to-green-700 p-6 text-white">
          <div class="mb-2 text-center">
            <span class="rounded-full bg-white/20 px-3 py-1 text-xs">{{ stageLabel }}</span>
          </div>

          <!-- 双方球队和比分 -->
          <div class="mt-4 flex items-center justify-between">
            <div
              class="flex flex-1 cursor-pointer flex-col items-center"
              @click="goTeam(match.home_team.id)"
            >
              <div class="mb-2 flex h-16 w-16 items-center justify-center rounded-full bg-white/20">
                <span class="text-2xl font-bold">{{ match.home_team.code }}</span>
              </div>
              <span class="text-sm font-medium">{{ match.home_team.name }}</span>
            </div>

            <div class="flex items-center gap-3 px-4">
              <template v-if="match.status === 'upcoming'">
                <span class="text-3xl font-bold opacity-50">VS</span>
              </template>
              <template v-else>
                <span class="text-4xl font-bold">{{ match.home_score }}</span>
                <span class="text-2xl opacity-50">:</span>
                <span class="text-4xl font-bold">{{ match.away_score }}</span>
              </template>
            </div>

            <div
              class="flex flex-1 cursor-pointer flex-col items-center"
              @click="goTeam(match.away_team.id)"
            >
              <div class="mb-2 flex h-16 w-16 items-center justify-center rounded-full bg-white/20">
                <span class="text-2xl font-bold">{{ match.away_team.code }}</span>
              </div>
              <span class="text-sm font-medium">{{ match.away_team.name }}</span>
            </div>
          </div>

          <!-- 时间/场馆/状态 -->
          <div class="mt-4 flex items-center justify-center gap-4 text-xs text-white/70">
            <span>{{ formattedTime }}</span>
            <span v-if="match.venue">{{ match.venue }}</span>
          </div>

          <div class="mt-3 text-center">
            <span
              class="inline-flex items-center rounded-full px-3 py-1 text-xs"
              :class="statusConfig.class"
            >
              {{ statusConfig.label }}
            </span>
          </div>
        </div>

        <!-- 直播比分 -->
        <LiveScore v-if="match.status === 'live'" :match="match" class="px-4 pt-4" />

        <!-- 操作区域 -->
        <div class="space-y-4 px-4 py-4">
          <!-- 设置提醒 -->
          <ReminderSetting
            v-if="match.status === 'upcoming'"
            :match-id="match.id"
            @success="onReminderSuccess"
          />

          <!-- AI 赛果预测 -->
          <AIPrediction :match-id="match.id" />

          <!-- 比赛事件时间线 -->
          <div v-if="allEvents.length > 0" class="rounded-xl bg-white p-4">
            <h3 class="mb-3 text-sm font-bold text-gray-700">比赛事件</h3>
            <div class="space-y-3">
              <div
                v-for="event in allEvents"
                :key="event.id"
                class="flex items-center gap-3 text-sm"
              >
                <span class="w-8 text-center font-mono text-gray-400">{{ event.minute }}'</span>
                <span>{{ eventIcon(event.event_type) }}</span>
                <span class="text-gray-700">{{ event.detail || event.event_type }}</span>
              </div>
            </div>
          </div>

          <!-- 暂无事件 -->
          <div v-else class="rounded-xl bg-white p-6 text-center text-sm text-gray-400">
            暂无比赛事件
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
