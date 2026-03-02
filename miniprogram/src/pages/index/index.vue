<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { request } from '@/utils/api'

const matches = ref<any[]>([])
const teams = ref<any[]>([])

onMounted(async () => {
  try {
    const [matchData, teamData] = await Promise.all([
      request<any>({ url: '/matches?status=upcoming&limit=5' }),
      request<any>({ url: '/teams' }),
    ])
    matches.value = matchData.items || matchData
    teams.value = teamData.items || teamData
  } catch (e) {
    console.error('加载数据失败', e)
  }
})

function goToSchedule() {
  uni.switchTab({ url: '/pages/schedule/schedule' })
}

function goToTeam(id: number) {
  uni.navigateTo({ url: `/pages/team/team?id=${id}` })
}
</script>

<template>
  <view class="container">
    <view class="hero">
      <text class="hero-title">FIFA World Cup 2026</text>
      <text class="hero-sub">球探 Pro - 你的世界杯全能助手</text>
    </view>

    <view class="section">
      <view class="section-header">
        <text class="section-title">近期赛程</text>
        <text class="section-more" @tap="goToSchedule">查看全部</text>
      </view>
      <view v-for="match in matches" :key="match.id" class="match-card">
        <text>{{ match.home_team?.name || '待定' }} vs {{ match.away_team?.name || '待定' }}</text>
        <text class="match-time">{{ match.start_time }}</text>
      </view>
      <view v-if="!matches.length" class="empty">暂无赛程</view>
    </view>

    <view class="section">
      <view class="section-header">
        <text class="section-title">参赛球队</text>
      </view>
      <view class="team-grid">
        <view v-for="team in teams.slice(0, 8)" :key="team.id" class="team-item" @tap="goToTeam(team.id)">
          <text class="team-name">{{ team.name }}</text>
          <text class="team-code">{{ team.code }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<style scoped>
.container { padding: 20rpx; }
.hero { background: linear-gradient(135deg, #1e40af, #3b82f6); border-radius: 16rpx; padding: 60rpx 30rpx; margin-bottom: 30rpx; color: #fff; text-align: center; }
.hero-title { font-size: 40rpx; font-weight: bold; display: block; }
.hero-sub { font-size: 26rpx; opacity: 0.9; margin-top: 10rpx; display: block; }
.section { margin-bottom: 30rpx; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16rpx; }
.section-title { font-size: 32rpx; font-weight: bold; }
.section-more { font-size: 24rpx; color: #3b82f6; }
.match-card { background: #fff; border-radius: 12rpx; padding: 24rpx; margin-bottom: 12rpx; }
.match-time { font-size: 22rpx; color: #999; display: block; margin-top: 8rpx; }
.team-grid { display: flex; flex-wrap: wrap; gap: 16rpx; }
.team-item { width: calc(25% - 12rpx); background: #fff; border-radius: 12rpx; padding: 20rpx; text-align: center; }
.team-name { font-size: 26rpx; display: block; }
.team-code { font-size: 22rpx; color: #999; display: block; }
.empty { text-align: center; color: #999; padding: 40rpx; }
</style>
