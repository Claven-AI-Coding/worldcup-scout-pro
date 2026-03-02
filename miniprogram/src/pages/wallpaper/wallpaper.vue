<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { request } from '@/utils/api'

const teams = ref<any[]>([])
const selectedTeam = ref(0)
const selectedStyle = ref('cyberpunk')
const generating = ref(false)
const result = ref<any>(null)

const styles = [
  { key: 'cyberpunk', label: '赛博朋克' },
  { key: 'ink', label: '水墨' },
  { key: 'comic', label: '漫画' },
  { key: 'minimal', label: '极简' },
]

onMounted(async () => {
  try {
    const data = await request<any>({ url: '/teams' })
    teams.value = data.items || data
  } catch (e) {
    console.error('加载失败', e)
  }
})

async function generate() {
  if (!selectedTeam.value) {
    uni.showToast({ title: '请选择球队', icon: 'none' })
    return
  }
  generating.value = true
  try {
    result.value = await request<any>({
      url: '/wallpapers/generate',
      method: 'POST',
      data: { team_id: selectedTeam.value, style: selectedStyle.value },
    })
    uni.showToast({ title: '生成中，请稍候' })
  } catch (e: any) {
    uni.showToast({ title: e.message || '生成失败', icon: 'error' })
  } finally {
    generating.value = false
  }
}
</script>

<template>
  <view class="container">
    <view class="section">
      <text class="section-title">选择球队</text>
      <picker mode="selector" :range="teams" range-key="name" @change="(e: any) => selectedTeam = teams[e.detail.value]?.id">
        <view class="picker">{{ teams.find(t => t.id === selectedTeam)?.name || '请选择球队' }}</view>
      </picker>
    </view>

    <view class="section">
      <text class="section-title">选择风格</text>
      <view class="style-grid">
        <view
          v-for="s in styles"
          :key="s.key"
          :class="['style-card', selectedStyle === s.key && 'style-active']"
          @tap="selectedStyle = s.key"
        >
          {{ s.label }}
        </view>
      </view>
    </view>

    <view class="generate-btn" :class="{ disabled: generating }" @tap="generate">
      {{ generating ? '生成中...' : '生成壁纸' }}
    </view>

    <view v-if="result?.image_url" class="result">
      <image :src="result.image_url" mode="widthFix" class="wallpaper-img" />
    </view>
  </view>
</template>

<style scoped>
.container { padding: 20rpx; }
.section { margin-bottom: 30rpx; }
.section-title { font-size: 30rpx; font-weight: bold; margin-bottom: 16rpx; display: block; }
.picker { background: #fff; padding: 20rpx; border-radius: 12rpx; font-size: 28rpx; color: #333; }
.style-grid { display: flex; gap: 16rpx; }
.style-card { flex: 1; text-align: center; padding: 24rpx 12rpx; background: #fff; border-radius: 12rpx; font-size: 26rpx; border: 2rpx solid transparent; }
.style-active { border-color: #3b82f6; color: #3b82f6; background: #eff6ff; }
.generate-btn { background: #3b82f6; color: #fff; text-align: center; padding: 24rpx; border-radius: 12rpx; font-size: 32rpx; font-weight: bold; }
.generate-btn.disabled { opacity: 0.6; }
.result { margin-top: 20rpx; }
.wallpaper-img { width: 100%; border-radius: 12rpx; }
</style>
