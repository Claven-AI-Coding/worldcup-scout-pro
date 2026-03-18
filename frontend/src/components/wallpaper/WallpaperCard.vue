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
const badgeClass = computed(
  () => styleBadgeClass[props.wallpaper.style] || 'bg-gray-100 text-gray-600'
)

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
  <div class="group overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm">
    <!-- Image -->
    <div class="relative aspect-[9/16] overflow-hidden bg-gray-100">
      <img
        :src="props.wallpaper.image_url"
        :alt="displayName"
        class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
      />

      <!-- Style badge -->
      <span
        class="absolute left-2 top-2 rounded-full px-2 py-0.5 text-xs font-medium backdrop-blur-sm"
        :class="badgeClass"
      >
        {{ styleLabel }}
      </span>

      <!-- Download overlay -->
      <div
        class="absolute inset-0 flex items-end justify-center bg-black/0 pb-4 opacity-0 transition-colors group-hover:bg-black/20 group-hover:opacity-100"
      >
        <button
          class="flex items-center gap-1.5 rounded-full bg-white/90 px-4 py-2 text-sm font-medium text-gray-800 shadow-lg backdrop-blur-sm transition-colors hover:bg-white"
          @click.stop="handleDownload"
        >
          <svg
            class="h-4 w-4"
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
      <p v-if="displayName" class="truncate text-sm font-medium text-gray-700">
        {{ displayName }}
      </p>
    </div>
  </div>
</template>
