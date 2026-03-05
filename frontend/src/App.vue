<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import NavBar from '@/components/common/NavBar.vue'
import TabBar from '@/components/common/TabBar.vue'
import ToastContainer from '@/components/common/ToastContainer.vue'

const route = useRoute()

// 登录页不显示导航栏和底部栏
const hideChrome = computed(() => route.name === 'login')
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <NavBar v-if="!hideChrome" />
    <main class="flex-1" :class="hideChrome ? '' : 'pb-16'">
      <RouterView />
    </main>
    <TabBar v-if="!hideChrome" />
    <ToastContainer />
  </div>
</template>
