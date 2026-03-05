<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
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
  <div class="bg-white rounded-xl p-4">
    <h3 class="text-sm font-bold text-gray-700 mb-3">球队头像框</h3>

    <!-- 预览 -->
    <div class="flex justify-center mb-4">
      <div
        class="w-24 h-24 rounded-full border-4 ring-4 flex items-center justify-center bg-gray-100 transition-all"
        :class="frameClass"
      >
        <img
          v-if="avatarUrl"
          :src="avatarUrl"
          class="w-full h-full rounded-full object-cover"
        />
        <span v-else class="text-2xl font-bold text-gray-400">{{ teamCode || '?' }}</span>
      </div>
    </div>

    <!-- 球队名 -->
    <p v-if="teamName" class="text-xs text-center text-gray-500 mb-3">{{ teamName }}</p>

    <!-- 颜色选择 -->
    <div class="flex justify-center gap-3">
      <button
        v-for="frame in frames"
        :key="frame.id"
        class="w-8 h-8 rounded-full border-2 transition-transform"
        :class="[
          frame.border,
          selectedFrame === frame.id ? 'scale-125 ring-2 ring-offset-2' : 'hover:scale-110',
          frame.ring,
        ]"
        @click="selectedFrame = frame.id"
      />
    </div>

    <button class="w-full mt-4 py-2 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition-colors">
      保存头像框
    </button>
  </div>
</template>
