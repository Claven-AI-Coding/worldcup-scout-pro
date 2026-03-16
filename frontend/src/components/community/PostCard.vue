<script setup lang="ts">
import { computed } from 'vue'

interface Author {
  id: number
  nickname: string
  avatar: string | null
}

interface Post {
  id: number
  author: Author
  content: string
  images: string[]
  like_count: number
  comment_count: number
  liked: boolean
  created_at: string
}

interface Props {
  post: Post
}

const props = defineProps<Props>()

const emit = defineEmits<{
  like: [postId: number]
  comment: [postId: number]
}>()

const timeAgo = computed(() => {
  const now = Date.now()
  const created = new Date(props.post.created_at).getTime()
  const diff = now - created
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 30) return `${days}天前`
  return new Date(props.post.created_at).toLocaleDateString('zh-CN')
})

const imageGridClass = computed(() => {
  const count = props.post.images.length
  if (count === 1) return 'grid-cols-1 max-w-xs'
  if (count === 2) return 'grid-cols-2'
  return 'grid-cols-3'
})
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
    <!-- Author header -->
    <div class="flex items-center gap-3 mb-3">
      <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden flex-shrink-0">
        <img
          v-if="props.post.author.avatar"
          :src="props.post.author.avatar"
          :alt="props.post.author.nickname"
          class="w-full h-full object-cover"
        >
        <svg
          v-else
          class="w-5 h-5 text-gray-400"
          fill="currentColor"
          viewBox="0 0 24 24"
        >
          <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
        </svg>
      </div>
      <div class="min-w-0 flex-1">
        <p class="text-sm font-medium text-gray-800 truncate">
          {{ props.post.author.nickname }}
        </p>
        <p class="text-xs text-gray-400">
          {{ timeAgo }}
        </p>
      </div>
    </div>

    <!-- Content -->
    <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap mb-3">
      {{ props.post.content }}
    </p>

    <!-- Image grid -->
    <div
      v-if="props.post.images && props.post.images.length > 0"
      class="grid gap-2 mb-3"
      :class="imageGridClass"
    >
      <div
        v-for="(image, index) in props.post.images"
        :key="index"
        class="aspect-square rounded-lg bg-gray-100 overflow-hidden"
      >
        <img
          :src="image"
          alt=""
          class="w-full h-full object-cover"
        >
      </div>
    </div>

    <!-- Actions -->
    <div class="flex items-center gap-6 pt-3 border-t border-gray-50">
      <!-- Like -->
      <button
        class="flex items-center gap-1.5 text-sm transition-colors"
        :class="props.post.liked ? 'text-red-500' : 'text-gray-400 hover:text-red-400'"
        @click="emit('like', props.post.id)"
      >
        <svg
          class="w-5 h-5"
          :fill="props.post.liked ? 'currentColor' : 'none'"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"
          />
        </svg>
        <span>{{ props.post.like_count }}</span>
      </button>

      <!-- Comment -->
      <button
        class="flex items-center gap-1.5 text-sm text-gray-400 hover:text-primary-500 transition-colors"
        @click="emit('comment', props.post.id)"
      >
        <svg
          class="w-5 h-5"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2v10z"
          />
        </svg>
        <span>{{ props.post.comment_count }}</span>
      </button>
    </div>
  </div>
</template>
