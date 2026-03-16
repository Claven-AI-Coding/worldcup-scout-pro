<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

interface Team {
  id: number
  name: string
  code: string
  flag_url: string | null
}

interface Match {
  id: number
  stage: string
  group_name: string | null
  home_team: Team
  away_team: Team
  home_score: number | null
  away_score: number | null
  status: string
  start_time: string
  venue: string | null
}

interface Props {
  match: Match
}

const props = defineProps<Props>()
const router = useRouter()

const formattedTime = computed(() => {
  const d = new Date(props.match.start_time)
  const hours = String(d.getHours()).padStart(2, '0')
  const mins = String(d.getMinutes()).padStart(2, '0')
  return `${hours}:${mins}`
})

const stageLabel = computed(() => {
  const map: Record<string, string> = {
    group: props.match.group_name ? `小组赛 ${props.match.group_name}组` : '小组赛',
    round_32: '32强赛',
    round_16: '16强赛',
    quarter: '1/4决赛',
    semi: '半决赛',
    third_place: '三四名决赛',
    final: '决赛',
  }
  return map[props.match.stage] || props.match.stage
})

// 状态配置：已结束灰色、进行中红色、未开始绿色
const statusConfig = computed(() => {
  switch (props.match.status) {
    case 'live':
      return { label: '直播中', class: 'bg-red-100 text-red-600', pulse: true }
    case 'finished':
      return { label: '已结束', class: 'bg-gray-100 text-gray-400', pulse: false }
    default:
      return { label: '未开始', class: 'bg-green-100 text-green-600', pulse: false }
  }
})

// 卡片整体样式：已结束半透明灰化，进行中加红色左边框
const cardClass = computed(() => {
  if (props.match.status === 'finished') {
    return 'opacity-60 border-gray-200'
  }
  if (props.match.status === 'live') {
    return 'border-l-4 border-l-red-500 border-gray-100'
  }
  return 'border-gray-100'
})

function goToDetail() {
  router.push({ name: 'match-detail', params: { id: props.match.id } })
}
</script>

<template>
  <div
    class="bg-white rounded-xl shadow-sm border p-4 min-w-[280px] cursor-pointer hover:shadow-md transition-all"
    :class="cardClass"
    @click="goToDetail"
  >
    <!-- 顶部：阶段 + 时间 + 状态 -->
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-2">
        <span class="text-xs text-gray-500 bg-gray-50 px-2 py-0.5 rounded">{{ stageLabel }}</span>
        <span class="text-xs text-gray-400">{{ formattedTime }}</span>
      </div>
      <span
        class="inline-flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded-full"
        :class="statusConfig.class"
      >
        <span
          v-if="statusConfig.pulse"
          class="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse"
        />
        {{ statusConfig.label }}
      </span>
    </div>

    <!-- 双方球队和比分 -->
    <div class="flex items-center justify-between gap-2">
      <!-- 主队 -->
      <div class="flex flex-col items-center flex-1 min-w-0">
        <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden mb-1">
          <img
            v-if="props.match.home_team.flag_url"
            :src="props.match.home_team.flag_url"
            :alt="props.match.home_team.name"
            class="w-full h-full object-cover"
          >
          <span
            v-else
            class="text-sm font-bold text-gray-400"
          >{{ props.match.home_team.code }}</span>
        </div>
        <span class="text-xs text-gray-700 font-medium truncate w-full text-center">
          {{ props.match.home_team.name }}
        </span>
      </div>

      <!-- 比分 -->
      <div class="flex items-center gap-2 px-3">
        <template v-if="props.match.status === 'upcoming'">
          <span class="text-lg font-bold text-gray-300">VS</span>
        </template>
        <template v-else>
          <span
            class="text-2xl font-bold"
            :class="props.match.status === 'live' ? 'text-red-600' : 'text-gray-800'"
          >
            {{ props.match.home_score }}
          </span>
          <span class="text-lg text-gray-300">:</span>
          <span
            class="text-2xl font-bold"
            :class="props.match.status === 'live' ? 'text-red-600' : 'text-gray-800'"
          >
            {{ props.match.away_score }}
          </span>
        </template>
      </div>

      <!-- 客队 -->
      <div class="flex flex-col items-center flex-1 min-w-0">
        <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden mb-1">
          <img
            v-if="props.match.away_team.flag_url"
            :src="props.match.away_team.flag_url"
            :alt="props.match.away_team.name"
            class="w-full h-full object-cover"
          >
          <span
            v-else
            class="text-sm font-bold text-gray-400"
          >{{ props.match.away_team.code }}</span>
        </div>
        <span class="text-xs text-gray-700 font-medium truncate w-full text-center">
          {{ props.match.away_team.name }}
        </span>
      </div>
    </div>

    <!-- 场馆 -->
    <div
      v-if="props.match.venue"
      class="mt-3 text-center"
    >
      <span class="text-xs text-gray-400">{{ props.match.venue }}</span>
    </div>
  </div>
</template>
