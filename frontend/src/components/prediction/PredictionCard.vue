<script setup lang="ts">
import { ref, computed } from 'vue'

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
  start_time: string
  venue: string | null
}

interface Props {
  match: Match
}

const props = defineProps<Props>()

const emit = defineEmits<{
  submit: [data: {
    match_id: number
    predicted_result: string
    predicted_home_score?: number
    predicted_away_score?: number
    points_wagered: number
  }]
}>()

const selectedResult = ref<string>('')
const homeScore = ref<number | undefined>(undefined)
const awayScore = ref<number | undefined>(undefined)
const pointsWagered = ref(10)
const submitting = ref(false)

const formattedTime = computed(() => {
  const d = new Date(props.match.start_time)
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const mins = String(d.getMinutes()).padStart(2, '0')
  return `${month}/${day} ${hours}:${mins}`
})

const canSubmit = computed(() => {
  return selectedResult.value !== '' && pointsWagered.value > 0 && !submitting.value
})

function selectResult(result: string) {
  selectedResult.value = result
}

function handleSubmit() {
  if (!canSubmit.value) return
  submitting.value = true

  const data: {
    match_id: number
    predicted_result: string
    predicted_home_score?: number
    predicted_away_score?: number
    points_wagered: number
  } = {
    match_id: props.match.id,
    predicted_result: selectedResult.value,
    points_wagered: pointsWagered.value,
  }

  if (homeScore.value !== undefined) data.predicted_home_score = homeScore.value
  if (awayScore.value !== undefined) data.predicted_away_score = awayScore.value

  emit('submit', data)
  submitting.value = false
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
    <!-- Match info header -->
    <div class="flex items-center justify-between mb-4">
      <span class="text-xs text-gray-400">{{ formattedTime }}</span>
      <span
        v-if="props.match.venue"
        class="text-xs text-gray-400"
      >{{ props.match.venue }}</span>
    </div>

    <!-- Teams -->
    <div class="flex items-center justify-center gap-4 mb-5">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden">
          <img
            v-if="props.match.home_team.flag_url"
            :src="props.match.home_team.flag_url"
            :alt="props.match.home_team.name"
            class="w-full h-full object-cover"
          >
          <span
            v-else
            class="text-xs font-bold text-gray-400"
          >{{ props.match.home_team.code }}</span>
        </div>
        <span class="text-sm font-medium text-gray-700">{{ props.match.home_team.name }}</span>
      </div>
      <span class="text-gray-300 font-bold">VS</span>
      <div class="flex items-center gap-2">
        <span class="text-sm font-medium text-gray-700">{{ props.match.away_team.name }}</span>
        <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden">
          <img
            v-if="props.match.away_team.flag_url"
            :src="props.match.away_team.flag_url"
            :alt="props.match.away_team.name"
            class="w-full h-full object-cover"
          >
          <span
            v-else
            class="text-xs font-bold text-gray-400"
          >{{ props.match.away_team.code }}</span>
        </div>
      </div>
    </div>

    <!-- Outcome buttons -->
    <div class="grid grid-cols-3 gap-2 mb-4">
      <button
        class="py-2.5 rounded-lg text-sm font-medium border-2 transition-all"
        :class="selectedResult === 'home_win'
          ? 'border-primary-500 bg-primary-50 text-primary-600'
          : 'border-gray-200 text-gray-500 hover:border-gray-300'"
        @click="selectResult('home_win')"
      >
        主胜
      </button>
      <button
        class="py-2.5 rounded-lg text-sm font-medium border-2 transition-all"
        :class="selectedResult === 'draw'
          ? 'border-primary-500 bg-primary-50 text-primary-600'
          : 'border-gray-200 text-gray-500 hover:border-gray-300'"
        @click="selectResult('draw')"
      >
        平
      </button>
      <button
        class="py-2.5 rounded-lg text-sm font-medium border-2 transition-all"
        :class="selectedResult === 'away_win'
          ? 'border-primary-500 bg-primary-50 text-primary-600'
          : 'border-gray-200 text-gray-500 hover:border-gray-300'"
        @click="selectResult('away_win')"
      >
        客胜
      </button>
    </div>

    <!-- Optional score prediction -->
    <div class="flex items-center justify-center gap-3 mb-4">
      <span class="text-xs text-gray-400">比分预测 (可选)</span>
      <div class="flex items-center gap-2">
        <input
          v-model.number="homeScore"
          type="number"
          min="0"
          max="20"
          class="w-12 h-9 text-center text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          placeholder="-"
        >
        <span class="text-gray-300">:</span>
        <input
          v-model.number="awayScore"
          type="number"
          min="0"
          max="20"
          class="w-12 h-9 text-center text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          placeholder="-"
        >
      </div>
    </div>

    <!-- Points wager slider -->
    <div class="mb-5">
      <div class="flex items-center justify-between mb-2">
        <span class="text-xs text-gray-500">下注积分</span>
        <span class="text-sm font-bold text-primary-600">{{ pointsWagered }} 分</span>
      </div>
      <input
        v-model.number="pointsWagered"
        type="range"
        min="10"
        max="100"
        step="10"
        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-500"
      >
      <div class="flex justify-between text-xs text-gray-400 mt-1">
        <span>10</span>
        <span>100</span>
      </div>
    </div>

    <!-- Submit -->
    <button
      class="w-full py-2.5 bg-primary-500 text-white text-sm font-medium rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary-600 transition-colors"
      :disabled="!canSubmit"
      @click="handleSubmit"
    >
      {{ submitting ? '提交中...' : '确认竞猜' }}
    </button>
  </div>
</template>
