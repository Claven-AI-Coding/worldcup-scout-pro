<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { request } from '@/utils/api'

const matches = ref<any[]>([])
const leaderboard = ref<any[]>([])
const activeTab = ref('matches')

onMounted(async () => {
  try {
    const data = await request<any>({ url: '/matches?status=upcoming&limit=10' })
    matches.value = data.items || data
  } catch (e) {
    console.error('加载失败', e)
  }
})

async function loadLeaderboard() {
  try {
    leaderboard.value = await request<any[]>({ url: '/predictions/leaderboard' })
  } catch (e) {
    console.error('加载排行榜失败', e)
  }
}

function switchTab(tab: string) {
  activeTab.value = tab
  if (tab === 'leaderboard') loadLeaderboard()
}
</script>

<template>
  <view class="container">
    <view class="tabs">
      <view :class="['tab', activeTab === 'matches' && 'tab-active']" @tap="switchTab('matches')">竞猜</view>
      <view :class="['tab', activeTab === 'leaderboard' && 'tab-active']" @tap="switchTab('leaderboard')">排行榜</view>
    </view>

    <template v-if="activeTab === 'matches'">
      <view v-for="match in matches" :key="match.id" class="match-card">
        <view class="match-info">
          <text class="team">{{ match.home_team?.name }}</text>
          <text class="vs">VS</text>
          <text class="team">{{ match.away_team?.name }}</text>
        </view>
        <view class="predict-buttons">
          <view class="btn">主胜</view>
          <view class="btn">平局</view>
          <view class="btn">客胜</view>
        </view>
      </view>
    </template>

    <template v-if="activeTab === 'leaderboard'">
      <view v-for="(entry, index) in leaderboard" :key="entry.user_id" class="rank-item">
        <text class="rank-num">{{ index + 1 }}</text>
        <text class="rank-name">{{ entry.nickname }}</text>
        <text class="rank-points">{{ entry.total_points }} 分</text>
      </view>
    </template>
  </view>
</template>

<style scoped>
.container { padding: 20rpx; }
.tabs { display: flex; margin-bottom: 20rpx; background: #f0f0f0; border-radius: 12rpx; }
.tab { flex: 1; text-align: center; padding: 16rpx; font-size: 28rpx; border-radius: 12rpx; }
.tab-active { background: #3b82f6; color: #fff; }
.match-card { background: #fff; border-radius: 12rpx; padding: 24rpx; margin-bottom: 16rpx; }
.match-info { display: flex; justify-content: center; align-items: center; gap: 20rpx; margin-bottom: 16rpx; }
.team { font-size: 30rpx; font-weight: bold; }
.vs { font-size: 24rpx; color: #999; }
.predict-buttons { display: flex; gap: 16rpx; }
.btn { flex: 1; text-align: center; padding: 12rpx; border: 2rpx solid #3b82f6; border-radius: 8rpx; color: #3b82f6; font-size: 26rpx; }
.rank-item { display: flex; align-items: center; background: #fff; border-radius: 12rpx; padding: 20rpx; margin-bottom: 10rpx; }
.rank-num { width: 60rpx; font-size: 32rpx; font-weight: bold; color: #3b82f6; }
.rank-name { flex: 1; font-size: 28rpx; }
.rank-points { font-size: 28rpx; color: #f59e0b; font-weight: bold; }
</style>
