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
    setTimeout(() => { showModal.value = false }, 1500)
  } catch (e: unknown) {
    error.value = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || '举报失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div>
    <button
      class="text-xs text-gray-400 hover:text-red-500 transition-colors"
      @click.stop="showModal = true"
    >
      举报
    </button>

    <!-- 举报弹窗 -->
    <Teleport to="body">
      <div
        v-if="showModal"
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4"
        @click.self="showModal = false"
      >
        <div class="bg-white rounded-xl p-6 w-full max-w-sm">
          <h3 class="text-sm font-bold text-gray-800 mb-3">
            举报内容
          </h3>

          <div
            v-if="done"
            class="text-center py-4"
          >
            <div class="text-green-500 text-2xl mb-2">
              ✓
            </div>
            <p class="text-sm text-gray-600">
              举报已提交
            </p>
          </div>

          <template v-else>
            <textarea
              v-model="reason"
              placeholder="请描述举报原因（可选）"
              class="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm resize-none h-24 focus:outline-none focus:ring-2 focus:ring-green-500"
            />

            <div class="flex gap-2 mt-4">
              <button
                class="flex-1 py-2 text-sm border border-gray-200 rounded-lg text-gray-500 hover:bg-gray-50"
                @click="showModal = false"
              >
                取消
              </button>
              <button
                class="flex-1 py-2 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50"
                :disabled="loading"
                @click="handleReport"
              >
                {{ loading ? '提交中...' : '提交举报' }}
              </button>
            </div>

            <p
              v-if="error"
              class="text-xs text-red-500 mt-2 text-center"
            >
              {{ error }}
            </p>
          </template>
        </div>
      </div>
    </Teleport>
  </div>
</template>
