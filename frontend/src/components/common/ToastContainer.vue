<script setup lang="ts">
import { useToast } from '@/composables/useToast'

const { toasts } = useToast()

const typeClasses: Record<string, string> = {
  success: 'bg-green-600 text-white',
  error: 'bg-red-600 text-white',
  warning: 'bg-yellow-500 text-white',
  info: 'bg-gray-800 text-white',
}

const typeIcons: Record<string, string> = {
  success: 'M5 13l4 4L19 7',
  error: 'M6 18L18 6M6 6l12 12',
  warning: 'M12 9v4m0 4h.01',
  info: 'M13 16h-1v-4h-1m1-4h.01',
}
</script>

<template>
  <Teleport to="body">
    <div
      class="pointer-events-none fixed left-0 right-0 top-16 z-[999] flex flex-col items-center gap-2 px-4"
    >
      <TransitionGroup
        enter-active-class="transition-all duration-300 ease-out"
        leave-active-class="transition-all duration-200 ease-in"
        enter-from-class="opacity-0 -translate-y-4 scale-95"
        enter-to-class="opacity-100 translate-y-0 scale-100"
        leave-from-class="opacity-100 translate-y-0 scale-100"
        leave-to-class="opacity-0 -translate-y-2 scale-95"
      >
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="pointer-events-auto flex w-full max-w-sm items-center gap-3 rounded-lg px-4 py-3 shadow-lg"
          :class="typeClasses[toast.type]"
        >
          <svg
            class="h-5 w-5 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" :d="typeIcons[toast.type]" />
          </svg>
          <span class="text-sm font-medium">{{ toast.message }}</span>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>
