<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const isLoginMode = ref(true)
const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function handleSubmit() {
  if (!username.value.trim() || !password.value.trim()) {
    errorMsg.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    if (isLoginMode.value) {
      await userStore.login(username.value, password.value)
    } else {
      await userStore.register(username.value, password.value)
    }
    router.push({ name: 'home' })
  } catch (err: unknown) {
    const error = err as { response?: { data?: { detail?: string } } }
    errorMsg.value = error.response?.data?.detail || (isLoginMode.value ? '登录失败，请检查用户名或密码' : '注册失败，请重试')
  } finally {
    loading.value = false
  }
}

function toggleMode() {
  isLoginMode.value = !isLoginMode.value
  errorMsg.value = ''
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-500 via-primary-600 to-blue-600 flex items-center justify-center px-4">
    <div class="w-full max-w-sm">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="w-20 h-20 mx-auto rounded-2xl bg-white/20 backdrop-blur-sm flex items-center justify-center mb-4">
          <svg class="w-12 h-12 text-white" viewBox="0 0 24 24" fill="currentColor">
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" fill="none" />
            <path d="M12 2 C14 6 18 8 22 12 C18 16 14 18 12 22 C10 18 6 16 2 12 C6 8 10 6 12 2Z" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold text-white">球探 Pro</h1>
        <p class="text-primary-200 text-sm mt-1">世界杯全能助手</p>
      </div>

      <!-- Form card -->
      <div class="bg-white rounded-2xl shadow-xl p-6">
        <h2 class="text-lg font-bold text-gray-800 text-center mb-6">
          {{ isLoginMode ? '登录' : '注册' }}
        </h2>

        <!-- Error message -->
        <div
          v-if="errorMsg"
          class="mb-4 px-3 py-2 bg-red-50 border border-red-200 rounded-lg text-sm text-red-600"
        >
          {{ errorMsg }}
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Username -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
            <div class="relative">
              <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                <circle cx="12" cy="8" r="4" />
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2" />
              </svg>
              <input
                v-model="username"
                type="text"
                class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                placeholder="请输入用户名"
                autocomplete="username"
              />
            </div>
          </div>

          <!-- Password -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
            <div class="relative">
              <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                <rect x="3" y="11" width="18" height="11" rx="2" />
                <path d="M7 11V7a5 5 0 0110 0v4" />
              </svg>
              <input
                v-model="password"
                type="password"
                class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                placeholder="请输入密码"
                autocomplete="current-password"
              />
            </div>
          </div>

          <!-- Submit button -->
          <button
            type="submit"
            class="w-full py-2.5 bg-primary-500 text-white text-sm font-bold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-primary-600 transition-colors flex items-center justify-center gap-2"
            :disabled="loading"
          >
            <div v-if="loading" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            {{ isLoginMode ? '登录' : '注册' }}
          </button>
        </form>

        <!-- Toggle mode -->
        <div class="mt-4 text-center">
          <button
            class="text-sm text-primary-500 hover:text-primary-600 transition-colors"
            @click="toggleMode"
          >
            {{ isLoginMode ? '没有账号？点击注册' : '已有账号？点击登录' }}
          </button>
        </div>

        <!-- Divider -->
        <div class="flex items-center gap-3 my-5">
          <div class="flex-1 h-px bg-gray-200"></div>
          <span class="text-xs text-gray-400">其他登录方式</span>
          <div class="flex-1 h-px bg-gray-200"></div>
        </div>

        <!-- WeChat login placeholder -->
        <button
          class="w-full flex items-center justify-center gap-2 py-2.5 bg-[#07C160] text-white text-sm font-medium rounded-lg hover:bg-[#06AD56] transition-colors"
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 01.213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 00.167-.054l1.903-1.114a.864.864 0 01.717-.098 10.16 10.16 0 002.837.403c.276 0 .543-.027.811-.05-.857-2.578.157-4.972 1.932-6.446 1.703-1.415 3.882-1.98 5.853-1.838-.576-3.583-4.196-6.348-8.596-6.348zM5.785 5.991c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 01-1.162 1.178A1.17 1.17 0 014.623 7.17c0-.651.52-1.18 1.162-1.18zm5.813 0c.642 0 1.162.529 1.162 1.18a1.17 1.17 0 01-1.162 1.178 1.17 1.17 0 01-1.162-1.178c0-.651.52-1.18 1.162-1.18zm5.34 2.867c-1.797-.052-3.746.512-5.28 1.786-1.72 1.428-2.687 3.72-1.78 6.22.942 2.453 3.666 4.229 6.884 4.229.826 0 1.622-.12 2.361-.336a.722.722 0 01.598.082l1.584.926a.272.272 0 00.14.045c.134 0 .24-.11.24-.245 0-.06-.024-.12-.04-.178L21.32 20.2a.49.49 0 01.177-.554C23.063 18.456 24 16.826 24 14.994c0-3.36-3.065-6.136-7.062-6.136zM14.5 13.171c.535 0 .969.44.969.982a.976.976 0 01-.969.983.976.976 0 01-.969-.983c0-.542.434-.982.97-.982zm4.844 0c.535 0 .969.44.969.982a.976.976 0 01-.969.983.976.976 0 01-.969-.983c0-.542.434-.982.969-.982z" />
          </svg>
          微信登录
        </button>
      </div>
    </div>
  </div>
</template>
