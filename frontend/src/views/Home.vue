<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCountdown } from '@/composables/useCountdown'
import { useMatchStore } from '@/stores/matches'
import { useTeamStore } from '@/stores/teams'
import MatchCard from '@/components/match/MatchCard.vue'
import TeamCard from '@/components/team/TeamCard.vue'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'

const router = useRouter()
const matchStore = useMatchStore()
const teamStore = useTeamStore()
const loadError = ref(false)

// World Cup 2026 starts June 11, 2026
const { days, hours, minutes, seconds, expired, start } = useCountdown('2026-06-11T00:00:00Z')

async function loadData() {
  loadError.value = false
  try {
    await Promise.all([
      matchStore.fetchMatches({ date: new Date().toISOString().split('T')[0] }),
      teamStore.fetchTeams(),
    ])
  } catch {
    loadError.value = true
  }
}

onMounted(() => {
  start()
  loadData()
})

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

function onMatchClick(match: MatchObject) {
  router.push({ name: 'schedule', query: { matchId: match.id.toString() } })
}

interface QuickLink {
  label: string
  icon: string
  route: string
  color: string
}

const quickLinks: QuickLink[] = [
  { label: '赛程表', icon: 'calendar', route: '/schedule', color: 'from-blue-500 to-blue-600' },
  { label: '球队圈子', icon: 'users', route: '/community', color: 'from-green-500 to-green-600' },
  { label: '竞猜中心', icon: 'star', route: '/prediction', color: 'from-yellow-500 to-orange-500' },
  { label: 'AI 壁纸', icon: 'image', route: '/wallpaper', color: 'from-purple-500 to-pink-500' },
]
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section with Countdown -->
    <section class="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-500 to-blue-500 text-white px-4 py-8">
      <div class="relative z-10 max-w-screen-lg mx-auto text-center">
        <h1 class="text-2xl font-bold mb-2">2026 世界杯</h1>
        <p class="text-primary-100 text-sm mb-6">FIFA World Cup 2026 -- 美国/加拿大/墨西哥</p>

        <!-- Countdown -->
        <div v-if="!expired" class="flex items-center justify-center gap-3">
          <div class="flex flex-col items-center">
            <span class="text-3xl font-bold tabular-nums bg-white/20 backdrop-blur-sm rounded-lg w-16 h-16 flex items-center justify-center">
              {{ days }}
            </span>
            <span class="text-xs mt-1 text-primary-200">天</span>
          </div>
          <span class="text-2xl font-light text-primary-200 -mt-4">:</span>
          <div class="flex flex-col items-center">
            <span class="text-3xl font-bold tabular-nums bg-white/20 backdrop-blur-sm rounded-lg w-16 h-16 flex items-center justify-center">
              {{ String(hours).padStart(2, '0') }}
            </span>
            <span class="text-xs mt-1 text-primary-200">时</span>
          </div>
          <span class="text-2xl font-light text-primary-200 -mt-4">:</span>
          <div class="flex flex-col items-center">
            <span class="text-3xl font-bold tabular-nums bg-white/20 backdrop-blur-sm rounded-lg w-16 h-16 flex items-center justify-center">
              {{ String(minutes).padStart(2, '0') }}
            </span>
            <span class="text-xs mt-1 text-primary-200">分</span>
          </div>
          <span class="text-2xl font-light text-primary-200 -mt-4">:</span>
          <div class="flex flex-col items-center">
            <span class="text-3xl font-bold tabular-nums bg-white/20 backdrop-blur-sm rounded-lg w-16 h-16 flex items-center justify-center">
              {{ String(seconds).padStart(2, '0') }}
            </span>
            <span class="text-xs mt-1 text-primary-200">秒</span>
          </div>
        </div>
        <div v-else class="text-xl font-bold">
          世界杯已开赛!
        </div>
      </div>

      <!-- Decorative circles -->
      <div class="absolute top-0 right-0 w-40 h-40 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2"></div>
      <div class="absolute bottom-0 left-0 w-32 h-32 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2"></div>
    </section>

    <div class="max-w-screen-lg mx-auto px-4 py-6 space-y-8">
      <!-- Quick links -->
      <section class="grid grid-cols-4 gap-3">
        <router-link
          v-for="link in quickLinks"
          :key="link.route"
          :to="link.route"
          class="flex flex-col items-center gap-2"
        >
          <div
            class="w-12 h-12 rounded-xl bg-gradient-to-br flex items-center justify-center shadow-sm"
            :class="link.color"
          >
            <svg v-if="link.icon === 'calendar'" class="w-6 h-6 text-white" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <rect x="3" y="4" width="18" height="18" rx="2" />
              <path d="M16 2v4M8 2v4M3 10h18" />
            </svg>
            <svg v-else-if="link.icon === 'users'" class="w-6 h-6 text-white" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" />
            </svg>
            <svg v-else-if="link.icon === 'star'" class="w-6 h-6 text-white" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
            </svg>
            <svg v-else-if="link.icon === 'image'" class="w-6 h-6 text-white" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <circle cx="8.5" cy="8.5" r="1.5" />
              <path d="M21 15l-5-5L5 21" />
            </svg>
          </div>
          <span class="text-xs text-gray-600 font-medium">{{ link.label }}</span>
        </router-link>
      </section>

      <!-- Today's matches -->
      <section>
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-bold text-gray-800">今日赛程</h2>
          <router-link to="/schedule" class="text-sm text-primary-500 hover:text-primary-600">
            查看全部 &rarr;
          </router-link>
        </div>

        <!-- 加载失败重试 -->
        <div v-if="loadError" class="text-center py-8">
          <p class="text-sm text-gray-400 mb-3">加载失败</p>
          <button class="px-4 py-2 bg-green-600 text-white text-sm rounded-lg" @click="loadData">重新加载</button>
        </div>

        <SkeletonLoader v-else-if="matchStore.loading" type="card" :count="2" />

        <div
          v-else-if="matchStore.matches.length > 0"
          class="flex gap-3 overflow-x-auto pb-2 -mx-4 px-4 snap-x snap-mandatory scrollbar-hide"
        >
          <div
            v-for="match in matchStore.matches"
            :key="match.id"
            class="snap-start flex-shrink-0"
          >
            <MatchCard :match="match" @click="onMatchClick" />
          </div>
        </div>

        <div v-else class="text-center py-8 text-gray-400 text-sm">
          今日暂无比赛
        </div>
      </section>

      <!-- Popular teams -->
      <section>
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-bold text-gray-800">热门球队</h2>
        </div>

        <SkeletonLoader v-if="teamStore.loading" type="grid" :count="6" />

        <div
          v-else-if="teamStore.teams.length > 0"
          class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3"
        >
          <TeamCard
            v-for="team in teamStore.teams.slice(0, 12)"
            :key="team.id"
            :team="team"
          />
        </div>

        <div v-else class="text-center py-8 text-gray-400 text-sm">
          暂无球队数据
        </div>
      </section>
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
