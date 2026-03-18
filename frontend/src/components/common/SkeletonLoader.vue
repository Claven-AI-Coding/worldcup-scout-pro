<script setup lang="ts">
// 骨架屏组件：支持多种布局类型
defineProps<{
  type?: 'card' | 'list' | 'detail' | 'grid'
  count?: number
}>()
</script>

<template>
  <div class="animate-pulse">
    <!-- 卡片骨架 -->
    <template v-if="type === 'card' || !type">
      <div v-for="i in count || 3" :key="i" class="mb-3 rounded-xl bg-white p-4">
        <div class="mb-3 flex items-center gap-3">
          <div class="h-10 w-10 rounded-full bg-gray-200" />
          <div class="flex-1">
            <div class="mb-2 h-4 w-3/4 rounded bg-gray-200" />
            <div class="h-3 w-1/2 rounded bg-gray-100" />
          </div>
        </div>
        <div class="mb-2 h-3 w-full rounded bg-gray-100" />
        <div class="h-3 w-2/3 rounded bg-gray-100" />
      </div>
    </template>

    <!-- 列表骨架 -->
    <template v-if="type === 'list'">
      <div
        v-for="i in count || 5"
        :key="i"
        class="flex items-center gap-3 border-b border-gray-50 py-3"
      >
        <div class="h-8 w-8 flex-shrink-0 rounded-full bg-gray-200" />
        <div class="flex-1">
          <div class="mb-1 h-4 w-2/3 rounded bg-gray-200" />
          <div class="h-3 w-1/3 rounded bg-gray-100" />
        </div>
        <div class="h-6 w-16 rounded bg-gray-100" />
      </div>
    </template>

    <!-- 详情骨架 -->
    <template v-if="type === 'detail'">
      <div class="mb-4 rounded-xl bg-white p-4">
        <div class="mb-4 flex items-center justify-between">
          <div class="h-16 w-16 rounded-full bg-gray-200" />
          <div class="h-8 w-20 rounded bg-gray-200" />
          <div class="h-16 w-16 rounded-full bg-gray-200" />
        </div>
        <div class="mx-auto mb-3 h-4 w-1/2 rounded bg-gray-200" />
        <div class="mx-auto h-3 w-1/3 rounded bg-gray-100" />
      </div>
      <div class="rounded-xl bg-white p-4">
        <div class="mb-4 h-4 w-1/4 rounded bg-gray-200" />
        <div class="space-y-3">
          <div class="h-3 w-full rounded bg-gray-100" />
          <div class="h-3 w-5/6 rounded bg-gray-100" />
          <div class="h-3 w-4/6 rounded bg-gray-100" />
        </div>
      </div>
    </template>

    <!-- 网格骨架 -->
    <template v-if="type === 'grid'">
      <div class="grid grid-cols-2 gap-3">
        <div v-for="i in count || 6" :key="i" class="rounded-xl bg-white p-4">
          <div class="mb-3 h-10 w-10 rounded-full bg-gray-200" />
          <div class="mb-2 h-4 w-3/4 rounded bg-gray-200" />
          <div class="h-3 w-1/2 rounded bg-gray-100" />
        </div>
      </div>
    </template>
  </div>
</template>
