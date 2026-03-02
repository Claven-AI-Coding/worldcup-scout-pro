<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { useWebSocket } from '@/composables/useWebSocket'

interface Team {
  id: number
  name: string
  code: string
  flag_url: string | null
}

interface Match {
  id: number
  home_team: Team
  away_team: Team
  home_score: number | null
  away_score: number | null
  status: string
}

interface Props {
  match: Match
}

const props = defineProps<Props>()

const { data, connected, connect } = useWebSocket(props.match.id)

onMounted(() => {
  if (props.match.status === 'live') {
    connect()
  }
})

watch(
  () => props.match.status,
  (status) => {
    if (status === 'live' && !connected.value) {
      connect()
    }
  }
)

const liveHomeScore = computed(() => {
  if (data.value && typeof data.value.home_score === 'number') {
    return data.value.home_score
  }
  return props.match.home_score ?? 0
})

const liveAwayScore = computed(() => {
  if (data.value && typeof data.value.away_score === 'number') {
    return data.value.away_score
  }
  return props.match.away_score ?? 0
})

const matchMinute = computed(() => {
  if (data.value && data.value.minute) {
    return data.value.minute
  }
  return null
})

interface MatchEvent {
  type: string
  minute: number
  player: string
  team: string
}

const recentEvents = computed<MatchEvent[]>(() => {
  if (data.value && Array.isArray(data.value.events)) {
    return (data.value.events as MatchEvent[]).slice(-5)
  }
  return []
})

function eventIcon(type: string): string {
  switch (type) {
    case 'goal':
      return '⚽'
    case 'yellow_card':
      return '🟨'
    case 'red_card':
      return '🟥'
    case 'substitution':
      return '🔄'
    default:
      return '📋'
  }
}
</script>

<template>
  <div class="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl p-5 text-white">
    <!-- Connection status -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2">
        <span
          class="w-2 h-2 rounded-full"
          :class="connected ? 'bg-green-400 animate-pulse' : 'bg-gray-500'"
        ></span>
        <span class="text-xs text-gray-400">
          {{ connected ? '实时连接中' : '未连接' }}
        </span>
      </div>
      <span v-if="matchMinute" class="text-xs font-mono text-green-400 animate-pulse">
        {{ matchMinute }}'
      </span>
    </div>

    <!-- Score display -->
    <div class="flex items-center justify-between gap-4">
      <!-- Home team -->
      <div class="flex flex-col items-center flex-1">
        <div class="w-14 h-14 rounded-full bg-white/10 flex items-center justify-center overflow-hidden mb-2">
          <img
            v-if="props.match.home_team.flag_url"
            :src="props.match.home_team.flag_url"
            :alt="props.match.home_team.name"
            class="w-full h-full object-cover"
          />
          <span v-else class="text-lg font-bold text-white/60">{{ props.match.home_team.code }}</span>
        </div>
        <span class="text-sm font-medium text-gray-300">{{ props.match.home_team.name }}</span>
      </div>

      <!-- Animated score -->
      <div class="flex items-center gap-3">
        <span class="text-4xl font-bold tabular-nums transition-all duration-300">
          {{ liveHomeScore }}
        </span>
        <span class="text-2xl text-gray-500 font-light">-</span>
        <span class="text-4xl font-bold tabular-nums transition-all duration-300">
          {{ liveAwayScore }}
        </span>
      </div>

      <!-- Away team -->
      <div class="flex flex-col items-center flex-1">
        <div class="w-14 h-14 rounded-full bg-white/10 flex items-center justify-center overflow-hidden mb-2">
          <img
            v-if="props.match.away_team.flag_url"
            :src="props.match.away_team.flag_url"
            :alt="props.match.away_team.name"
            class="w-full h-full object-cover"
          />
          <span v-else class="text-lg font-bold text-white/60">{{ props.match.away_team.code }}</span>
        </div>
        <span class="text-sm font-medium text-gray-300">{{ props.match.away_team.name }}</span>
      </div>
    </div>

    <!-- Recent events -->
    <div v-if="recentEvents.length > 0" class="mt-4 pt-4 border-t border-white/10">
      <p class="text-xs text-gray-500 mb-2">最近事件</p>
      <div class="space-y-1.5">
        <div
          v-for="(event, index) in recentEvents"
          :key="index"
          class="flex items-center gap-2 text-xs text-gray-400"
        >
          <span>{{ eventIcon(event.type) }}</span>
          <span class="font-mono text-gray-500">{{ event.minute }}'</span>
          <span>{{ event.player }}</span>
          <span class="text-gray-600">{{ event.team }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
