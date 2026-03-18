<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getScorers, getAssists } from '@/api/rankings'
import EmptyState from '@/components/common/EmptyState.vue'

const router = useRouter()

type RankType = 'scorers' | 'assists'
const activeTab = ref<RankType>('scorers')

interface RankEntry {
  rank: number
  player_id: number
  player_name: string
  player_name_en: string | null
  team_id: number
  team_name: string | null
  team_code: string | null
  goals?: number
  assists?: number
  appearances: number
  position: string | null
}

const scorers = ref<RankEntry[]>([])
const assists = ref<RankEntry[]>([])
const loading = ref(false)

async function loadData() {
  loading.value = true
  try {
    const [scorerRes, assistRes] = await Promise.all([getScorers(30), getAssists(30)])
    scorers.value = scorerRes.data
    assists.value = assistRes.data
  } catch {
    // 加载失败
  } finally {
    loading.value = false
  }
}

function goPlayer(id: number) {
  router.push({ name: 'player-detail', params: { id } })
}

onMounted(loadData)
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="mx-auto max-w-screen-lg">
      <!-- Tab 切换 -->
      <div class="sticky top-14 z-40 border-b border-gray-100 bg-white">
        <div class="flex">
          <button
            class="flex-1 border-b-2 py-3 text-center text-sm font-medium transition-colors"
            :class="
              activeTab === 'scorers'
                ? 'border-green-600 text-green-600'
                : 'border-transparent text-gray-500'
            "
            @click="activeTab = 'scorers'"
          >
            🏆 射手榜
          </button>
          <button
            class="flex-1 border-b-2 py-3 text-center text-sm font-medium transition-colors"
            :class="
              activeTab === 'assists'
                ? 'border-green-600 text-green-600'
                : 'border-transparent text-gray-500'
            "
            @click="activeTab = 'assists'"
          >
            🎯 助攻榜
          </button>
        </div>
      </div>

      <div class="px-4 py-4">
        <LoadingSpinner v-if="loading" text="加载排行榜..." />

        <template v-else>
          <!-- 射手榜 -->
          <div v-if="activeTab === 'scorers'">
            <div v-if="scorers.length > 0" class="overflow-hidden rounded-xl bg-white">
              <div class="grid grid-cols-12 bg-gray-50 px-4 py-2 text-xs font-medium text-gray-400">
                <span class="col-span-1">#</span>
                <span class="col-span-5">球员</span>
                <span class="col-span-3">球队</span>
                <span class="col-span-1 text-center">场</span>
                <span class="col-span-2 text-center font-bold">进球</span>
              </div>
              <div
                v-for="entry in scorers"
                :key="entry.player_id"
                class="grid cursor-pointer grid-cols-12 items-center border-t border-gray-50 px-4 py-3 hover:bg-gray-50"
                @click="goPlayer(entry.player_id)"
              >
                <span
                  class="col-span-1 text-sm font-bold"
                  :class="entry.rank <= 3 ? 'text-green-600' : 'text-gray-400'"
                >
                  {{ entry.rank }}
                </span>
                <span class="col-span-5 truncate text-sm text-gray-800">{{
                  entry.player_name
                }}</span>
                <span class="col-span-3 text-xs text-gray-500">{{ entry.team_code }}</span>
                <span class="col-span-1 text-center text-xs text-gray-400">{{
                  entry.appearances
                }}</span>
                <span class="col-span-2 text-center text-sm font-bold text-green-600">{{
                  entry.goals
                }}</span>
              </div>
            </div>
            <EmptyState v-else message="暂无射手数据" />
          </div>

          <!-- 助攻榜 -->
          <div v-if="activeTab === 'assists'">
            <div v-if="assists.length > 0" class="overflow-hidden rounded-xl bg-white">
              <div class="grid grid-cols-12 bg-gray-50 px-4 py-2 text-xs font-medium text-gray-400">
                <span class="col-span-1">#</span>
                <span class="col-span-5">球员</span>
                <span class="col-span-3">球队</span>
                <span class="col-span-1 text-center">场</span>
                <span class="col-span-2 text-center font-bold">助攻</span>
              </div>
              <div
                v-for="entry in assists"
                :key="entry.player_id"
                class="grid cursor-pointer grid-cols-12 items-center border-t border-gray-50 px-4 py-3 hover:bg-gray-50"
                @click="goPlayer(entry.player_id)"
              >
                <span
                  class="col-span-1 text-sm font-bold"
                  :class="entry.rank <= 3 ? 'text-green-600' : 'text-gray-400'"
                >
                  {{ entry.rank }}
                </span>
                <span class="col-span-5 truncate text-sm text-gray-800">{{
                  entry.player_name
                }}</span>
                <span class="col-span-3 text-xs text-gray-500">{{ entry.team_code }}</span>
                <span class="col-span-1 text-center text-xs text-gray-400">{{
                  entry.appearances
                }}</span>
                <span class="col-span-2 text-center text-sm font-bold text-green-600">{{
                  entry.assists
                }}</span>
              </div>
            </div>
            <EmptyState v-else message="暂无助攻数据" />
          </div>
        </template>
      </div>
    </div>
  </div>
</template>
