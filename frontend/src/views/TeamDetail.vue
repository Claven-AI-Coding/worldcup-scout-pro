<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTeamStore } from '@/stores/teams'
import { useMatchStore } from '@/stores/matches'
import { subscribeTeamMatches } from '@/api/matches'
import PlayerCard from '@/components/team/PlayerCard.vue'
import MatchCard from '@/components/match/MatchCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const route = useRoute()
const router = useRouter()
const teamStore = useTeamStore()
const matchStore = useMatchStore()

const teamId = computed(() => Number(route.params.id))
const subscribing = ref(false)
const subscribeMsg = ref('')

onMounted(() => {
  teamStore.fetchTeam(teamId.value)
  teamStore.fetchTeamPlayers(teamId.value)
  matchStore.fetchMatches()
})

const team = computed(() => teamStore.currentTeam)

const teamMatches = computed(() => {
  return matchStore.matches.filter(
    m => m.home_team?.id === teamId.value || m.away_team?.id === teamId.value
  )
})

const stats = computed(() => {
  if (!team.value?.stats) return null
  return team.value.stats as Record<string, unknown>
})

// 中文标签映射
const statsLabelMap: Record<string, string> = {
  fifa_ranking: 'FIFA 排名',
  confederation: '所属联盟',
  appearances: '世界杯参赛次数',
  best_result: '最佳成绩',
  attack: '进攻',
  defense: '防守',
  possession: '控球率',
  shooting: '射门',
  goal_efficiency: '进球效率',
}

function getStatsLabel(key: string): string {
  return statsLabelMap[key] || key
}

// 战力属性（数值型，可展示进度条）
const powerStats = computed(() => {
  if (!stats.value) return []
  const numericKeys = ['attack', 'defense', 'possession', 'shooting', 'goal_efficiency']
  return numericKeys
    .filter(k => typeof stats.value![k] === 'number')
    .map(k => ({ key: k, label: getStatsLabel(k), value: stats.value![k] as number }))
})

// 文本型属性
const infoStats = computed(() => {
  if (!stats.value) return []
  const numericKeys = new Set(['attack', 'defense', 'possession', 'shooting', 'goal_efficiency'])
  return Object.entries(stats.value)
    .filter(([k]) => !numericKeys.has(k))
    .map(([k, v]) => ({ key: k, label: getStatsLabel(k), value: v }))
})

// 球员按位置分组
const playersByPosition = computed(() => {
  const groups: Record<string, typeof teamStore.teamPlayers> = {
    GK: [],
    DF: [],
    MF: [],
    FW: [],
  }
  for (const p of teamStore.teamPlayers) {
    const pos = p.position || 'FW'
    if (groups[pos]) groups[pos].push(p)
    else groups.FW.push(p)
  }
  return groups
})

const positionLabels: Record<string, string> = { GK: '门将', DF: '后卫', MF: '中场', FW: '前锋' }

async function subscribeAll() {
  subscribing.value = true
  subscribeMsg.value = ''
  try {
    const res = await subscribeTeamMatches(teamId.value)
    subscribeMsg.value = res.data.message
  } catch {
    subscribeMsg.value = '订阅失败，请先登录'
  } finally {
    subscribing.value = false
  }
}

