<script setup lang="ts">
import { computed } from 'vue'

interface Player {
  id: number
  team_id: number
  name: string
  number: number | null
  position: string | null
  age: number | null
  club: string | null
}

interface Props {
  player: Player
}

const props = defineProps<Props>()

const positionConfig = computed(() => {
  switch (props.player.position) {
    case 'GK':
      return { label: '门将', class: 'bg-yellow-100 text-yellow-700' }
    case 'DF':
      return { label: '后卫', class: 'bg-blue-100 text-blue-700' }
    case 'MF':
      return { label: '中场', class: 'bg-green-100 text-green-700' }
    case 'FW':
      return { label: '前锋', class: 'bg-red-100 text-red-700' }
    default:
      return { label: props.player.position || '未知', class: 'bg-gray-100 text-gray-600' }
  }
})
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 hover:shadow-md transition-shadow">
    <!-- Photo placeholder + number -->
    <div class="relative w-16 h-16 mx-auto mb-3">
      <div class="w-16 h-16 rounded-full bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
        <svg class="w-8 h-8 text-gray-300" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
        </svg>
      </div>
      <span
        v-if="props.player.number !== null"
        class="absolute -top-1 -right-1 w-6 h-6 bg-gray-800 text-white text-xs font-bold rounded-full flex items-center justify-center"
      >
        {{ props.player.number }}
      </span>
    </div>

    <!-- Name -->
    <h4 class="text-sm font-bold text-gray-800 text-center truncate">{{ props.player.name }}</h4>

    <!-- Position badge -->
    <div class="mt-2 flex justify-center">
      <span
        class="text-xs font-medium px-2 py-0.5 rounded-full"
        :class="positionConfig.class"
      >
        {{ positionConfig.label }}
      </span>
    </div>

    <!-- Club -->
    <p v-if="props.player.club" class="mt-2 text-xs text-gray-400 text-center truncate">
      {{ props.player.club }}
    </p>
  </div>
</template>
