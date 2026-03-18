<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  submit: [data: { content: string; images: string[] }]
}>()

const content = ref('')
const images = ref<string[]>([])
const submitting = ref(false)

function handleImageUpload() {
  // Placeholder: in a real app, this would open a file picker and upload images
  // For now, we just show the upload area
}

function removeImage(index: number) {
  images.value.splice(index, 1)
}

async function handleSubmit() {
  if (!content.value.trim()) return
  submitting.value = true
  try {
    emit('submit', {
      content: content.value.trim(),
      images: images.value,
    })
    content.value = ''
    images.value = []
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="rounded-xl bg-white p-4">
    <!-- Textarea -->
    <textarea
      v-model="content"
      class="min-h-[120px] w-full resize-none rounded-lg border border-gray-200 bg-gray-50 p-3 text-sm text-gray-700 placeholder-gray-400 transition-all focus:border-transparent focus:outline-none focus:ring-2 focus:ring-primary-500"
      placeholder="分享你的看法..."
      maxlength="1000"
    />

    <!-- Character count -->
    <div class="mt-1 flex justify-end">
      <span class="text-xs text-gray-400">{{ content.length }}/1000</span>
    </div>

    <!-- Image preview grid -->
    <div v-if="images.length > 0" class="mt-3 flex flex-wrap gap-2">
      <div
        v-for="(image, index) in images"
        :key="index"
        class="relative h-20 w-20 overflow-hidden rounded-lg bg-gray-100"
      >
        <img :src="image" alt="" class="h-full w-full object-cover" />
        <button
          class="absolute right-0.5 top-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-black/50 text-white"
          @click="removeImage(index)"
        >
          <svg
            class="h-3 w-3"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" d="M18 6L6 18M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Image upload area -->
    <div
      v-if="images.length < 9"
      class="mt-3 cursor-pointer rounded-lg border-2 border-dashed border-gray-200 p-4 text-center transition-colors hover:border-primary-300 hover:bg-primary-50/30"
      @click="handleImageUpload"
    >
      <svg
        class="mx-auto mb-1 h-8 w-8 text-gray-300"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909M3.75 21h16.5A2.25 2.25 0 0022.5 18.75V5.25A2.25 2.25 0 0020.25 3H3.75A2.25 2.25 0 001.5 5.25v13.5A2.25 2.25 0 003.75 21z"
        />
      </svg>
      <p class="text-xs text-gray-400">点击添加图片 (最多9张)</p>
    </div>

    <!-- Submit button -->
    <div class="mt-4 flex justify-end">
      <button
        class="rounded-full bg-primary-500 px-6 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-600 disabled:cursor-not-allowed disabled:opacity-50"
        :disabled="!content.trim() || submitting"
        @click="handleSubmit"
      >
        {{ submitting ? '发布中...' : '发布' }}
      </button>
    </div>
  </div>
</template>
