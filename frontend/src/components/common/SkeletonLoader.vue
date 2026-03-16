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
      <div
        v-for="i in (count || 3)"
        :key="i"
        class="bg-white rounded-xl p-4 mb-3"
      >
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 bg-gray-200 rounded-full" />
          <div class="flex-1">
            <div class="h-4 bg-gray-200 rounded w-3/4 mb-2" />
            <div class="h-3 bg-gray-100 rounded w-1/2" />
          </div>
        </div>
        <div class="h-3 bg-gray-100 rounded w-full mb-2" />
        <div class="h-3 bg-gray-100 rounded w-2/3" />
      </div>
    </template>

    <!-- 列表骨架 -->
    <template v-if="type === 'list'">
      <div
        v-for="i in (count || 5)"
        :key="i"
        class="flex items-center gap-3 py-3 border-b border-gray-50"
      >
        <div class="w-8 h-8 bg-gray-200 rounded-full flex-shrink-0" />
        <div class="flex-1">
          <div class="h-4 bg-gray-200 rounded w-2/3 mb-1" />
          <div class="h-3 bg-gray-100 rounded w-1/3" />
        </div>
        <div class="w-16 h-6 bg-gray-100 rounded" />
      </div>
    </template>

    <!-- 详情骨架 -->
    <template v-if="type === 'detail'">
      <div class="bg-white rounded-xl p-4 mb-4">
        <div class="flex justify-between items-center mb-4">
          <div class="w-16 h-16 bg-gray-200 rounded-full" />
          <div class="w-20 h-8 bg-gray-200 rounded" />
          <div class="w-16 h-16 bg-gray-200 rounded-full" />
        </div>
        <div class="h-4 bg-gray-200 rounded w-1/2 mx-auto mb-3" />
        <div class="h-3 bg-gray-100 rounded w-1/3 mx-auto" />
      </div>
      <div class="bg-white rounded-xl p-4">
        <div class="h-4 bg-gray-200 rounded w-1/4 mb-4" />
        <div class="space-y-3">
          <div class="h-3 bg-gray-100 rounded w-full" />
          <div class="h-3 bg-gray-100 rounded w-5/6" />
          <div class="h-3 bg-gray-100 rounded w-4/6" />
        </div>
      </div>
    </template>

    <!-- 网格骨架 -->
    <template v-if="type === 'grid'">
      <div class="grid grid-cols-2 gap-3">
        <div
          v-for="i in (count || 6)"
          :key="i"
          class="bg-white rounded-xl p-4"
        >
          <div class="w-10 h-10 bg-gray-200 rounded-full mb-3" />
          <div class="h-4 bg-gray-200 rounded w-3/4 mb-2" />
          <div class="h-3 bg-gray-100 rounded w-1/2" />
        </div>
      </div>
    </template>
  </div>
</template>
