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
    <div class="max-w-screen-lg mx-auto px-4 py-4">
      <!-- 会员状态 -->
      <div class="bg-gradient-to-r from-yellow-400 to-yellow-500 rounded-xl p-6 text-white mb-6">
        <h2 class="text-lg font-bold">
          球探 Pro 会员
        </h2>
        <p class="text-sm text-white/80 mt-1">
          {{ isMember ? '您已是会员用户' : '开通会员享受专属权益' }}
        </p>
      </div>

      <!-- 会员权益对比 -->
      <div class="bg-white rounded-xl p-4 mb-6">
        <h3 class="text-sm font-bold text-gray-700 mb-3">
          会员权益
        </h3>
        <div class="grid grid-cols-3 gap-4 text-center">
          <div>
            <div class="text-2xl mb-1">
              🚫
            </div>
            <p class="text-xs text-gray-600">
              去广告
            </p>
          </div>
          <div>
            <div class="text-2xl mb-1">
              🎨
            </div>
            <p class="text-xs text-gray-600">
              无水印壁纸
            </p>
          </div>
          <div>
            <div class="text-2xl mb-1">
              🤖
            </div>
            <p class="text-xs text-gray-600">
              AI 深度分析
            </p>
          </div>
          <div>
            <div class="text-2xl mb-1">
              🏅
            </div>
            <p class="text-xs text-gray-600">
              专属勋章
            </p>
          </div>
          <div>
            <div class="text-2xl mb-1">
              💰
            </div>
            <p class="text-xs text-gray-600">
              额外积分
            </p>
          </div>
          <div>
            <div class="text-2xl mb-1">
              👑
            </div>
            <p class="text-xs text-gray-600">
              专属称号
            </p>
          </div>
        </div>
      </div>

      <!-- 套餐选择 -->
      <div class="space-y-3 mb-6">
        <div
          v-for="plan in plans"
          :key="plan.type"
          class="bg-white rounded-xl p-4 border-2 cursor-pointer transition-all relative"
          :class="selectedPlan === plan.type
            ? 'border-green-500 shadow-md'
            : 'border-gray-100 hover:border-gray-200'"
          @click="selectPlan(plan.type)"
        >
          <div
            v-if="plan.popular"
            class="absolute -top-2 right-4 bg-red-500 text-white text-xs px-2 py-0.5 rounded-full"
          >
            推荐
          </div>
          <div class="flex items-center justify-between">
            <div>
              <h4 class="text-sm font-bold text-gray-800">
                {{ plan.label }}
              </h4>
              <p class="text-xs text-gray-400 mt-0.5">
                {{ plan.perMonth }}
              </p>
            </div>
            <div class="text-right">
              <span class="text-xl font-bold text-green-600">{{ plan.price }}</span>
              <span class="text-xs text-gray-400 line-through ml-1">{{ plan.originalPrice }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 开通按钮 -->
      <button
        class="w-full py-3 bg-green-600 text-white rounded-xl font-medium hover:bg-green-700 transition-colors"
      >
        立即开通
      </button>
      <p class="text-xs text-gray-400 text-center mt-2">
        支付功能将在 V1.1 版本上线
      </p>
    </div>
  </div>
</template>
