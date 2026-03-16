<script setup lang="ts">
import { computed } from 'vue'

interface Author {
  id: number
  nickname: string
  avatar: string | null
}

interface Comment {
  id: number
  author: Author
  content: string
  created_at: string
}

interface Props {
  comment: Comment
}

const props = defineProps<Props>()

const timeAgo = computed(() => {
  const now = Date.now()
  const created = new Date(props.comment.created_at).getTime()
  const diff = now - created
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 30) return `${days}天前`
  return new Date(props.comment.created_at).toLocaleDateString('zh-CN')
})
</script>

<template>
  <div class="flex gap-3 py-3">
    <!-- Author avatar -->
    <div class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden flex-shrink-0">
      <img
        v-if="props.comment.author.avatar"
        :src="props.comment.author.avatar"
        :alt="props.comment.author.nickname"
        class="w-full h-full object-cover"
      >
      <svg
        v-else
        class="w-4 h-4 text-gray-400"
        fill="currentColor"
        viewBox="0 0 24 24"
      >
        <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
      </svg>
    </div>

    <!-- Content -->
    <div class="flex-1 min-w-0">
      <div class="flex items-center gap-2 mb-1">
        <span class="text-sm font-medium text-gray-700">{{ props.comment.author.nickname }}</span>
        <span class="text-xs text-gray-400">{{ timeAgo }}</span>
      </div>
      <p class="text-sm text-gray-600 leading-relaxed">
        {{ props.comment.content }}
      </p>
    </div>
  </div>
</template>
