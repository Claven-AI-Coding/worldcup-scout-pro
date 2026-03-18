<script setup lang="ts">
import { ref } from 'vue'
import { createReport } from '@/api/reports'

const props = defineProps<{
  targetType: 'post' | 'comment' | 'user'
  targetId: number
}>()

const showModal = ref(false)
const reason = ref('')
const loading = ref(false)
const done = ref(false)
const error = ref('')

async function handleReport() {
  loading.value = true
  error.value = ''
  try {
    await createReport({
      target_type: props.targetType,
      target_id: props.targetId,
      reason: reason.value || undefined,
    })
    done.value = true
    setTimeout(() => {
      showModal.value = false
    }, 1500)
  } catch (e: unknown) {
    error.value =
      (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || '举报失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <button
      class="text-xs text-gray-400 transition-colors hover:text-red-500"
      @click.stop="showModal = true"
    >
      举报
    </button>

    <!-- 举报弹窗 -->
    <Teleport to="body">
      <div
        v-if="showModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4"
        @click.self="showModal = false"
      >
        <div class="w-full max-w-sm rounded-xl bg-white p-6">
          <h3 class="mb-3 text-sm font-bold text-gray-800">举报内容</h3>

          <div v-if="done" class="py-4 text-center">
            <div class="mb-2 text-2xl text-green-500">✓</div>
            <p class="text-sm text-gray-600">举报已提交</p>
          </div>

          <template v-else>
            <textarea
              v-model="reason"
              placeholder="请描述举报原因（可选）"
              class="h-24 w-full resize-none rounded-lg border border-gray-200 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            />

            <div class="mt-4 flex gap-2">
              <button
                class="flex-1 rounded-lg border border-gray-200 py-2 text-sm text-gray-500 hover:bg-gray-50"
                @click="showModal = false"
              >
                取消
              </button>
              <button
                class="flex-1 rounded-lg bg-red-500 py-2 text-sm text-white hover:bg-red-600 disabled:opacity-50"
                :disabled="loading"
                @click="handleReport"
              >
                {{ loading ? '提交中...' : '提交举报' }}
              </button>
            </div>

            <p v-if="error" class="mt-2 text-center text-xs text-red-500">
              {{ error }}
            </p>
          </template>
        </div>
      </div>
    </Teleport>
  </div>
</template>
