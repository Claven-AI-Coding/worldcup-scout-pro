<script setup lang="ts">
defineProps<{
  text?: string
}>()
</script>

<template>
  <div class="flex items-start gap-2 rounded-lg border border-yellow-200 bg-yellow-50 px-3 py-2">
    <svg
      class="mt-0.5 h-4 w-4 flex-shrink-0 text-yellow-500"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4.5c-.77-.833-2.694-.833-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"
      />
    </svg>
    <p class="text-xs text-yellow-700">
      {{ text || '预测仅供参考，不构成任何投注建议' }}
    </p>
  </div>
</template>
