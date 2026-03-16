<script setup lang="ts">
import { useRouter } from 'vue-router'

interface Team {
  id: number
  name: string
  name_en?: string | null
  code: string
  group_name: string | null
  flag_url: string | null
  coach: string | null
}

interface Props {
  team: Team
}

const props = defineProps<Props>()

const router = useRouter()

function goToTeam() {
  router.push({ name: 'team-detail', params: { id: props.team.id } })
}
</script>

<template>
  <div
    class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 cursor-pointer hover:shadow-md hover:-translate-y-0.5 transition-all duration-200"
    @click="goToTeam"
  >
    <!-- Flag -->
    <div class="w-16 h-16 mx-auto rounded-full bg-gray-100 flex items-center justify-center overflow-hidden mb-3">
      <img
        v-if="props.team.flag_url"
        :src="props.team.flag_url"
        :alt="props.team.name"
        class="w-full h-full object-cover"
      >
      <span
        v-else
        class="text-xl font-bold text-gray-300"
      >{{ props.team.code }}</span>
    </div>

    <!-- Name -->
    <h3 class="text-sm font-bold text-gray-800 text-center truncate">
      {{ props.team.name }}
    </h3>

    <!-- Group badge -->
    <div
      v-if="props.team.group_name"
      class="mt-2 flex justify-center"
    >
      <span class="text-xs px-2 py-0.5 bg-blue-50 text-blue-600 rounded-full font-medium">
        {{ props.team.group_name }}
      </span>
    </div>

    <!-- Coach -->
    <p
      v-if="props.team.coach"
      class="mt-2 text-xs text-gray-400 text-center truncate"
    >
      主教练: {{ props.team.coach }}
    </p>
  </div>
</template>
