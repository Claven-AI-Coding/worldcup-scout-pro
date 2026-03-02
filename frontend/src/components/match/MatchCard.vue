<script setup lang="ts">
import { computed } from 'vue'

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

const emit = defineEmits<{
  click: [match: Match]
}>()

const formattedTime = computed(() => {
  const d = new Date(props.match.start_time)
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hours = String(d.getHours()).padStart(2, '0')
  const mins = String(d.getMinutes()).padStart(2, '0')
  return `${month}/${day} ${hours}:${mins}`
})

const statusConfig = computed(() => {
  switch (props.match.status) {
    case 'live':
      return { label: '进行中', class: 'bg-red-100 text-red-600', pulse: true }
    case 'finished':
      return { label: '已结束', class: 'bg-gray-100 text-gray-500', pulse: false }
    default:
      return { label: '未开始', class: 'bg-blue-100 text-blue-600', pulse: false }
  }
})
</script>

<template>
  <div
    class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 min-w-[280px] cursor-pointer hover:shadow-md transition-shadow"
    @click="emit('click', props.match)"
  >
    <!-- Header: time + status -->
    <div class="flex items-center justify-between mb-3">
      <span class="text-xs text-gray-400">{{ formattedTime }}</span>
      <span
        class="inline-flex items-center gap-1 text-xs font-medium px-2 py-0.5 rounded-full"
        :class="statusConfig.class"
      >
        <span
          v-if="statusConfig.pulse"
          class="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse"
        ></span>
        {{ statusConfig.label }}
      </span>
    </div>

    <!-- Teams and score -->
    <div class="flex items-center justify-between gap-2">
      <!-- Home team -->
      <div class="flex flex-col items-center flex-1 min-w-0">
        <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden mb-1">
          <img
            v-if="props.match.home_team.flag_url"
            :src="props.match.home_team.flag_url"
            :alt="props.match.home_team.name"
            class="w-full h-full object-cover"
          />
          <span v-else class="text-sm font-bold text-gray-400">{{ props.match.home_team.code }}</span>
        </div>
        <span class="text-xs text-gray-700 font-medium truncate w-full text-center">
          {{ props.match.home_team.name }}
        </span>
      </div>

      <!-- Score -->
      <div class="flex items-center gap-2 px-3">
        <template v-if="props.match.status === 'upcoming'">
          <span class="text-lg font-bold text-gray-300">VS</span>
        </template>
        <template v-else>
          <span class="text-2xl font-bold text-gray-800">{{ props.match.home_score }}</span>
          <span class="text-lg text-gray-300">:</span>
          <span class="text-2xl font-bold text-gray-800">{{ props.match.away_score }}</span>
        </template>
      </div>

      <!-- Away team -->
      <div class="flex flex-col items-center flex-1 min-w-0">
        <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center overflow-hidden mb-1">
          <img
            v-if="props.match.away_team.flag_url"
            :src="props.match.away_team.flag_url"
            :alt="props.match.away_team.name"
            class="w-full h-full object-cover"
          />
          <span v-else class="text-sm font-bold text-gray-400">{{ props.match.away_team.code }}</span>
        </div>
        <span class="text-xs text-gray-700 font-medium truncate w-full text-center">
          {{ props.match.away_team.name }}
        </span>
      </div>
    </div>

    <!-- Venue -->
    <div v-if="props.match.venue" class="mt-3 text-center">
      <span class="text-xs text-gray-400">{{ props.match.venue }}</span>
    </div>
  </div>
</template>
