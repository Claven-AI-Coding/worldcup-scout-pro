<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useTeamStore } from '@/stores/teams'
import { getPosts, createPost, likePost } from '@/api/community'
import PostCard from '@/components/community/PostCard.vue'
import PostForm from '@/components/community/PostForm.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const route = useRoute()
const teamStore = useTeamStore()

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

const selectedTeamId = ref<number | null>(null)
const posts = ref<Post[]>([])
const loading = ref(false)
const showPostForm = ref(false)

onMounted(() => {
  teamStore.fetchTeams()
  // Check if teamId is passed via query
  if (route.query.teamId) {
    selectedTeamId.value = Number(route.query.teamId)
  }
})

const selectedTeam = computed(() => {
  if (!selectedTeamId.value) return null
  return teamStore.teams.find(t => t.id === selectedTeamId.value) || null
})

async function loadPosts() {
  if (!selectedTeamId.value) return
  loading.value = true
  try {
    const res = await getPosts(selectedTeamId.value)
    posts.value = (res.data.items || res.data) as Post[]
  } catch {
    posts.value = []
  } finally {
    loading.value = false
  }
}

watch(selectedTeamId, () => {
  if (selectedTeamId.value) {
    loadPosts()
  } else {
    posts.value = []
  }
})

// Load posts if team is already selected on mount
watch(
  () => teamStore.teams,
  teams => {
    if (teams.length > 0 && selectedTeamId.value) {
      loadPosts()
    } else if (teams.length > 0 && !selectedTeamId.value) {
      selectedTeamId.value = teams[0].id
    }
  },
  { once: true }
)

function selectTeam(teamId: number) {
  selectedTeamId.value = teamId
}

async function handleLike(postId: number) {
  try {
    await likePost(postId)
    const post = posts.value.find(p => p.id === postId)
    if (post) {
      post.liked = !post.liked
      post.like_count += post.liked ? 1 : -1
    }
  } catch {
    // ignore
  }
}

function handleComment(postId: number) {
  // Placeholder: navigate to post detail or open comment modal
  console.log('Comment on post:', postId)
}

async function handleSubmitPost(data: { content: string; images: string[] }) {
  if (!selectedTeamId.value) return
  try {
    await createPost({
      team_id: selectedTeamId.value,
      content: data.content,
      images: data.images.length > 0 ? data.images : undefined,
    })
    showPostForm.value = false
    loadPosts()
  } catch {
    // ignore
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="mx-auto max-w-screen-lg">
      <!-- Team circle selector -->
      <div class="sticky top-14 z-40 border-b border-gray-100 bg-white">
        <div class="scrollbar-hide flex gap-4 overflow-x-auto px-4 py-3">
          <button
            v-for="team in teamStore.teams"
            :key="team.id"
            class="group flex flex-shrink-0 flex-col items-center gap-1"
            @click="selectTeam(team.id)"
          >
            <div
              class="flex h-12 w-12 items-center justify-center overflow-hidden rounded-full border-2 transition-all"
              :class="
                selectedTeamId === team.id
                  ? 'border-primary-500 shadow-md'
                  : 'border-transparent group-hover:border-gray-200'
              "
            >
              <img
                v-if="team.flag_url"
                :src="team.flag_url"
                :alt="team.name"
                class="h-full w-full object-cover"
              />
              <span
                v-else
                class="flex h-full w-full items-center justify-center bg-gray-100 text-xs font-bold text-gray-400"
              >
                {{ team.code }}
              </span>
            </div>
            <span
              class="max-w-[48px] truncate text-xs transition-colors"
              :class="selectedTeamId === team.id ? 'font-medium text-primary-600' : 'text-gray-500'"
            >
              {{ team.name }}
            </span>
          </button>
        </div>
      </div>

      <div class="px-4 py-4">
        <!-- Selected team header -->
        <div v-if="selectedTeam" class="mb-4">
          <h2 class="text-lg font-bold text-gray-800">{{ selectedTeam.name }} 球迷圈</h2>
        </div>

        <!-- Posts feed -->
        <LoadingSpinner v-if="loading" text="加载中..." />

        <div v-else-if="posts.length > 0" class="space-y-3">
          <PostCard
            v-for="post in posts"
            :key="post.id"
            :post="post"
            @like="handleLike"
            @comment="handleComment"
          />
        </div>

        <EmptyState
          v-else-if="selectedTeamId"
          message="暂无帖子，来发第一条吧"
          action-text="发布帖子"
          @action="showPostForm = true"
        />

        <EmptyState v-else message="请选择一支球队" />
      </div>
    </div>

    <!-- Floating create button -->
    <button
      v-if="selectedTeamId && !showPostForm"
      class="fixed bottom-20 right-4 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-primary-500 text-white shadow-lg transition-all hover:bg-primary-600 active:scale-95"
      @click="showPostForm = true"
    >
      <svg class="h-7 w-7" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" d="M12 5v14m-7-7h14" />
      </svg>
    </button>

    <!-- Post form modal -->
    <Teleport to="body">
      <div
        v-if="showPostForm"
        class="fixed inset-0 z-50 flex items-end justify-center sm:items-center"
      >
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40" @click="showPostForm = false" />

        <!-- Modal content -->
        <div
          class="relative mx-0 max-h-[80vh] w-full max-w-lg overflow-y-auto rounded-t-2xl bg-white sm:mx-4 sm:rounded-2xl"
        >
          <!-- Modal header -->
          <div class="flex items-center justify-between border-b border-gray-100 px-4 py-3">
            <h3 class="text-base font-bold text-gray-800">发布帖子</h3>
            <button
              class="flex h-8 w-8 items-center justify-center rounded-full transition-colors hover:bg-gray-100"
              @click="showPostForm = false"
            >
              <svg
                class="h-5 w-5 text-gray-500"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" d="M18 6L6 18M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div class="p-4">
            <PostForm @submit="handleSubmitPost" />
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
