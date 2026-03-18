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
    class="cursor-pointer rounded-xl border border-gray-100 bg-white p-4 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
    @click="goToTeam"
  >
    <!-- Flag -->
    <div
      class="mx-auto mb-3 flex h-16 w-16 items-center justify-center overflow-hidden rounded-full bg-gray-100"
    >
      <img
        v-if="props.team.flag_url"
        :src="props.team.flag_url"
        :alt="props.team.name"
        class="h-full w-full object-cover"
      />
      <span v-else class="text-xl font-bold text-gray-300">{{ props.team.code }}</span>
    </div>

    <!-- Name -->
    <h3 class="truncate text-center text-sm font-bold text-gray-800">
      {{ props.team.name }}
    </h3>

    <!-- Group badge -->
    <div v-if="props.team.group_name" class="mt-2 flex justify-center">
      <span class="rounded-full bg-blue-50 px-2 py-0.5 text-xs font-medium text-blue-600">
        {{ props.team.group_name }}
      </span>
    </div>

    <!-- Coach -->
    <p v-if="props.team.coach" class="mt-2 truncate text-center text-xs text-gray-400">
      主教练: {{ props.team.coach }}
    </p>
  </div>
</template>
