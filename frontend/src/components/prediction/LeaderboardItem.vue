<script setup lang="ts">
import { computed } from 'vue'

interface LeaderboardEntry {
  user_id: number
  nickname: string
  avatar: string | null
  total_points: number
  win_streak: number
}

interface Props {
  entry: LeaderboardEntry
  rank: number
}

const props = defineProps<Props>()

const rankStyle = computed(() => {
  switch (props.rank) {
    case 1:
      return 'bg-gradient-to-br from-yellow-400 to-yellow-500 text-white'
    case 2:
      return 'bg-gradient-to-br from-gray-300 to-gray-400 text-white'
    case 3:
      return 'bg-gradient-to-br from-amber-600 to-amber-700 text-white'
    default:
      return 'bg-gray-100 text-gray-500'
  }
})
</script>

<template>
  <div class="flex items-center gap-3 py-3 px-4 hover:bg-gray-50 transition-colors rounded-lg">
    <!-- Rank -->
    <div
      class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0"
      :class="rankStyle"
    >
      {{ props.rank }}
    </div>

    <!-- User avatar -->
    <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden flex-shrink-0">
      <img
        v-if="props.entry.avatar"
        :src="props.entry.avatar"
        :alt="props.entry.nickname"
        class="w-full h-full object-cover"
      >
      <svg
        v-else
        class="w-5 h-5 text-gray-400"
        fill="currentColor"
        viewBox="0 0 24 24"
      >
        <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
      </svg>
    </div>

    <!-- Name and streak -->
    <div class="flex-1 min-w-0">
      <p class="text-sm font-medium text-gray-800 truncate">
        {{ props.entry.nickname }}
      </p>
      <div
        v-if="props.entry.win_streak >= 3"
        class="flex items-center gap-1 mt-0.5"
      >
        <!-- Flame icon for win streak -->
        <svg
          class="w-3.5 h-3.5 text-orange-500"
          viewBox="0 0 24 24"
          fill="currentColor"
        >
          <path d="M12 23c-4.97 0-9-3.58-9-8 0-3.07 2.13-5.64 3.5-7.13.39-.42 1.07-.17 1.1.4.12 2.14 1.23 3.8 2.4 4.46V12c0-4.56 3.93-8.86 5.47-10.37.38-.38 1.03-.14 1.08.39.33 3.7 2.88 6.78 3.95 8.48C21.67 12.4 21 14.81 21 15c0 4.42-4.03 8-9 8z" />
        </svg>
        <span class="text-xs text-orange-500 font-medium">{{ props.entry.win_streak }}连胜</span>
      </div>
    </div>

    <!-- Points -->
    <div class="text-right flex-shrink-0">
      <p class="text-sm font-bold text-gray-800">
        {{ props.entry.total_points }}
      </p>
      <p class="text-xs text-gray-400">
        积分
      </p>
    </div>
  </div>
</template>
