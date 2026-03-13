<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useMatchStore } from '@/stores/matches'
import { getStandings } from '@/api/matches'
import MatchCard from '@/components/match/MatchCard.vue'
import StandingsTable from '@/components/match/StandingsTable.vue'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const matchStore = useMatchStore()

// 赛事阶段筛选（新增 round_32 和 third_place）
interface StageTab {
  value: string
  label: string
}

const stages: StageTab[] = [
  { value: '', label: '全部' },
  { value: 'group', label: '小组赛' },
  { value: 'round_32', label: '32强' },
  { value: 'round_16', label: '16强' },
  { value: 'quarter', label: '1/4决赛' },
  { value: 'semi', label: '半决赛' },
  { value: 'final', label: '决赛' },
]

const activeStage = ref('')
const activeGroup = ref('')  // 小组筛选 A-L
const showStandings = ref(false)

// 12 组
const groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

// 日期导航：今日/明日/全部
type DateMode = 'today' | 'tomorrow' | 'all' | 'custom'
const dateMode = ref<DateMode>('today')
const customDate = ref(new Date().toISOString().split('T')[0])

const currentDate = computed(() => {
  const today = new Date()
  if (dateMode.value === 'today') return today.toISOString().split('T')[0]
  if (dateMode.value === 'tomorrow') {
    const tm = new Date(today)
    tm.setDate(tm.getDate() + 1)
    return tm.toISOString().split('T')[0]
  }
  if (dateMode.value === 'custom') return customDate.value
  return undefined // 'all' 不按日期筛选
})

const formattedDate = computed(() => {
  if (!currentDate.value) return '全部日期'
  const d = new Date(currentDate.value)
  const month = d.getMonth() + 1
  const day = d.getDate()
  const weekdays = ['日', '一', '二', '三', '四', '五', '六']
  const weekday = weekdays[d.getDay()]
  return `${month}月${day}日 周${weekday}`
})

// 按日期分组比赛列表
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
  const grouped: Record<string, MatchObject[]> = {}
  for (const match of matchStore.matches) {
    const dateKey = match.start_time.split('T')[0]
    if (!grouped[dateKey]) grouped[dateKey] = []
    grouped[dateKey].push(match)
  }
  return grouped
})

// 积分榜
interface StandingEntry {
  position: number
  team_id: number
  team_name: string
  team_code: string
  flag_url: string | null
  played: number
  won: number
  drawn: number
  lost: number
  goals_for: number
  goals_against: number
  goal_difference: number
  points: number
}

const standings = ref<Record<string, StandingEntry[]>>({})
const standingsLoading = ref(false)
const activeStandingsGroup = ref('A')

async function fetchStandings() {
  standingsLoading.value = true
  try {
    const res = await getStandings()
    standings.value = res.data as Record<string, StandingEntry[]>
  } catch {
    standings.value = {}
  } finally {
    standingsLoading.value = false
  }
}

function loadMatches() {
  matchStore.fetchMatches({
    stage: activeStage.value || undefined,
    group: activeGroup.value || undefined,
    date: currentDate.value,
    limit: 50,
  })
}

watch([activeStage, activeGroup, dateMode, customDate], () => {
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
      <!-- 阶段筛选 -->
      <div class="bg-white border-b border-gray-100 sticky top-14 z-40">
        <div class="flex overflow-x-auto px-4 py-2 gap-1 scrollbar-hide">
          <button
            v-for="stage in stages"
            :key="stage.value"
            class="flex-shrink-0 px-4 py-1.5 text-sm font-medium rounded-full transition-colors"
            :class="activeStage === stage.value
              ? 'bg-green-600 text-white'
              : 'text-gray-500 hover:bg-gray-100'"
            @click="activeStage = stage.value"
          >
            {{ stage.label }}
          </button>
        </div>

        <!-- 小组赛时显示小组筛选 -->
        <div v-if="activeStage === 'group'" class="flex overflow-x-auto px-4 pb-2 gap-1 scrollbar-hide">
          <button
            class="flex-shrink-0 px-3 py-1 text-xs font-medium rounded-full transition-colors"
            :class="activeGroup === '' ? 'bg-green-100 text-green-700' : 'text-gray-400 hover:bg-gray-50'"
            @click="activeGroup = ''"
          >
            全部
          </button>
          <button
            v-for="g in groups"
            :key="g"
            class="flex-shrink-0 px-3 py-1 text-xs font-medium rounded-full transition-colors"
            :class="activeGroup === g ? 'bg-green-100 text-green-700' : 'text-gray-400 hover:bg-gray-50'"
            @click="activeGroup = g"
          >
            {{ g }}组
          </button>
        </div>
      </div>

      <div class="px-4 py-4">
        <!-- 日期切换：今日 / 明日 / 全部 -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex gap-2">
            <button
              v-for="mode in [
                { value: 'today' as DateMode, label: '今日' },
                { value: 'tomorrow' as DateMode, label: '明日' },
                { value: 'all' as DateMode, label: '全部' },
              ]"
              :key="mode.value"
              class="px-3 py-1 text-sm rounded-lg transition-colors"
              :class="dateMode === mode.value ? 'bg-green-600 text-white' : 'bg-white text-gray-600 border border-gray-200'"
              @click="dateMode = mode.value"
            >
              {{ mode.label }}
            </button>
          </div>
          <span class="text-sm text-gray-500">{{ formattedDate }}</span>
        </div>

        <!-- 积分榜切换 -->
        <div class="flex justify-end mb-4">
          <button
            class="text-sm flex items-center gap-1 px-3 py-1.5 rounded-lg transition-colors"
            :class="showStandings ? 'bg-green-50 text-green-600' : 'text-gray-500 hover:bg-gray-100'"
            @click="toggleStandings"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" d="M3 10h18M3 14h18M3 18h18M3 6h18" />
            </svg>
            积分榜
          </button>
        </div>

        <!-- 积分榜展示（12 组 Tab 切换） -->
        <div v-if="showStandings" class="mb-6">
          <SkeletonLoader v-if="standingsLoading" type="list" :count="4" />
          <template v-else-if="Object.keys(standings).length > 0">
            <!-- 小组 Tab -->
            <div class="flex overflow-x-auto gap-1 mb-3 scrollbar-hide">
              <button
                v-for="g in groups"
                :key="g"
                class="flex-shrink-0 px-3 py-1 text-xs font-medium rounded-full transition-colors"
                :class="activeStandingsGroup === g ? 'bg-green-600 text-white' : 'text-gray-400 bg-gray-100'"
                @click="activeStandingsGroup = g"
              >
                {{ g }}组
              </button>
            </div>
            <StandingsTable
              v-if="standings[activeStandingsGroup]"
              :standings="standings[activeStandingsGroup]"
              :group-name="activeStandingsGroup"
            />
            <EmptyState v-else message="该组暂无数据" />
          </template>
          <EmptyState v-else message="暂无积分数据" />
        </div>

        <!-- 比赛列表 -->
        <div v-if="!showStandings">
          <SkeletonLoader v-if="matchStore.loading" type="card" :count="3" />

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

          <EmptyState v-else message="暂无比赛" />
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
