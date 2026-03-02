<script setup lang="ts">
interface Props {
  message: string
  actionText?: string
}

const props = withDefaults(defineProps<Props>(), {
  actionText: '',
})

const emit = defineEmits<{
  action: []
}>()
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 px-6">
    <!-- Empty icon -->
    <div class="w-20 h-20 rounded-full bg-gray-100 flex items-center justify-center mb-4">
      <svg class="w-10 h-10 text-gray-300" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
        />
      </svg>
    </div>

    <p class="text-sm text-gray-400 text-center">{{ props.message }}</p>

    <button
      v-if="props.actionText"
      class="mt-4 px-6 py-2 bg-primary-500 text-white text-sm font-medium rounded-full hover:bg-primary-600 transition-colors"
      @click="emit('action')"
    >
      {{ props.actionText }}
    </button>
  </div>
</template>
