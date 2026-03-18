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
    <section
      class="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-500 to-blue-500 px-4 py-8 text-white"
    >
      <div class="relative z-10 mx-auto max-w-screen-lg text-center">
        <h1 class="mb-2 text-2xl font-bold">2026 世界杯</h1>
        <p class="mb-6 text-sm text-primary-100">FIFA World Cup 2026 -- 美国/加拿大/墨西哥</p>

        <!-- Countdown -->
        <div v-if="!expired" class="flex items-center justify-center gap-3">
          <div class="flex flex-col items-center">
            <span
              class="flex h-16 w-16 items-center justify-center rounded-lg bg-white/20 text-3xl font-bold tabular-nums backdrop-blur-sm"
            >
              {{ days }}
            </span>
            <span class="mt-1 text-xs text-primary-200">天</span>
          </div>
          <span class="-mt-4 text-2xl font-light text-primary-200">:</span>
          <div class="flex flex-col items-center">
            <span
              class="flex h-16 w-16 items-center justify-center rounded-lg bg-white/20 text-3xl font-bold tabular-nums backdrop-blur-sm"
            >
              {{ String(hours).padStart(2, '0') }}
            </span>
            <span class="mt-1 text-xs text-primary-200">时</span>
          </div>
          <span class="-mt-4 text-2xl font-light text-primary-200">:</span>
          <div class="flex flex-col items-center">
            <span
              class="flex h-16 w-16 items-center justify-center rounded-lg bg-white/20 text-3xl font-bold tabular-nums backdrop-blur-sm"
            >
              {{ String(minutes).padStart(2, '0') }}
            </span>
            <span class="mt-1 text-xs text-primary-200">分</span>
          </div>
          <span class="-mt-4 text-2xl font-light text-primary-200">:</span>
          <div class="flex flex-col items-center">
            <span
              class="flex h-16 w-16 items-center justify-center rounded-lg bg-white/20 text-3xl font-bold tabular-nums backdrop-blur-sm"
            >
              {{ String(seconds).padStart(2, '0') }}
            </span>
            <span class="mt-1 text-xs text-primary-200">秒</span>
          </div>
        </div>
        <div v-else class="text-xl font-bold">世界杯已开赛!</div>
      </div>

      <!-- Decorative circles -->
      <div
        class="absolute right-0 top-0 h-40 w-40 -translate-y-1/2 translate-x-1/2 rounded-full bg-white/5"
      />
      <div
        class="absolute bottom-0 left-0 h-32 w-32 -translate-x-1/2 translate-y-1/2 rounded-full bg-white/5"
      />
    </section>

    <div class="mx-auto max-w-screen-lg space-y-8 px-4 py-6">
      <!-- Quick links -->
      <section class="grid grid-cols-4 gap-3">
        <router-link
          v-for="link in quickLinks"
          :key="link.route"
          :to="link.route"
          class="flex flex-col items-center gap-2"
        >
          <div
            class="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br shadow-sm"
            :class="link.color"
          >
            <svg
              v-if="link.icon === 'calendar'"
              class="h-6 w-6 text-white"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              viewBox="0 0 24 24"
            >
              <rect x="3" y="4" width="18" height="18" rx="2" />
              <path d="M16 2v4M8 2v4M3 10h18" />
            </svg>
            <svg
              v-else-if="link.icon === 'users'"
              class="h-6 w-6 text-white"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              viewBox="0 0 24 24"
            >
              <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" />
              <circle cx="9" cy="7" r="4" />
              <path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" />
            </svg>
            <svg
              v-else-if="link.icon === 'star'"
              class="h-6 w-6 text-white"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              viewBox="0 0 24 24"
            >
              <path
                d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
              />
            </svg>
            <svg
              v-else-if="link.icon === 'image'"
              class="h-6 w-6 text-white"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              viewBox="0 0 24 24"
            >
              <rect x="3" y="3" width="18" height="18" rx="2" />
              <circle cx="8.5" cy="8.5" r="1.5" />
              <path d="M21 15l-5-5L5 21" />
            </svg>
          </div>
          <span class="text-xs font-medium text-gray-600">{{ link.label }}</span>
        </router-link>
      </section>

      <!-- Today's matches -->
      <section>
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-bold text-gray-800">今日赛程</h2>
          <router-link to="/schedule" class="text-sm text-primary-500 hover:text-primary-600">
            查看全部 &rarr;
          </router-link>
        </div>

        <!-- 加载失败重试 -->
        <div v-if="loadError" class="py-8 text-center">
          <p class="mb-3 text-sm text-gray-400">加载失败</p>
          <button class="rounded-lg bg-green-600 px-4 py-2 text-sm text-white" @click="loadData">
            重新加载
          </button>
        </div>

        <SkeletonLoader v-else-if="matchStore.loading" type="card" :count="2" />

        <div
          v-else-if="matchStore.matches.length > 0"
          class="scrollbar-hide -mx-4 flex snap-x snap-mandatory gap-3 overflow-x-auto px-4 pb-2"
        >
          <div v-for="match in matchStore.matches" :key="match.id" class="flex-shrink-0 snap-start">
            <MatchCard :match="match" @click="onMatchClick" />
          </div>
        </div>

        <div v-else class="py-8 text-center text-sm text-gray-400">今日暂无比赛</div>
      </section>

      <!-- Popular teams -->
      <section>
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-bold text-gray-800">热门球队</h2>
        </div>

        <SkeletonLoader v-if="teamStore.loading" type="grid" :count="6" />

        <div
          v-else-if="teamStore.teams.length > 0"
          class="grid grid-cols-3 gap-3 sm:grid-cols-4 md:grid-cols-6"
        >
          <TeamCard v-for="team in teamStore.teams.slice(0, 12)" :key="team.id" :team="team" />
        </div>

        <div v-else class="py-8 text-center text-sm text-gray-400">暂无球队数据</div>
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
