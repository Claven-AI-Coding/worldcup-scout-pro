<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { request, wxLogin } from '@/utils/api'

const user = ref<any>(null)
const isLoggedIn = ref(false)

onMounted(async () => {
  const token = uni.getStorageSync('token')
  if (token) {
    try {
      user.value = await request<any>({ url: '/auth/me' })
      isLoggedIn.value = true
    } catch {
      isLoggedIn.value = false
    }
  }
})

async function handleLogin() {
  try {
    await wxLogin()
    user.value = await request<any>({ url: '/auth/me' })
    isLoggedIn.value = true
    uni.showToast({ title: '登录成功' })
  } catch (e) {
    uni.showToast({ title: '登录失败', icon: 'error' })
  }
}

function handleLogout() {
  uni.removeStorageSync('token')
  user.value = null
  isLoggedIn.value = false
  uni.showToast({ title: '已退出登录' })
}
</script>

<template>
  <view class="container">
    <view v-if="isLoggedIn && user" class="profile-card">
      <view class="avatar-wrap">
        <image v-if="user.avatar" :src="user.avatar" class="avatar" />
        <view v-else class="avatar-placeholder">{{ user.nickname?.[0] || '球' }}</view>
      </view>
      <text class="nickname">{{ user.nickname }}</text>
      <text v-if="user.title" class="title-badge">{{ user.title }}</text>
      <view class="stats">
        <view class="stat">
          <text class="stat-num">{{ user.points }}</text>
          <text class="stat-label">积分</text>
        </view>
        <view class="stat">
          <text class="stat-num">{{ user.win_streak }}</text>
          <text class="stat-label">连胜</text>
        </view>
      </view>
    </view>

    <view v-else class="login-card">
      <text class="login-text">登录后享受完整功能</text>
      <view class="login-btn" @tap="handleLogin">微信一键登录</view>
    </view>

    <view v-if="isLoggedIn" class="menu">
      <view class="menu-item" @tap="() => uni.navigateTo({ url: '/pages/wallpaper/wallpaper' })">
        <text>AI壁纸</text>
        <text class="arrow">></text>
      </view>
      <view class="menu-item" @tap="handleLogout">
        <text style="color: #ef4444">退出登录</text>
        <text class="arrow">></text>
      </view>
    </view>
  </view>
</template>

<style scoped>
.container { padding: 20rpx; }
.profile-card { background: linear-gradient(135deg, #1e40af, #3b82f6); border-radius: 16rpx; padding: 40rpx; color: #fff; text-align: center; margin-bottom: 20rpx; }
.avatar-wrap { margin-bottom: 16rpx; }
.avatar { width: 120rpx; height: 120rpx; border-radius: 50%; }
.avatar-placeholder { width: 120rpx; height: 120rpx; border-radius: 50%; background: rgba(255,255,255,0.3); display: inline-flex; align-items: center; justify-content: center; font-size: 48rpx; margin: 0 auto; line-height: 120rpx; }
.nickname { font-size: 36rpx; font-weight: bold; display: block; }
.title-badge { display: inline-block; background: #f59e0b; padding: 4rpx 16rpx; border-radius: 12rpx; font-size: 22rpx; margin-top: 8rpx; }
.stats { display: flex; justify-content: center; gap: 80rpx; margin-top: 24rpx; }
.stat { text-align: center; }
.stat-num { font-size: 40rpx; font-weight: bold; display: block; }
.stat-label { font-size: 22rpx; opacity: 0.8; }
.login-card { background: #fff; border-radius: 16rpx; padding: 60rpx; text-align: center; margin-bottom: 20rpx; }
.login-text { font-size: 28rpx; color: #666; display: block; margin-bottom: 24rpx; }
.login-btn { background: #07c160; color: #fff; padding: 20rpx; border-radius: 12rpx; font-size: 30rpx; }
.menu { background: #fff; border-radius: 12rpx; overflow: hidden; }
.menu-item { display: flex; justify-content: space-between; align-items: center; padding: 28rpx 24rpx; border-bottom: 1rpx solid #f0f0f0; font-size: 28rpx; }
.arrow { color: #ccc; }
</style>
