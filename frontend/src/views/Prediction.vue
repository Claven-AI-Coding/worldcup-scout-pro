<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useMatchStore } from '@/stores/matches'
import { submitPrediction, getMyPredictions, getLeaderboard } from '@/api/predictions'
import PredictionCard from '@/components/prediction/PredictionCard.vue'
import LeaderboardItem from '@/components/prediction/LeaderboardItem.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const matchStore = useMatchStore()

// Tabs
type TabName = 'upcoming' | 'my' | 'leaderboard'
const activeTab = ref<TabName>('upcoming')

interface Tab {
  value: TabName
  label: string
}

const tabs: Tab[] = [
  { value: 'upcoming', label: '竞猜赛事' },
  { value: 'my', label: '我的竞猜' },
  { value: 'leaderboard', label: '排行榜' },
]

// Upcoming matches for prediction
const upcomingMatches = computed(() => {
  return matchStore.matches.filter(m => m.status === 'upcoming')
})

// My predictions
interface PredictionRecord {
  id: number
  match_id: number
  predicted_result: string
  predicted_home_score: number | null
  predicted_away_score: number | null
  points_wagered: number
  result: string | null
  points_earned: number | null
  created_at: string
  match?: {
    home_team: { name: string }
    away_team: { name: string }
    home_score: number | null
    away_score: number | null
    status: string
  }
}

const myPredictions = ref<PredictionRecord[]>([])
const myPredictionsLoading = ref(false)

async function fetchMyPredictions() {
  myPredictionsLoading.value = true
  try {
    const res = await getMyPredictions()
    myPredictions.value = (res.data.items || res.data) as PredictionRecord[]
  } catch {
    myPredictions.value = []
  } finally {
    myPredictionsLoading.value = false
  }
}

// Leaderboard
interface LeaderboardEntry {
  user_id: number
  nickname: string
  avatar: string | null
  total_points: number
  win_streak: number
}

const leaderboard = ref<LeaderboardEntry[]>([])
const leaderboardLoading = ref(false)
const leaderboardType = ref<'daily' | 'all'>('all')

async function fetchLeaderboard() {
  leaderboardLoading.value = true
  try {
    const res = await getLeaderboard(leaderboardType.value)
    leaderboard.value = (res.data.items || res.data) as LeaderboardEntry[]
  } catch {
    leaderboard.value = []
  } finally {
    leaderboardLoading.value = false
  }
}

function handleTabChange(tabValue: TabName) {
  activeTab.value = tabValue
  if (tabValue === 'my') {
    fetchMyPredictions()
  } else if (tabValue === 'leaderboard') {
    fetchLeaderboard()
  }
}

function toggleLeaderboardType(type: 'daily' | 'all') {
  leaderboardType.value = type
  fetchLeaderboard()
}

// Submit prediction
async function handlePredictionSubmit(data: {
  match_id: number
  predicted_result: string
  predicted_home_score?: number
  predicted_away_score?: number
  points_wagered: number
}) {
  try {
    await submitPrediction(data)
    // Refresh after submission
    fetchMyPredictions()
  } catch {
    // ignore
  }
}

function resultLabel(result: string): string {
  const map: Record<string, string> = {
    home_win: '主胜',
    draw: '平',
    away_win: '客胜',
  }
  return map[result] || result
}

function resultBadgeClass(result: string | null): string {
  if (!result) return 'bg-gray-100 text-gray-500'
  if (result === 'win') return 'bg-green-100 text-green-600'
  if (result === 'lose') return 'bg-red-100 text-red-600'
  return 'bg-gray-100 text-gray-500'
}

