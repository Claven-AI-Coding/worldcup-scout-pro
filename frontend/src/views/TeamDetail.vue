<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTeamStore } from '@/stores/teams'
import { useMatchStore } from '@/stores/matches'
import PlayerCard from '@/components/team/PlayerCard.vue'
import MatchCard from '@/components/match/MatchCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const route = useRoute()
const router = useRouter()
const teamStore = useTeamStore()
const matchStore = useMatchStore()

const teamId = computed(() => Number(route.params.id))

onMounted(() => {
  teamStore.fetchTeam(teamId.value)
  teamStore.fetchTeamPlayers(teamId.value)
  matchStore.fetchMatches()
})

const team = computed(() => teamStore.currentTeam)

const teamMatches = computed(() => {
  return matchStore.matches.filter(
    (m) => m.home_team.id === teamId.value || m.away_team.id === teamId.value
  )
})

const stats = computed(() => {
  if (!team.value?.stats) return null
  return team.value.stats as Record<string, unknown>
})

function goToCommunity() {
  router.push({ name: 'community', query: { teamId: teamId.value.toString() } })
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <LoadingSpinner v-if="teamStore.loading && !team" text="加载球队信息..." />

    <template v-else-if="team">
      <!-- Team header -->
      <section class="bg-gradient-to-br from-primary-600 to-primary-700 text-white px-4 py-8">
        <div class="max-w-screen-lg mx-auto">
          <!-- Back button -->
          <button
            class="mb-4 flex items-center gap-1 text-sm text-primary-200 hover:text-white transition-colors"
            @click="router.back()"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" d="M15 19l-7-7 7-7" />
            </svg>
            返回
          </button>

          <div class="flex items-center gap-4">
            <!-- Flag -->
            <div class="w-20 h-20 rounded-full bg-white/20 flex items-center justify-center overflow-hidden flex-shrink-0">
              <img
                v-if="team.flag_url"
                :src="team.flag_url"
                :alt="team.name"
                class="w-full h-full object-cover"
              />
              <span v-else class="text-2xl font-bold text-white/60">{{ team.code }}</span>
            </div>

            <div>
              <h1 class="text-2xl font-bold">{{ team.name }}</h1>
              <p v-if="team.name_en" class="text-sm text-primary-200">{{ team.name_en }}</p>
              <div class="flex items-center gap-3 mt-2">
                <span v-if="team.group_name" class="text-xs px-2 py-0.5 bg-white/20 rounded-full">
                  {{ team.group_name }}
                </span>
                <span v-if="team.coach" class="text-xs text-primary-200">
                  主教练: {{ team.coach }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div class="max-w-screen-lg mx-auto px-4 py-6 space-y-8">
        <!-- Stats section -->
        <section v-if="stats">
          <h2 class="text-lg font-bold text-gray-800 mb-3">球队数据</h2>
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div
                v-for="(value, key) in stats"
                :key="String(key)"
                class="text-center"
              >
                <p class="text-2xl font-bold text-gray-800">{{ value }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ String(key) }}</p>
              </div>
            </div>
          </div>
        </section>

        <!-- Description -->
        <section v-if="team.description">
          <h2 class="text-lg font-bold text-gray-800 mb-3">球队简介</h2>
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <p class="text-sm text-gray-600 leading-relaxed">{{ team.description }}</p>
          </div>
        </section>

        <!-- Player roster -->
        <section>
          <h2 class="text-lg font-bold text-gray-800 mb-3">球员名单</h2>

          <div
            v-if="teamStore.teamPlayers.length > 0"
            class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3"
          >
            <router-link
              v-for="player in teamStore.teamPlayers"
              :key="player.id"
              :to="{ name: 'player-detail', params: { id: player.id } }"
            >
              <PlayerCard :player="player" />
            </router-link>
          </div>

          <EmptyState v-else message="暂无球员数据" />
        </section>

        <!-- Recent matches -->
        <section>
          <h2 class="text-lg font-bold text-gray-800 mb-3">相关比赛</h2>

          <div v-if="teamMatches.length > 0" class="space-y-3">
            <MatchCard
              v-for="match in teamMatches"
              :key="match.id"
              :match="match"
            />
          </div>

          <EmptyState v-else message="暂无比赛数据" />
        </section>

        <!-- Community link -->
        <section class="pb-4">
          <button
            class="w-full py-3 bg-primary-500 text-white text-sm font-medium rounded-xl hover:bg-primary-600 transition-colors flex items-center justify-center gap-2"
            @click="goToCommunity"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a4 4 0 00-3-3.87M9 20H4v-2a4 4 0 013-3.87" />
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
