<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { request } from '@/utils/api'

const teams = ref<any[]>([])
const posts = ref<any[]>([])
const activeTeamId = ref(0)

onMounted(async () => {
  try {
    const data = await request<any>({ url: '/teams' })
    teams.value = data.items || data
    if (teams.value.length > 0) {
      activeTeamId.value = teams.value[0].id
      loadPosts()
    }
  } catch (e) {
    console.error('加载失败', e)
  }
})

async function loadPosts() {
  try {
    const data = await request<any>({ url: `/community/${activeTeamId.value}/posts` })
    posts.value = data.items || data
  } catch (e) {
    console.error('加载帖子失败', e)
  }
}

function switchTeam(id: number) {
  activeTeamId.value = id
  loadPosts()
}
</script>

<template>
  <view class="container">
    <scroll-view scroll-x class="team-tabs">
      <view
        v-for="team in teams"
        :key="team.id"
        :class="['tab', activeTeamId === team.id && 'tab-active']"
        @tap="switchTeam(team.id)"
      >
        {{ team.name }}
      </view>
    </scroll-view>

    <view v-for="post in posts" :key="post.id" class="post-card">
      <view class="post-header">
        <text class="author">{{ post.author?.nickname || '匿名' }}</text>
        <text class="time">{{ post.created_at }}</text>
      </view>
      <text class="post-content">{{ post.content }}</text>
      <view class="post-actions">
        <text>{{ post.likes }} 赞</text>
        <text>{{ post.comments_count }} 评论</text>
      </view>
    </view>

    <view v-if="!posts.length" class="empty">暂无帖子，成为第一个发帖的人吧</view>
  </view>
</template>

<style scoped>
.container { padding: 20rpx; }
.team-tabs { white-space: nowrap; margin-bottom: 20rpx; }
.tab { display: inline-block; padding: 10rpx 24rpx; margin-right: 10rpx; border-radius: 20rpx; background: #f0f0f0; font-size: 24rpx; }
.tab-active { background: #3b82f6; color: #fff; }
.post-card { background: #fff; border-radius: 12rpx; padding: 24rpx; margin-bottom: 16rpx; }
.post-header { display: flex; justify-content: space-between; margin-bottom: 12rpx; }
.author { font-weight: bold; font-size: 28rpx; }
.time { font-size: 22rpx; color: #999; }
.post-content { font-size: 28rpx; line-height: 1.6; }
.post-actions { display: flex; gap: 30rpx; margin-top: 16rpx; font-size: 24rpx; color: #666; }
.empty { text-align: center; color: #999; padding: 60rpx; }
</style>
