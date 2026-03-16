<script setup lang="ts">
interface Props {
  text?: string
}

withDefaults(defineProps<Props>(), {
  text: '',
})
</script>

<template>
  <div class="flex flex-col items-center justify-center py-12">
    <div
      class="w-10 h-10 border-4 border-gray-200 border-t-primary-500 rounded-full animate-spin"
    />
    <p
      v-if="text"
      class="mt-3 text-sm text-gray-500"
    >
      {{ text }}
    </p>
  </div>
</template>
