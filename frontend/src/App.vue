<script setup lang="ts">
import { RouterView } from 'vue-router'
import NavBar from '@/components/common/NavBar.vue'
import TabBar from '@/components/common/TabBar.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <NavBar />
    <main class="flex-1 pb-16">
      <RouterView />
    </main>
    <TabBar />
  </div>
</template>
