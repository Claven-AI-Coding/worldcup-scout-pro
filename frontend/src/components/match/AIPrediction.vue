<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getMatchPrediction } from '@/api/matches'
import Disclaimer from '@/components/common/Disclaimer.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const props = defineProps<{
  matchId: number
  homeTeamName?: string
  awayTeamName?: string
}>()

interface PredictedScore {
  score: string
  probability: number
}

interface Prediction {
  home_win_pct: number
  draw_pct: number
  away_win_pct: number
  predicted_scores: PredictedScore[]
  analysis: string
  disclaimer: string
}

const prediction = ref<Prediction | null>(null)
const loading = ref(false)
const error = ref('')

async function loadPrediction() {
  loading.value = true
  error.value = ''
  try {
    const res = await getMatchPrediction(props.matchId)
    prediction.value = res.data
  } catch {
    error.value = '暂无预测数据'
  } finally {
    loading.value = false
  }
}

onMounted(loadPrediction)
</script>

<template>
  <div class="rounded-xl bg-white p-4">
    <h3 class="mb-3 flex items-center gap-2 text-sm font-bold text-gray-700">
      <span>🤖</span> AI 赛果预测
    </h3>

    <LoadingSpinner v-if="loading" text="AI 分析中..." />

    <div v-else-if="error" class="py-4 text-center text-sm text-gray-400">
      {{ error }}
    </div>

    <template v-else-if="prediction">
      <!-- 胜率环形图（简化为进度条） -->
      <div class="mb-4 space-y-2">
        <div class="flex items-center gap-2">
          <span class="w-16 text-xs text-gray-500">{{ homeTeamName || '主队' }}</span>
          <div class="h-6 flex-1 overflow-hidden rounded-full bg-gray-100">
            <div
              class="flex h-full items-center justify-center rounded-full bg-green-500 text-xs font-bold text-white"
              :style="{ width: prediction.home_win_pct + '%' }"
            >
              {{ prediction.home_win_pct }}%
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-16 text-xs text-gray-500">平局</span>
          <div class="h-6 flex-1 overflow-hidden rounded-full bg-gray-100">
            <div
              class="flex h-full items-center justify-center rounded-full bg-yellow-400 text-xs font-bold text-white"
              :style="{ width: prediction.draw_pct + '%' }"
            >
              {{ prediction.draw_pct }}%
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-16 text-xs text-gray-500">{{ awayTeamName || '客队' }}</span>
          <div class="h-6 flex-1 overflow-hidden rounded-full bg-gray-100">
            <div
              class="flex h-full items-center justify-center rounded-full bg-red-400 text-xs font-bold text-white"
              :style="{ width: prediction.away_win_pct + '%' }"
            >
              {{ prediction.away_win_pct }}%
            </div>
          </div>
        </div>
      </div>

      <!-- 比分预测 -->
      <div v-if="prediction.predicted_scores.length > 0" class="mb-4">
        <p class="mb-2 text-xs text-gray-400">预测比分</p>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="(s, idx) in prediction.predicted_scores"
            :key="idx"
            class="inline-flex items-center gap-1 rounded-full bg-gray-50 px-3 py-1 text-xs"
          >
            <span class="font-bold text-gray-700">{{ s.score }}</span>
            <span class="text-gray-400">{{ s.probability }}%</span>
          </span>
        </div>
      </div>

      <!-- 分析摘要 -->
      <p v-if="prediction.analysis" class="mb-3 text-xs text-gray-500">
        {{ prediction.analysis }}
      </p>

      <!-- 免责声明 -->
      <Disclaimer :text="prediction.disclaimer" />
    </template>
  </div>
</template>
