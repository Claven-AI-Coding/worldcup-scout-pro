<script setup lang="ts">
interface Props {
  modelValue: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

interface StyleOption {
  value: string
  label: string
  gradient: string
}

const styles: StyleOption[] = [
  {
    value: 'cyberpunk',
    label: '赛博朋克',
    gradient: 'from-purple-600 via-pink-500 to-cyan-400',
  },
  {
    value: 'ink',
    label: '水墨',
    gradient: 'from-gray-800 via-gray-500 to-gray-200',
  },
  {
    value: 'comic',
    label: '漫画',
    gradient: 'from-yellow-400 via-red-500 to-blue-600',
  },
  {
    value: 'minimal',
    label: '极简',
    gradient: 'from-slate-100 via-white to-slate-200',
  },
]

function selectStyle(value: string) {
  emit('update:modelValue', value)
}
</script>

<template>
  <div class="grid grid-cols-2 gap-3">
    <div
      v-for="style in styles"
      :key="style.value"
      class="relative rounded-xl overflow-hidden cursor-pointer transition-all duration-200"
      :class="props.modelValue === style.value
        ? 'ring-2 ring-primary-500 ring-offset-2 scale-[1.02]'
        : 'hover:scale-[1.01]'"
      @click="selectStyle(style.value)"
    >
      <!-- Gradient preview -->
      <div
        class="h-24 bg-gradient-to-br"
        :class="style.gradient"
      ></div>

      <!-- Label overlay -->
      <div class="absolute inset-0 flex items-end">
        <div class="w-full px-3 py-2 bg-gradient-to-t from-black/60 to-transparent">
          <span class="text-sm font-medium text-white">{{ style.label }}</span>
        </div>
      </div>

      <!-- Check mark -->
      <div
        v-if="props.modelValue === style.value"
        class="absolute top-2 right-2 w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center"
      >
        <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
        </svg>
      </div>
    </div>
  </div>
</template>
