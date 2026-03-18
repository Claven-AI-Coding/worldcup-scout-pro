<script setup lang="ts">
// 统一空状态组件：支持 no-data / no-network / no-permission 三种类型
interface Props {
  message: string
  type?: 'no-data' | 'no-network' | 'no-permission'
  actionText?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'no-data',
  actionText: '',
})

const emit = defineEmits<{
  action: []
}>()

// 根据类型返回默认操作文字
const defaultActionText: Record<string, string> = {
  'no-data': '',
  'no-network': '重新加载',
  'no-permission': '去登录',
}

const displayAction = props.actionText || defaultActionText[props.type] || ''
</script>

<template>
  <div class="flex flex-col items-center justify-center px-6 py-16">
    <!-- 无数据图标 -->
    <div
      v-if="type === 'no-data'"
      class="mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-gray-100"
    >
      <svg
        class="h-10 w-10 text-gray-300"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
        />
      </svg>
    </div>

    <!-- 无网络图标 -->
    <div
      v-else-if="type === 'no-network'"
      class="mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-red-50"
    >
      <svg
        class="h-10 w-10 text-red-300"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M18.364 5.636a9 9 0 010 12.728M5.636 18.364a9 9 0 010-12.728"
        />
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M15.536 8.464a5 5 0 010 7.072M8.464 15.536a5 5 0 010-7.072"
        />
        <circle cx="12" cy="12" r="1" fill="currentColor" />
        <path stroke-linecap="round" stroke-width="2" d="M4 4l16 16" />
      </svg>
    </div>

    <!-- 无权限图标 -->
    <div
      v-else-if="type === 'no-permission'"
      class="mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-yellow-50"
    >
      <svg
        class="h-10 w-10 text-yellow-400"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        viewBox="0 0 24 24"
      >
        <rect x="3" y="11" width="18" height="11" rx="2" />
        <path d="M7 11V7a5 5 0 0110 0v4" />
      </svg>
    </div>

    <p class="text-center text-sm text-gray-400">
      {{ props.message }}
    </p>

    <button
      v-if="displayAction"
      class="mt-4 rounded-full bg-primary-500 px-6 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-600"
      @click="emit('action')"
    >
      {{ displayAction }}
    </button>
  </div>
</template>
