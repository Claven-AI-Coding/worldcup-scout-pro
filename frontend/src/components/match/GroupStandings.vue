<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getStandings } from '@/api/matches'
import StandingsTable from './StandingsTable.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

// 12 组积分榜 Tab 切换
const groups = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
const activeGroup = ref('A')

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
const loading = ref(false)

async function fetchStandings() {
  loading.value = true
  try {
    const res = await getStandings()
    standings.value = res.data as Record<string, StandingEntry[]>
  } catch {
    standings.value = {}
  } finally {
    loading.value = false
  }
}

onMounted(fetchStandings)
</script>

<template>
  <div>
    <!-- 小组 Tab -->
    <div class="flex overflow-x-auto gap-1 mb-3 scrollbar-hide">
      <button
        v-for="g in groups"
        :key="g"
        class="flex-shrink-0 px-3 py-1.5 text-xs font-medium rounded-full transition-colors"
        :class="activeGroup === g ? 'bg-green-600 text-white' : 'text-gray-400 bg-gray-100 hover:bg-gray-200'"
        @click="activeGroup = g"
      >
        {{ g }}组
      </button>
    </div>

    <LoadingSpinner v-if="loading" text="加载积分榜..." />

    <template v-else>
      <StandingsTable
        v-if="standings[activeGroup]"
        :standings="standings[activeGroup]"
        :group-name="activeGroup"
      />

      <!-- 出线标识：前 2 名绿色背景 + 最佳第三 -->
      <div v-if="standings[activeGroup]" class="mt-2 flex gap-4 text-xs text-gray-400">
        <span class="flex items-center gap-1">
          <span class="w-2 h-2 rounded-full bg-green-500"></span> 出线
        </span>
        <span class="flex items-center gap-1">
          <span class="w-2 h-2 rounded-full bg-yellow-400"></span> 待定（最佳第三）
        </span>
      </div>

      <EmptyState v-if="!standings[activeGroup]" message="暂无该组数据" />
    </template>
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
