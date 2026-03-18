<script setup lang="ts">
import { ref, computed } from 'vue'

defineProps<{
  teamCode?: string
  teamName?: string
  avatarUrl?: string
}>()

const frames = [
  { id: 'gold', label: '金色', border: 'border-yellow-400', ring: 'ring-yellow-300' },
  { id: 'green', label: '绿色', border: 'border-green-500', ring: 'ring-green-400' },
  { id: 'red', label: '红色', border: 'border-red-500', ring: 'ring-red-400' },
  { id: 'blue', label: '蓝色', border: 'border-blue-500', ring: 'ring-blue-400' },
]

const selectedFrame = ref('gold')

const frameClass = computed(() => {
  const frame = frames.find(f => f.id === selectedFrame.value)
  return frame ? `${frame.border} ${frame.ring}` : ''
})
</script>

<template>
  <div class="rounded-xl bg-white p-4">
    <h3 class="mb-3 text-sm font-bold text-gray-700">球队头像框</h3>

    <!-- 预览 -->
    <div class="mb-4 flex justify-center">
      <div
        class="flex h-24 w-24 items-center justify-center rounded-full border-4 bg-gray-100 ring-4 transition-all"
        :class="frameClass"
      >
        <img v-if="avatarUrl" :src="avatarUrl" class="h-full w-full rounded-full object-cover" />
        <span v-else class="text-2xl font-bold text-gray-400">{{ teamCode || '?' }}</span>
      </div>
    </div>

    <!-- 球队名 -->
    <p v-if="teamName" class="mb-3 text-center text-xs text-gray-500">
      {{ teamName }}
    </p>

    <!-- 颜色选择 -->
    <div class="flex justify-center gap-3">
      <button
        v-for="frame in frames"
        :key="frame.id"
        class="h-8 w-8 rounded-full border-2 transition-transform"
        :class="[
          frame.border,
          selectedFrame === frame.id ? 'scale-125 ring-2 ring-offset-2' : 'hover:scale-110',
          frame.ring,
        ]"
        @click="selectedFrame = frame.id"
      />
    </div>

    <button
      class="mt-4 w-full rounded-lg bg-green-600 py-2 text-sm text-white transition-colors hover:bg-green-700"
    >
      保存头像框
    </button>
  </div>
</template>
