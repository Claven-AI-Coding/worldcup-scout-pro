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
  submit: [
    data: {
      match_id: number
      predicted_result: string
      predicted_home_score?: number
      predicted_away_score?: number
      points_wagered: number
    },
  ]
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
  <div class="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
    <!-- Match info header -->
    <div class="mb-4 flex items-center justify-between">
      <span class="text-xs text-gray-400">{{ formattedTime }}</span>
      <span v-if="props.match.venue" class="text-xs text-gray-400">{{ props.match.venue }}</span>
    </div>

    <!-- Teams -->
    <div class="mb-5 flex items-center justify-center gap-4">
      <div class="flex items-center gap-2">
        <div
          class="flex h-8 w-8 items-center justify-center overflow-hidden rounded-full bg-gray-100"
        >
          <img
            v-if="props.match.home_team.flag_url"
            :src="props.match.home_team.flag_url"
            :alt="props.match.home_team.name"
            class="h-full w-full object-cover"
          />
          <span v-else class="text-xs font-bold text-gray-400">{{
            props.match.home_team.code
          }}</span>
        </div>
        <span class="text-sm font-medium text-gray-700">{{ props.match.home_team.name }}</span>
      </div>
      <span class="font-bold text-gray-300">VS</span>
      <div class="flex items-center gap-2">
        <span class="text-sm font-medium text-gray-700">{{ props.match.away_team.name }}</span>
        <div
          class="flex h-8 w-8 items-center justify-center overflow-hidden rounded-full bg-gray-100"
        >
          <img
            v-if="props.match.away_team.flag_url"
            :src="props.match.away_team.flag_url"
            :alt="props.match.away_team.name"
            class="h-full w-full object-cover"
          />
          <span v-else class="text-xs font-bold text-gray-400">{{
            props.match.away_team.code
          }}</span>
        </div>
      </div>
    </div>

    <!-- Outcome buttons -->
    <div class="mb-4 grid grid-cols-3 gap-2">
      <button
        class="rounded-lg border-2 py-2.5 text-sm font-medium transition-all"
        :class="
          selectedResult === 'home_win'
            ? 'border-primary-500 bg-primary-50 text-primary-600'
            : 'border-gray-200 text-gray-500 hover:border-gray-300'
        "
        @click="selectResult('home_win')"
      >
        主胜
      </button>
      <button
        class="rounded-lg border-2 py-2.5 text-sm font-medium transition-all"
        :class="
          selectedResult === 'draw'
            ? 'border-primary-500 bg-primary-50 text-primary-600'
            : 'border-gray-200 text-gray-500 hover:border-gray-300'
        "
        @click="selectResult('draw')"
      >
        平
      </button>
      <button
        class="rounded-lg border-2 py-2.5 text-sm font-medium transition-all"
        :class="
          selectedResult === 'away_win'
            ? 'border-primary-500 bg-primary-50 text-primary-600'
            : 'border-gray-200 text-gray-500 hover:border-gray-300'
        "
        @click="selectResult('away_win')"
      >
        客胜
      </button>
    </div>

    <!-- Optional score prediction -->
    <div class="mb-4 flex items-center justify-center gap-3">
      <span class="text-xs text-gray-400">比分预测 (可选)</span>
      <div class="flex items-center gap-2">
        <input
          v-model.number="homeScore"
          type="number"
          min="0"
          max="20"
          class="h-9 w-12 rounded-lg border border-gray-200 text-center text-sm focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary-500"
          placeholder="-"
        />
        <span class="text-gray-300">:</span>
        <input
          v-model.number="awayScore"
          type="number"
          min="0"
          max="20"
          class="h-9 w-12 rounded-lg border border-gray-200 text-center text-sm focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary-500"
          placeholder="-"
        />
      </div>
    </div>

    <!-- Points wager slider -->
    <div class="mb-5">
      <div class="mb-2 flex items-center justify-between">
        <span class="text-xs text-gray-500">下注积分</span>
        <span class="text-sm font-bold text-primary-600">{{ pointsWagered }} 分</span>
      </div>
      <input
        v-model.number="pointsWagered"
        type="range"
        min="10"
        max="100"
        step="10"
        class="h-2 w-full cursor-pointer appearance-none rounded-lg bg-gray-200 accent-primary-500"
      />
      <div class="mt-1 flex justify-between text-xs text-gray-400">
        <span>10</span>
        <span>100</span>
      </div>
    </div>

    <!-- Submit -->
    <button
      class="w-full rounded-lg bg-primary-500 py-2.5 text-sm font-medium text-white transition-colors hover:bg-primary-600 disabled:cursor-not-allowed disabled:opacity-50"
      :disabled="!canSubmit"
      @click="handleSubmit"
    >
      {{ submitting ? '提交中...' : '确认竞猜' }}
    </button>
  </div>
</template>
