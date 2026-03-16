<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTeamStore } from '@/stores/teams'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const router = useRouter()
const teamStore = useTeamStore()

// 筛选
type FilterMode = 'group' | 'confederation'
const filterMode = ref<FilterMode>('group')
const activeGroup = ref('')
const activeConfederation = ref('')
const searchQuery = ref('')

const groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
const confederations = [
  { value: 'UEFA', label: '欧洲' },
  { value: 'CONMEBOL', label: '南美' },
  { value: 'CONCACAF', label: '中北美' },
  { value: 'CAF', label: '非洲' },
  { value: 'AFC', label: '亚洲' },
  { value: 'OFC', label: '大洋洲' },
]

const filteredTeams = computed(() => {
  let teams = teamStore.teams
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    teams = teams.filter(t =>
      t.name.toLowerCase().includes(q) ||
      (t.name_en && t.name_en.toLowerCase().includes(q)) ||
      t.code.toLowerCase().includes(q)
    )
  }
  if (filterMode.value === 'group' && activeGroup.value) {
    teams = teams.filter(t => t.group_name === activeGroup.value)
  }
  if (filterMode.value === 'confederation' && activeConfederation.value) {
    teams = teams.filter(t => t.stats?.confederation === activeConfederation.value)
  }
  return teams
})

function goTeam(id: number) {
  router.push({ name: 'team-detail', params: { id } })
}

function goRankings() {
  router.push({ name: 'rankings' })
}

onMounted(() => {
  teamStore.fetchTeams()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-screen-lg mx-auto">
      <!-- 搜索 -->
      <div class="sticky top-14 z-40 bg-white border-b border-gray-100 px-4 py-3">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索球队..."
          class="w-full px-4 py-2 bg-gray-50 rounded-lg text-sm border border-gray-200 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
        >
      </div>

      <div class="px-4 py-4">
        <!-- 快捷入口 -->
        <div class="flex gap-3 mb-4">
          <button
            class="flex-1 bg-white rounded-xl p-3 border border-gray-100 hover:shadow-md transition-shadow text-center"
            @click="goRankings"
          >
            <div class="text-lg mb-1">
              🏆
            </div>
            <span class="text-xs text-gray-600">射手榜</span>
          </button>
          <button
            class="flex-1 bg-white rounded-xl p-3 border border-gray-100 hover:shadow-md transition-shadow text-center"
            @click="goRankings"
          >
            <div class="text-lg mb-1">
              🎯
            </div>
            <span class="text-xs text-gray-600">助攻榜</span>
          </button>
          <button
            class="flex-1 bg-white rounded-xl p-3 border border-gray-100 hover:shadow-md transition-shadow text-center"
            @click="filterMode = filterMode === 'group' ? 'confederation' : 'group'"
          >
            <div class="text-lg mb-1">
              🌍
            </div>
            <span class="text-xs text-gray-600">{{ filterMode === 'group' ? '按大洲' : '按小组' }}</span>
          </button>
        </div>

        <!-- 筛选 Tab -->
        <div class="flex overflow-x-auto gap-1 mb-4 scrollbar-hide">
          <template v-if="filterMode === 'group'">
            <button
              class="flex-shrink-0 px-3 py-1 text-xs rounded-full transition-colors"
              :class="activeGroup === '' ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-500'"
              @click="activeGroup = ''"
            >
              全部
            </button>
            <button
              v-for="g in groups"
              :key="g"
              class="flex-shrink-0 px-3 py-1 text-xs rounded-full transition-colors"
              :class="activeGroup === g ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-500'"
              @click="activeGroup = g"
            >
              {{ g }}组
            </button>
          </template>
          <template v-else>
            <button
              class="flex-shrink-0 px-3 py-1 text-xs rounded-full transition-colors"
              :class="activeConfederation === '' ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-500'"
              @click="activeConfederation = ''"
            >
              全部
            </button>
            <button
              v-for="c in confederations"
              :key="c.value"
              class="flex-shrink-0 px-3 py-1 text-xs rounded-full transition-colors"
              :class="activeConfederation === c.value ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-500'"
              @click="activeConfederation = c.value"
            >
              {{ c.label }}
            </button>
          </template>
        </div>

        <!-- 球队列表 -->
        <SkeletonLoader
          v-if="teamStore.loading"
          type="grid"
          :count="8"
        />

        <div
          v-else-if="filteredTeams.length > 0"
          class="grid grid-cols-2 gap-3"
        >
          <div
            v-for="team in filteredTeams"
            :key="team.id"
            class="bg-white rounded-xl p-4 border border-gray-100 cursor-pointer hover:shadow-md transition-shadow"
            @click="goTeam(team.id)"
          >
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0">
                <span class="text-sm font-bold text-gray-500">{{ team.code }}</span>
              </div>
              <div class="min-w-0">
                <p class="text-sm font-medium text-gray-800 truncate">
                  {{ team.name }}
                </p>
                <p class="text-xs text-gray-400">
                  {{ team.group_name }}组 · {{ team.stats?.confederation || '' }}
                </p>
              </div>
            </div>
            <div
              v-if="team.stats?.fifa_ranking"
              class="mt-2 text-xs text-gray-400"
            >
              FIFA 排名：#{{ team.stats.fifa_ranking }}
            </div>
          </div>
        </div>

        <EmptyState
          v-else
          message="未找到球队"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>
