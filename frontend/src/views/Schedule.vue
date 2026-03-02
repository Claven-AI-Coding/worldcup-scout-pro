<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useMatchStore } from '@/stores/matches'
import { getStandings } from '@/api/matches'
import MatchCard from '@/components/match/MatchCard.vue'
import StandingsTable from '@/components/match/StandingsTable.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const matchStore = useMatchStore()

// Stage filter
interface StageTab {
  value: string
  label: string
}

const stages: StageTab[] = [
  { value: '', label: '全部' },
  { value: 'group', label: '小组赛' },
  { value: 'round_16', label: '16强' },
  { value: 'quarter', label: '8强' },
  { value: 'semi', label: '半决赛' },
  { value: 'final', label: '决赛' },
]

const activeStage = ref('')
const showStandings = ref(false)

// Date navigation
const currentDate = ref(new Date().toISOString().split('T')[0])

function prevDate() {
  const d = new Date(currentDate.value)
  d.setDate(d.getDate() - 1)
  currentDate.value = d.toISOString().split('T')[0]
}

function nextDate() {
  const d = new Date(currentDate.value)
  d.setDate(d.getDate() + 1)
  currentDate.value = d.toISOString().split('T')[0]
}

const formattedDate = computed(() => {
  const d = new Date(currentDate.value)
  const month = d.getMonth() + 1
  const day = d.getDate()
  const weekdays = ['日', '一', '二', '三', '四', '五', '六']
  const weekday = weekdays[d.getDay()]
  return `${month}月${day}日 周${weekday}`
})

// Matches grouped by date
interface MatchObject {
  id: number
  stage: string
  group_name: string | null
  home_team: { id: number; name: string; code: string; flag_url: string | null }
  away_team: { id: number; name: string; code: string; flag_url: string | null }
  home_score: number | null
  away_score: number | null
  status: string
  start_time: string
  venue: string | null
}

const groupedMatches = computed(() => {
  const groups: Record<string, MatchObject[]> = {}
  for (const match of matchStore.matches) {
    const dateKey = match.start_time.split('T')[0]
    if (!groups[dateKey]) groups[dateKey] = []
    groups[dateKey].push(match)
  }
  return groups
})

// Standings
interface StandingEntry {
  position: number
  team_id: number
  team_name: string
  team_code: string
  played: number
  won: number
  drawn: number
  lost: number
  goals_for: number
  goals_against: number
  goal_difference: number
  points: number
  group_name: string
}

const standings = ref<Record<string, StandingEntry[]>>({})
const standingsLoading = ref(false)

async function fetchStandings() {
  standingsLoading.value = true
  try {
    const res = await getStandings()
    const data = res.data as StandingEntry[] | Record<string, StandingEntry[]>
    if (Array.isArray(data)) {
      // Group by group_name
      const grouped: Record<string, StandingEntry[]> = {}
      for (const entry of data) {
        const g = entry.group_name || 'Unknown'
        if (!grouped[g]) grouped[g] = []
        grouped[g].push(entry)
      }
      standings.value = grouped
    } else {
      standings.value = data
    }
  } catch {
    standings.value = {}
  } finally {
    standingsLoading.value = false
  }
}

function loadMatches() {
  matchStore.fetchMatches({
    stage: activeStage.value || undefined,
    date: currentDate.value,
  })
}

watch([activeStage, currentDate], () => {
  loadMatches()
})

onMounted(() => {
  loadMatches()
})

function toggleStandings() {
  showStandings.value = !showStandings.value
  if (showStandings.value && Object.keys(standings.value).length === 0) {
    fetchStandings()
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-screen-lg mx-auto">
      <!-- Stage filter tabs -->
      <div class="bg-white border-b border-gray-100 sticky top-14 z-40">
        <div class="flex overflow-x-auto px-4 py-2 gap-1 scrollbar-hide">
          <button
            v-for="stage in stages"
            :key="stage.value"
            class="flex-shrink-0 px-4 py-1.5 text-sm font-medium rounded-full transition-colors"
            :class="activeStage === stage.value
              ? 'bg-primary-500 text-white'
              : 'text-gray-500 hover:bg-gray-100'"
            @click="activeStage = stage.value"
          >
            {{ stage.label }}
          </button>
        </div>
      </div>

      <div class="px-4 py-4">
        <!-- Date navigation -->
        <div class="flex items-center justify-between mb-4">
          <button
            class="w-8 h-8 rounded-full bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition-colors"
            @click="prevDate"
          >
            <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <span class="text-sm font-medium text-gray-700">{{ formattedDate }}</span>
          <button
            class="w-8 h-8 rounded-full bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition-colors"
            @click="nextDate"
          >
            <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        <!-- Standings toggle -->
        <div class="flex justify-end mb-4">
          <button
            class="text-sm flex items-center gap-1 px-3 py-1.5 rounded-lg transition-colors"
            :class="showStandings ? 'bg-primary-50 text-primary-600' : 'text-gray-500 hover:bg-gray-100'"
            @click="toggleStandings"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" d="M3 10h18M3 14h18M3 18h18M3 6h18" />
            </svg>
            积分榜
          </button>
        </div>

        <!-- Standings -->
        <div v-if="showStandings" class="space-y-4 mb-6">
          <LoadingSpinner v-if="standingsLoading" text="加载积分榜..." />
          <template v-else>
            <StandingsTable
              v-for="(entries, groupName) in standings"
              :key="groupName"
              :standings="entries"
              :group-name="String(groupName)"
            />
          </template>
          <EmptyState
            v-if="!standingsLoading && Object.keys(standings).length === 0"
            message="暂无积分数据"
          />
        </div>

        <!-- Match list -->
        <div v-if="!showStandings">
          <LoadingSpinner v-if="matchStore.loading" text="加载赛程..." />

          <template v-else-if="Object.keys(groupedMatches).length > 0">
            <div
              v-for="(matches, dateKey) in groupedMatches"
              :key="dateKey"
              class="mb-6"
            >
              <h3 class="text-xs text-gray-400 font-medium mb-2 uppercase">{{ dateKey }}</h3>
              <div class="space-y-3">
                <MatchCard
                  v-for="match in matches"
                  :key="match.id"
                  :match="match"
                />
              </div>
            </div>
          </template>

          <EmptyState v-else message="该日期暂无比赛" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
