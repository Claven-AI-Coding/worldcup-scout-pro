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
  <div class="bg-white rounded-xl p-4">
    <!-- Textarea -->
    <textarea
      v-model="content"
      class="w-full min-h-[120px] p-3 bg-gray-50 rounded-lg border border-gray-200 text-sm text-gray-700 placeholder-gray-400 resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
      placeholder="分享你的看法..."
      maxlength="1000"
    />

    <!-- Character count -->
    <div class="flex justify-end mt-1">
      <span class="text-xs text-gray-400">{{ content.length }}/1000</span>
    </div>

    <!-- Image preview grid -->
    <div
      v-if="images.length > 0"
      class="flex gap-2 mt-3 flex-wrap"
    >
      <div
        v-for="(image, index) in images"
        :key="index"
        class="relative w-20 h-20 rounded-lg overflow-hidden bg-gray-100"
      >
        <img
          :src="image"
          alt=""
          class="w-full h-full object-cover"
        >
        <button
          class="absolute top-0.5 right-0.5 w-5 h-5 bg-black/50 rounded-full flex items-center justify-center text-white"
          @click="removeImage(index)"
        >
          <svg
            class="w-3 h-3"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              d="M18 6L6 18M6 6l12 12"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Image upload area -->
    <div
      v-if="images.length < 9"
      class="mt-3 border-2 border-dashed border-gray-200 rounded-lg p-4 text-center cursor-pointer hover:border-primary-300 hover:bg-primary-50/30 transition-colors"
      @click="handleImageUpload"
    >
      <svg
        class="w-8 h-8 text-gray-300 mx-auto mb-1"
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
      <p class="text-xs text-gray-400">
        点击添加图片 (最多9张)
      </p>
    </div>

    <!-- Submit button -->
    <div class="mt-4 flex justify-end">
      <button
        class="px-6 py-2 bg-primary-500 text-white text-sm font-medium rounded-full disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary-600 transition-colors"
        :disabled="!content.trim() || submitting"
        @click="handleSubmit"
      >
        {{ submitting ? '发布中...' : '发布' }}
      </button>
    </div>
  </div>
</template>