function goToCommunity() {
  router.push({ name: 'community', query: { teamId: teamId.value.toString() } })
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <LoadingSpinner v-if="teamStore.loading && !team" text="加载球队信息..." />

    <template v-else-if="team">
      <!-- Team header -->
      <section class="bg-gradient-to-br from-primary-600 to-primary-700 px-4 py-8 text-white">
        <div class="mx-auto max-w-screen-lg">
          <button
            class="mb-4 flex items-center gap-1 text-sm text-primary-200 transition-colors hover:text-white"
            @click="router.back()"
          >
            <svg
              class="h-4 w-4"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" d="M15 19l-7-7 7-7" />
            </svg>
            返回
          </button>

          <div class="flex items-center gap-4">
            <div
              class="flex h-20 w-20 flex-shrink-0 items-center justify-center overflow-hidden rounded-full bg-white/20"
            >
              <img
                v-if="team.flag_url"
                :src="team.flag_url"
                :alt="team.name"
                class="h-full w-full object-cover"
              />
              <span v-else class="text-2xl font-bold text-white/60">{{ team.code }}</span>
            </div>
            <div>
              <h1 class="text-2xl font-bold">
                {{ team.name }}
              </h1>
              <p v-if="team.name_en" class="text-sm text-primary-200">
                {{ team.name_en }}
              </p>
              <div class="mt-2 flex items-center gap-3">
                <span v-if="team.group_name" class="rounded-full bg-white/20 px-2 py-0.5 text-xs"
                  >{{ team.group_name }}组</span
                >
                <span v-if="team.coach" class="text-xs text-primary-200"
                  >主教练: {{ team.coach }}</span
                >
              </div>
            </div>
          </div>
        </div>
      </section>

      <div class="mx-auto max-w-screen-lg space-y-6 px-4 py-6">
        <!-- 球队信息 -->
        <section v-if="infoStats.length > 0">
          <h2 class="mb-3 text-lg font-bold text-gray-800">球队信息</h2>
          <div class="divide-y divide-gray-50 rounded-xl border border-gray-100 bg-white shadow-sm">
            <div
              v-for="item in infoStats"
              :key="item.key"
              class="flex items-center justify-between px-4 py-3"
            >
              <span class="text-sm text-gray-500">{{ item.label }}</span>
              <span class="text-sm font-medium text-gray-800">{{ item.value }}</span>
            </div>
          </div>
        </section>

        <!-- 战力数据可视化 -->
        <section v-if="powerStats.length > 0">
          <h2 class="mb-3 text-lg font-bold text-gray-800">战力数据</h2>
          <div class="space-y-3 rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
            <div v-for="stat in powerStats" :key="stat.key">
              <div class="mb-1 flex justify-between text-sm">
                <span class="text-gray-600">{{ stat.label }}</span>
                <span class="font-medium text-gray-800">{{ stat.value }}</span>
              </div>
              <div class="h-2 overflow-hidden rounded-full bg-gray-100">
                <div
                  class="h-full rounded-full bg-primary-500 transition-all"
                  :style="{ width: Math.min(stat.value, 100) + '%' }"
                />
              </div>
            </div>
          </div>
        </section>

        <!-- 球队简介 -->
        <section v-if="team.description">
          <h2 class="mb-3 text-lg font-bold text-gray-800">球队简介</h2>
          <div class="rounded-xl border border-gray-100 bg-white p-4 shadow-sm">
            <p class="text-sm leading-relaxed text-gray-600">
              {{ team.description }}
            </p>
          </div>
        </section>

        <!-- 球员名单（按位置分组） -->
        <section>
          <h2 class="mb-3 text-lg font-bold text-gray-800">球员名单</h2>
          <template v-if="teamStore.teamPlayers.length > 0">
            <div v-for="(players, pos) in playersByPosition" :key="pos" class="mb-4">
              <template v-if="players.length > 0">
                <h3 class="mb-2 text-sm font-medium text-gray-500">
                  {{ positionLabels[pos] || pos }}
                </h3>
                <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4">
                  <router-link
                    v-for="player in players"
                    :key="player.id"
                    :to="{ name: 'player-detail', params: { id: player.id } }"
                  >
                    <PlayerCard :player="player" />
                  </router-link>
                </div>
              </template>
            </div>
          </template>
          <EmptyState v-else message="暂无球员数据" />
        </section>

        <!-- 相关比赛 -->
        <section>
          <div class="mb-3 flex items-center justify-between">
            <h2 class="text-lg font-bold text-gray-800">相关比赛</h2>
            <button
              class="rounded-lg bg-primary-50 px-3 py-1.5 text-xs text-primary-600 transition-colors hover:bg-primary-100 disabled:opacity-50"
              :disabled="subscribing"
              @click="subscribeAll"
            >
              {{ subscribing ? '订阅中...' : '一键订阅全部提醒' }}
            </button>
          </div>
          <p v-if="subscribeMsg" class="mb-2 text-xs text-green-600">
            {{ subscribeMsg }}
          </p>

          <div v-if="teamMatches.length > 0" class="space-y-3">
            <MatchCard v-for="match in teamMatches" :key="match.id" :match="match" />
          </div>
          <EmptyState v-else message="暂无比赛数据" />
        </section>

        <!-- 球迷圈入口 -->
        <section class="pb-4">
          <button
            class="flex w-full items-center justify-center gap-2 rounded-xl bg-primary-500 py-3 text-sm font-medium text-white transition-colors hover:bg-primary-600"
            @click="goToCommunity"
          >
            <svg
              class="h-5 w-5"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M17 20h5v-2a4 4 0 00-3-3.87M9 20H4v-2a4 4 0 013-3.87"
              />
              <circle cx="9" cy="7" r="4" />
              <circle cx="17" cy="7" r="4" />
            </svg>
            进入 {{ team.name }} 球迷圈
          </button>
        </section>
      </div>
    </template>

    <EmptyState v-else message="球队不存在" action-text="返回首页" @action="router.push('/')" />
  </div>
</template>
