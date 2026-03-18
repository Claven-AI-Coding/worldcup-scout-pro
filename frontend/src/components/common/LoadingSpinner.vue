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
      class="h-10 w-10 animate-spin rounded-full border-4 border-gray-200 border-t-primary-500"
    />
    <p v-if="text" class="mt-3 text-sm text-gray-500">
      {{ text }}
    </p>
  </div>
</template>
