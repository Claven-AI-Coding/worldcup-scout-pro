<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { request } from '@/utils/api'

const team = ref<any>(null)
const players = ref<any[]>([])
const teamId = ref(0)

onLoad((query) => {
  teamId.value = Number(query?.id || 0)
})

onMounted(async () => {
  if (!teamId.value) return
  try {
    const [teamData, playerData] = await Promise.all([
      request<any>({ url: `/teams/${teamId.value}` }),
      request<any>({ url: `/teams/${teamId.value}/players` }),
    ])
    team.value = teamData
    players.value = playerData.items || playerData
  } catch (e) {
    console.error('加载球队数据失败', e)
  }
})
</script>

<template>
  <view class="container" v-if="team">
    <view class="team-header">
      <text class="team-name">{{ team.name }}</text>
      <text class="team-en">{{ team.name_en }}</text>
      <text class="team-group">{{ team.group_name }}组</text>
      <text class="team-coach">教练: {{ team.coach }}</text>
    </view>

    <view class="section">
      <text class="section-title">球员阵容</text>
      <view v-for="player in players" :key="player.id" class="player-card">
        <view class="player-num">{{ player.number }}</view>
        <view class="player-info">
          <text class="player-name">{{ player.name }}</text>
          <text class="player-detail">{{ player.position }} | {{ player.club }}</text>
        </view>
      </view>
      <view v-if="!players.length" class="empty">暂无球员数据</view>
    </view>
  </view>
</template>

<style scoped>
.container { padding: 20rpx; }
.team-header { background: linear-gradient(135deg, #1e40af, #3b82f6); border-radius: 16rpx; padding: 40rpx; color: #fff; margin-bottom: 20rpx; }
.team-name { font-size: 44rpx; font-weight: bold; display: block; }
.team-en { font-size: 26rpx; opacity: 0.8; display: block; margin-top: 4rpx; }
.team-group { display: inline-block; background: rgba(255,255,255,0.2); padding: 4rpx 16rpx; border-radius: 8rpx; font-size: 22rpx; margin-top: 12rpx; }
.team-coach { display: block; margin-top: 12rpx; font-size: 26rpx; }
.section { margin-bottom: 20rpx; }
.section-title { font-size: 32rpx; font-weight: bold; margin-bottom: 16rpx; display: block; }
.player-card { display: flex; align-items: center; background: #fff; border-radius: 12rpx; padding: 20rpx; margin-bottom: 10rpx; }
.player-num { width: 60rpx; height: 60rpx; border-radius: 50%; background: #3b82f6; color: #fff; font-size: 28rpx; font-weight: bold; display: flex; align-items: center; justify-content: center; margin-right: 20rpx; line-height: 60rpx; text-align: center; }
.player-info { flex: 1; }
.player-name { font-size: 28rpx; font-weight: bold; display: block; }
.player-detail { font-size: 22rpx; color: #999; display: block; margin-top: 4rpx; }
.empty { text-align: center; color: #999; padding: 40rpx; }
</style>
