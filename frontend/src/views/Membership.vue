<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

interface Plan {
  type: string
  label: string
  price: string
  originalPrice: string
  perMonth: string
  features: string[]
  popular?: boolean
}

const plans: Plan[] = [
  {
    type: 'monthly',
    label: '月卡',
    price: '¥18',
    originalPrice: '¥25',
    perMonth: '¥18/月',
    features: ['去广告', '无水印壁纸', 'AI 深度预测', '专属勋章'],
  },
  {
    type: 'quarterly',
    label: '季卡',
    price: '¥45',
    originalPrice: '¥75',
    perMonth: '¥15/月',
    features: ['月卡全部权益', '额外 500 积分', '世界杯限定头像框'],
    popular: true,
  },
  {
    type: 'yearly',
    label: '年卡',
    price: '¥128',
    originalPrice: '¥300',
    perMonth: '¥10.7/月',
    features: ['季卡全部权益', '额外 2000 积分', '专属称号', '优先客服'],
  },
]

const selectedPlan = ref('quarterly')

function selectPlan(type: string) {
  selectedPlan.value = type
}

const isMember = ref(userStore.user?.is_member || false)
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="mx-auto max-w-screen-lg px-4 py-4">
      <!-- 会员状态 -->
      <div class="mb-6 rounded-xl bg-gradient-to-r from-yellow-400 to-yellow-500 p-6 text-white">
        <h2 class="text-lg font-bold">球探 Pro 会员</h2>
        <p class="mt-1 text-sm text-white/80">
          {{ isMember ? '您已是会员用户' : '开通会员享受专属权益' }}
        </p>
      </div>

      <!-- 会员权益对比 -->
      <div class="mb-6 rounded-xl bg-white p-4">
        <h3 class="mb-3 text-sm font-bold text-gray-700">会员权益</h3>
        <div class="grid grid-cols-3 gap-4 text-center">
          <div>
            <div class="mb-1 text-2xl">🚫</div>
            <p class="text-xs text-gray-600">去广告</p>
          </div>
          <div>
            <div class="mb-1 text-2xl">🎨</div>
            <p class="text-xs text-gray-600">无水印壁纸</p>
          </div>
          <div>
            <div class="mb-1 text-2xl">🤖</div>
            <p class="text-xs text-gray-600">AI 深度分析</p>
          </div>
          <div>
            <div class="mb-1 text-2xl">🏅</div>
            <p class="text-xs text-gray-600">专属勋章</p>
          </div>
          <div>
            <div class="mb-1 text-2xl">💰</div>
            <p class="text-xs text-gray-600">额外积分</p>
          </div>
          <div>
            <div class="mb-1 text-2xl">👑</div>
            <p class="text-xs text-gray-600">专属称号</p>
          </div>
        </div>
      </div>

      <!-- 套餐选择 -->
      <div class="mb-6 space-y-3">
        <div
          v-for="plan in plans"
          :key="plan.type"
          class="relative cursor-pointer rounded-xl border-2 bg-white p-4 transition-all"
          :class="
            selectedPlan === plan.type
              ? 'border-green-500 shadow-md'
              : 'border-gray-100 hover:border-gray-200'
          "
          @click="selectPlan(plan.type)"
        >
          <div
            v-if="plan.popular"
            class="absolute -top-2 right-4 rounded-full bg-red-500 px-2 py-0.5 text-xs text-white"
          >
            推荐
          </div>
          <div class="flex items-center justify-between">
            <div>
              <h4 class="text-sm font-bold text-gray-800">
                {{ plan.label }}
              </h4>
              <p class="mt-0.5 text-xs text-gray-400">
                {{ plan.perMonth }}
              </p>
            </div>
            <div class="text-right">
              <span class="text-xl font-bold text-green-600">{{ plan.price }}</span>
              <span class="ml-1 text-xs text-gray-400 line-through">{{ plan.originalPrice }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 开通按钮 -->
      <button
        class="w-full rounded-xl bg-green-600 py-3 font-medium text-white transition-colors hover:bg-green-700"
      >
        立即开通
      </button>
      <p class="mt-2 text-center text-xs text-gray-400">支付功能将在 V1.1 版本上线</p>
    </div>
  </div>
</template>
