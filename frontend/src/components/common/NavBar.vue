<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

function goSearch() {
  // placeholder for search navigation
}

function goProfile() {
  if (userStore.isLoggedIn) {
    router.push({ name: 'profile' })
  } else {
    router.push({ name: 'login' })
  }
}
</script>

<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-white shadow-sm">
    <div class="flex items-center justify-between h-14 px-4 max-w-screen-lg mx-auto">
      <!-- Logo -->
      <router-link
        to="/"
        class="flex items-center gap-2"
      >
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-red-500 to-yellow-400 flex items-center justify-center">
          <svg
            class="w-5 h-5 text-white"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <circle
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="2"
              fill="none"
            />
            <path d="M12 2 C14 6 18 8 22 12 C18 16 14 18 12 22 C10 18 6 16 2 12 C6 8 10 6 12 2Z" />
          </svg>
        </div>
        <span class="text-lg font-bold text-gray-800">球探 Pro</span>
      </router-link>

      <!-- Right actions -->
      <div class="flex items-center gap-3">
        <!-- Search -->
        <button
          class="w-9 h-9 flex items-center justify-center rounded-full hover:bg-gray-100 transition-colors"
          @click="goSearch"
        >
          <svg
            class="w-5 h-5 text-gray-600"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <circle
              cx="11"
              cy="11"
              r="8"
            />
            <path
              d="m21 21-4.35-4.35"
              stroke-linecap="round"
            />
          </svg>
        </button>

        <!-- User avatar -->
        <button
          class="w-8 h-8 rounded-full overflow-hidden bg-gray-200 flex items-center justify-center hover:ring-2 hover:ring-primary-300 transition-all"
          @click="goProfile"
        >
          <img
            v-if="userStore.user?.avatar"
            :src="userStore.user.avatar"
            alt="avatar"
            class="w-full h-full object-cover"
          >
          <svg
            v-else
            class="w-5 h-5 text-gray-400"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
          </svg>
        </button>
      </div>
    </div>
  </header>
  <!-- Spacer for fixed header -->
  <div class="h-14" />
</template>
