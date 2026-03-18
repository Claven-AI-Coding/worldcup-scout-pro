<script setup lang="ts">
import { ref } from 'vue'
import { setReminder } from '@/api/matches'

const props = defineProps<{
  matchId: number
}>()

const emit = defineEmits<{
  success: []
}>()

const selectedMinutes = ref(30)
const loading = ref(false)
const done = ref(false)
const error = ref('')

const options = [
  { value: 30, label: '30 分钟前' },
  { value: 60, label: '1 小时前' },
  { value: 120, label: '2 小时前' },
]

async function handleSubmit() {
  loading.value = true
  error.value = ''
  try {
    await setReminder(props.matchId, selectedMinutes.value)
    done.value = true
    emit('success')
  } catch (e: unknown) {
    error.value =
      (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
      '设置失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="rounded-xl bg-white p-4">
    <h3 class="mb-3 text-sm font-bold text-gray-700">赛前提醒</h3>

    <div v-if="done" class="py-4 text-center">
      <div class="mb-2 text-2xl text-green-500">✓</div>
      <p class="text-sm text-gray-600">提醒已设置</p>
    </div>

    <template v-else>
      <div class="mb-4 flex gap-2">
        <button
          v-for="opt in options"
          :key="opt.value"
          class="flex-1 rounded-lg border py-2 text-xs transition-colors"
          :class="
            selectedMinutes === opt.value
              ? 'border-green-500 bg-green-50 text-green-700'
              : 'border-gray-200 text-gray-500 hover:border-gray-300'
          "
          @click="selectedMinutes = opt.value"
        >
          {{ opt.label }}
        </button>
      </div>

      <button
        class="w-full rounded-lg bg-green-600 py-2.5 text-sm font-medium text-white transition-colors hover:bg-green-700 disabled:opacity-50"
        :disabled="loading"
        @click="handleSubmit"
      >
        {{ loading ? '设置中...' : '设置提醒' }}
      </button>

      <p v-if="error" class="mt-2 text-center text-xs text-red-500">
        {{ error }}
      </p>
    </template>
  </div>
</template>
