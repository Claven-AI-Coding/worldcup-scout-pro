<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTeamStore } from '@/stores/teams'
import { searchPlayers } from '@/api/players'
import { generateWallpaper, getGallery } from '@/api/wallpapers'
import StyleSelector from '@/components/wallpaper/StyleSelector.vue'
import WallpaperCard from '@/components/wallpaper/WallpaperCard.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const teamStore = useTeamStore()

// Selection state
const selectedTeamId = ref<number | undefined>(undefined)
const selectedPlayerId = ref<number | undefined>(undefined)
const selectedStyle = ref('cyberpunk')

// Player list
interface Player {
  id: number
  name: string
  team_id: number
  number: number | null
  position: string | null
}

const players = ref<Player[]>([])
const playersLoading = ref(false)

// Generation state
const generating = ref(false)
const generationStatus = ref('')

// Gallery
interface Wallpaper {
  id: number
  image_url: string
  style: string
  team_name: string | null
  player_name: string | null
  created_at: string
}

const gallery = ref<Wallpaper[]>([])
const galleryLoading = ref(false)

onMounted(() => {
  teamStore.fetchTeams()
  loadGallery()
})

async function onTeamChange() {
  selectedPlayerId.value = undefined
  players.value = []
  if (selectedTeamId.value) {
    playersLoading.value = true
    try {
      const res = await searchPlayers({ team_id: selectedTeamId.value })
      players.value = (res.data.items || res.data) as Player[]
    } catch {
      players.value = []
    } finally {
      playersLoading.value = false
    }
  }
}

async function loadGallery() {
  galleryLoading.value = true
  try {
    const res = await getGallery()
    gallery.value = (res.data.items || res.data) as Wallpaper[]
  } catch {
    gallery.value = []
  } finally {
    galleryLoading.value = false
  }
}

async function handleGenerate() {
  if (!selectedTeamId.value && !selectedPlayerId.value) return

  generating.value = true
  generationStatus.value = '正在生成壁纸，请稍候...'

  try {
    const data: { team_id?: number; player_id?: number; style: string } = {
      style: selectedStyle.value,
    }
    if (selectedTeamId.value) data.team_id = selectedTeamId.value
    if (selectedPlayerId.value) data.player_id = selectedPlayerId.value

    await generateWallpaper(data)
    generationStatus.value = '壁纸生成成功!'
    loadGallery()
  } catch {
    generationStatus.value = '生成失败，请重试'
  } finally {
    generating.value = false
    setTimeout(() => {
      generationStatus.value = ''
    }, 3000)
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-screen-lg mx-auto px-4 py-6 space-y-6">
      <!-- Header -->
      <div>
        <h1 class="text-xl font-bold text-gray-800">
          AI 壁纸生成
        </h1>
        <p class="text-sm text-gray-400 mt-1">
          选择球队或球员，生成专属世界杯壁纸
        </p>
      </div>

      <!-- Selection section -->
      <section class="bg-white rounded-xl shadow-sm border border-gray-100 p-4 space-y-4">
        <!-- Team selector -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">选择球队</label>
          <select
            v-model="selectedTeamId"
            class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent appearance-none"
            @change="onTeamChange"
          >
            <option :value="undefined">
              请选择球队
            </option>
            <option
              v-for="team in teamStore.teams"
              :key="team.id"
              :value="team.id"
            >
              {{ team.name }} ({{ team.code }})
            </option>
          </select>
        </div>

        <!-- Player selector -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1.5">选择球员 (可选)</label>
          <select
            v-model="selectedPlayerId"
            class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent appearance-none disabled:opacity-50"
            :disabled="!selectedTeamId || playersLoading"
          >
            <option :value="undefined">
              不指定球员
            </option>
            <option
              v-for="player in players"
              :key="player.id"
              :value="player.id"
            >
              {{ player.name }}{{ player.number ? ` #${player.number}` : '' }}
            </option>
          </select>
          <p
            v-if="playersLoading"
            class="text-xs text-gray-400 mt-1"
          >
            加载球员列表中...
          </p>
        </div>

        <!-- Style selector -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">选择风格</label>
          <StyleSelector v-model="selectedStyle" />
        </div>

        <!-- Generate button -->
        <button
          class="w-full py-3 bg-gradient-to-r from-primary-500 to-purple-500 text-white text-sm font-bold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:from-primary-600 hover:to-purple-600 transition-all flex items-center justify-center gap-2"
          :disabled="(!selectedTeamId && !selectedPlayerId) || generating"
          @click="handleGenerate"
        >
          <svg
            v-if="!generating"
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"
            />
          </svg>
          <div
            v-else
            class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"
          />
          {{ generating ? '生成中...' : '生成壁纸' }}
        </button>

        <!-- Generation status -->
        <p
          v-if="generationStatus"
          class="text-sm text-center font-medium"
          :class="generationStatus.includes('失败') ? 'text-red-500' : 'text-green-600'"
        >
          {{ generationStatus }}
        </p>
      </section>

      <!-- Gallery -->
      <section>
        <h2 class="text-lg font-bold text-gray-800 mb-3">
          壁纸画廊
        </h2>

        <LoadingSpinner
          v-if="galleryLoading"
          text="加载壁纸画廊..."
        />

        <div
          v-else-if="gallery.length > 0"
          class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3"
        >
          <WallpaperCard
            v-for="wallpaper in gallery"
            :key="wallpaper.id"
            :wallpaper="wallpaper"
          />
        </div>

        <EmptyState
          v-else
          message="暂无壁纸，快来生成第一张吧"
        />
      </section>
    </div>
  </div>
</template>
