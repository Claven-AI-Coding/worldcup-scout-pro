<script setup lang="ts">
import { computed } from 'vue'

interface Wallpaper {
  id: number
  image_url: string
  style: string
  team_name: string | null
  player_name: string | null
  created_at: string
}

interface Props {
  wallpaper: Wallpaper
}

const props = defineProps<Props>()

const styleLabelMap: Record<string, string> = {
  cyberpunk: '赛博朋克',
  ink: '水墨',
  comic: '漫画',
  minimal: '极简',
}

const styleBadgeClass: Record<string, string> = {
  cyberpunk: 'bg-purple-100 text-purple-600',
  ink: 'bg-gray-100 text-gray-600',
  comic: 'bg-yellow-100 text-yellow-700',
  minimal: 'bg-slate-100 text-slate-600',
}

const styleLabel = computed(() => styleLabelMap[props.wallpaper.style] || props.wallpaper.style)
const badgeClass = computed(() => styleBadgeClass[props.wallpaper.style] || 'bg-gray-100 text-gray-600')

const displayName = computed(() => {
  return props.wallpaper.player_name || props.wallpaper.team_name || ''
})

function handleDownload() {
  const link = document.createElement('a')
  link.href = props.wallpaper.image_url
  link.download = `wallpaper-${props.wallpaper.id}.jpg`
  link.target = '_blank'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>

<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden group">
    <!-- Image -->
    <div class="relative aspect-[9/16] bg-gray-100 overflow-hidden">
      <img
        :src="props.wallpaper.image_url"
        :alt="displayName"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
      >

      <!-- Style badge -->
      <span
        class="absolute top-2 left-2 text-xs font-medium px-2 py-0.5 rounded-full backdrop-blur-sm"
        :class="badgeClass"
      >
        {{ styleLabel }}
      </span>

      <!-- Download overlay -->
      <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-end justify-center pb-4 opacity-0 group-hover:opacity-100">
        <button
          class="flex items-center gap-1.5 px-4 py-2 bg-white/90 backdrop-blur-sm text-gray-800 text-sm font-medium rounded-full shadow-lg hover:bg-white transition-colors"
          @click.stop="handleDownload"
        >
          <svg
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
            />
          </svg>
          下载
        </button>
      </div>
    </div>

    <!-- Info -->
    <div class="p-3">
      <p
        v-if="displayName"
        class="text-sm font-medium text-gray-700 truncate"
      >
        {{ displayName }}
      </p>
    </div>
  </div>
</template>