onMounted(() => {
  matchStore.fetchMatches({ status: 'upcoming' })
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="mx-auto max-w-screen-lg">
      <!-- Tabs -->
      <div class="sticky top-14 z-40 border-b border-gray-100 bg-white">
        <div class="flex">
          <button
            v-for="tab in tabs"
            :key="tab.value"
            class="flex-1 border-b-2 py-3 text-center text-sm font-medium transition-colors"
            :class="
              activeTab === tab.value
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            "
            @click="handleTabChange(tab.value)"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>

      <div class="px-4 py-4">
        <!-- Upcoming matches for prediction -->
        <div v-if="activeTab === 'upcoming'">
          <LoadingSpinner v-if="matchStore.loading" text="加载赛事..." />

          <div v-else-if="upcomingMatches.length > 0" class="space-y-4">
            <PredictionCard
              v-for="match in upcomingMatches"
              :key="match.id"
              :match="match"
              @submit="handlePredictionSubmit"
            />
          </div>

          <EmptyState v-else message="暂无可竞猜的比赛" />
        </div>

        <!-- My predictions -->
        <div v-if="activeTab === 'my'">
          <LoadingSpinner v-if="myPredictionsLoading" text="加载我的竞猜..." />

          <div v-else-if="myPredictions.length > 0" class="space-y-3">
            <div
              v-for="pred in myPredictions"
              :key="pred.id"
              class="rounded-xl border border-gray-100 bg-white p-4 shadow-sm"
            >
              <!-- Match info -->
              <div v-if="pred.match" class="mb-3 flex items-center justify-between">
                <span class="text-sm font-medium text-gray-700">
                  {{ pred.match.home_team.name }} vs {{ pred.match.away_team.name }}
                </span>
                <span
                  class="rounded-full px-2 py-0.5 text-xs font-medium"
                  :class="resultBadgeClass(pred.result)"
                >
                  {{ pred.result === 'win' ? '猜中' : pred.result === 'lose' ? '未中' : '待开奖' }}
                </span>
              </div>

              <!-- Prediction details -->
              <div class="flex items-center justify-between text-sm">
                <div class="flex items-center gap-3">
                  <span class="text-gray-500">预测:</span>
                  <span class="font-medium text-gray-700">{{
                    resultLabel(pred.predicted_result)
                  }}</span>
                  <span v-if="pred.predicted_home_score !== null" class="text-gray-400">
                    {{ pred.predicted_home_score }} : {{ pred.predicted_away_score }}
                  </span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-xs text-gray-400">下注</span>
                  <span class="font-bold text-gray-700">{{ pred.points_wagered }}分</span>
                  <template v-if="pred.points_earned !== null">
                    <span class="text-xs text-gray-400">|</span>
                    <span
                      class="font-bold"
                      :class="(pred.points_earned ?? 0) > 0 ? 'text-green-600' : 'text-red-500'"
                    >
                      {{ (pred.points_earned ?? 0) > 0 ? '+' : '' }}{{ pred.points_earned }}
                    </span>
                  </template>
                </div>
              </div>
            </div>
          </div>

          <EmptyState
            v-else
            message="暂无竞猜记录"
            action-text="去竞猜"
            @action="activeTab = 'upcoming'"
          />
        </div>

        <!-- Leaderboard -->
        <div v-if="activeTab === 'leaderboard'">
          <!-- Type toggle -->
          <div class="mb-4 flex gap-2">
            <button
              class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
              :class="
                leaderboardType === 'all'
                  ? 'bg-primary-500 text-white'
                  : 'border border-gray-200 bg-white text-gray-500 hover:bg-gray-50'
              "
              @click="toggleLeaderboardType('all')"
            >
              总榜
            </button>
            <button
              class="rounded-full px-4 py-1.5 text-sm font-medium transition-colors"
              :class="
                leaderboardType === 'daily'
                  ? 'bg-primary-500 text-white'
                  : 'border border-gray-200 bg-white text-gray-500 hover:bg-gray-50'
              "
              @click="toggleLeaderboardType('daily')"
            >
              今日
            </button>
          </div>

          <LoadingSpinner v-if="leaderboardLoading" text="加载排行榜..." />

          <div
            v-else-if="leaderboard.length > 0"
            class="divide-y divide-gray-50 overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm"
          >
            <LeaderboardItem
              v-for="(entry, index) in leaderboard"
              :key="entry.user_id"
              :entry="entry"
              :rank="index + 1"
            />
          </div>

          <EmptyState v-else message="暂无排行数据" />
        </div>
      </div>
    </div>
  </div>
</template>
