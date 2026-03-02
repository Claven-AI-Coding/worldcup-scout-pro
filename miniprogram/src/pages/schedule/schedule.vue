<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { request } from '@/utils/api'

const matches = ref<any[]>([])
const activeStage = ref('group')
const stages = [
  { key: 'group', label: '小组赛' },
  { key: 'round_16', label: '16强' },
  { key: 'quarter', label: '8强' },
  { key: 'semi', label: '半决赛' },
  { key: 'final', label: '决赛' },
]

async function loadMatches() {
  try {
    const data = await request<any>({ url: `/matches?stage=${activeStage.value}` })
    matches.value = data.items || data
  } catch (e) {
    console.error('加载赛程失败', e)
  }
}

function switchStage(stage: string) {
  activeStage.value = stage
  loadMatches()
}

onMounted(loadMatches)
</script>

<template>
  <view class="container">
    <scroll-view scroll-x class="stage-tabs">
      <view
        v-for="s in stages"
        :key="s.key"
        :class="['tab', activeStage === s.key && 'tab-active']"
        @tap="switchStage(s.key)"
      >
        {{ s.label }}
      </view>
    </scroll-view>

    <view v-for="match in matches" :key="match.id" class="match-card">
      <view class="match-teams">
        <text class="team">{{ match.home_team?.name || '待定' }}</text>
        <view class="score">
          <text v-if="match.status === 'finished'">{{ match.home_score }} - {{ match.away_score }}</text>
          <text v-else class="vs">VS</text>
        </view>
        <text class="team">{{ match.away_team?.name || '待定' }}</text>
      </view>
      <view class="match-info">
        <text>{{ match.start_time }}</text>
        <text>{{ match.venue }}</text>
      </view>
    </view>

    <view v-if="!matches.length" class="empty">暂无赛程</view>
  </view>
</template>

<style scoped>
.container { padding: 20rpx; }
.stage-tabs { white-space: nowrap; margin-bottom: 20rpx; }
.tab { display: inline-block; padding: 12rpx 28rpx; margin-right: 12rpx; border-radius: 24rpx; background: #f0f0f0; font-size: 26rpx; }
.tab-active { background: #3b82f6; color: #fff; }
.match-card { background: #fff; border-radius: 12rpx; padding: 24rpx; margin-bottom: 16rpx; }
.match-teams { display: flex; justify-content: space-between; align-items: center; }
.team { font-size: 30rpx; font-weight: bold; flex: 1; }
.team:last-child { text-align: right; }
.score { font-size: 36rpx; font-weight: bold; color: #3b82f6; }
.vs { font-size: 28rpx; color: #999; }
.match-info { display: flex; justify-content: space-between; margin-top: 12rpx; font-size: 22rpx; color: #999; }
.empty { text-align: center; color: #999; padding: 60rpx; }
</style>
