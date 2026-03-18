<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getHotPosts } from '@/api/community'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'

const router = useRouter()

const sections = [
  { icon: '💬', title: '球迷圈', desc: '加入球队讨论圈，和球迷一起聊', route: 'community' },
  { icon: '🎯', title: '竞猜中心', desc: '预测比赛结果，赢取积分', route: 'prediction' },
]

interface HotPost {
  id: number
  content: string
  likes: number
  comments_count: number
  author?: { username: string }
  created_at: string
}

const hotPosts = ref<HotPost[]>([])
const loading = ref(false)

async function fetchHotPosts() {
  loading.value = true
  try {
    const res = await getHotPosts({ limit: 10 })
    hotPosts.value = res.data.items || []
  } catch {
    hotPosts.value = []
  } finally {
    loading.value = false
  }
}

function goSection(routeName: string) {
  router.push({ name: routeName })
}

function formatTime(dateStr: string) {
  const d = new Date(dateStr)
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  const hours = Math.floor(diff / 3600000)
  if (hours < 1) return '刚刚'
  if (hours < 24) return `${hours}小时前`
  const days = Math.floor(hours / 24)
  if (days < 7) return `${days}天前`
  return d.toLocaleDateString()
}

onMounted(fetchHotPosts)
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="mx-auto max-w-screen-lg px-4 py-4">
      <h2 class="mb-4 text-lg font-bold text-gray-800">社交</h2>

      <!-- 功能入口 -->
      <div class="mb-6 space-y-3">
        <div
          v-for="section in sections"
          :key="section.route"
          class="flex cursor-pointer items-center gap-4 rounded-xl border border-gray-100 bg-white p-4 transition-shadow hover:shadow-md"
          @click="goSection(section.route)"
        >
          <div class="text-3xl">
            {{ section.icon }}
          </div>
          <div>
            <h3 class="text-sm font-bold text-gray-800">
              {{ section.title }}
            </h3>
            <p class="mt-0.5 text-xs text-gray-400">
              {{ section.desc }}
            </p>
          </div>
          <svg
            class="ml-auto h-5 w-5 text-gray-300"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" d="M9 5l7 7-7 7" />
          </svg>
        </div>
      </div>

      <!-- 热门帖子 -->
      <div class="rounded-xl border border-gray-100 bg-white p-4">
        <h3 class="mb-3 text-sm font-bold text-gray-700">热门讨论</h3>

        <SkeletonLoader v-if="loading" type="list" :count="3" />

        <div v-else-if="hotPosts.length > 0" class="space-y-3">
          <div
            v-for="post in hotPosts"
            :key="post.id"
            class="border-b border-gray-50 pb-3 last:border-0 last:pb-0"
          >
            <p class="line-clamp-2 text-sm text-gray-700">
              {{ post.content }}
            </p>
            <div class="mt-1.5 flex items-center gap-3 text-xs text-gray-400">
              <span v-if="post.author">{{ post.author.username }}</span>
              <span>{{ post.likes }} 赞</span>
              <span>{{ post.comments_count }} 评论</span>
              <span class="ml-auto">{{ formatTime(post.created_at) }}</span>
            </div>
          </div>
        </div>

        <p v-else class="py-6 text-center text-xs text-gray-400">
          还没有帖子，快去球迷圈发表你的观点吧！
        </p>
      </div>
    </div>
  </div>
</template>
