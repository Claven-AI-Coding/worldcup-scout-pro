# 数据可视化组件文档

## 概述

使用 ECharts 实现的数据可视化组件，用于展示球队数据、历史交锋、积分趋势等。

## 组件列表

### 1. TeamRadarChart - 球队战力雷达图

展示球队在进攻、防守、中场、速度、技术、体能等维度的能力值。

**使用示例：**
```vue
<script setup>
import TeamRadarChart from '@/components/charts/TeamRadarChart.vue'

const team1Stats = {
  attack: 85,
  defense: 78,
  midfield: 82,
  speed: 80,
  technique: 88,
  physical: 75
}

const team2Stats = {
  attack: 80,
  defense: 85,
  midfield: 75,
  speed: 78,
  technique: 82,
  physical: 80
}
</script>

<template>
  <TeamRadarChart
    team1-name="阿根廷"
    :team1-stats="team1Stats"
    team2-name="巴西"
    :team2-stats="team2Stats"
    height="500px"
  />
</template>
```

**Props：**
- `team1Name` (string, required) - 球队1名称
- `team1Stats` (TeamStats, required) - 球队1数据
- `team2Name` (string, optional) - 球队2名称
- `team2Stats` (TeamStats, optional) - 球队2数据
- `height` (string, optional) - 图表高度，默认 '400px'

**TeamStats 接口：**
```typescript
interface TeamStats {
  attack: number    // 进攻 0-100
  defense: number   // 防守 0-100
  midfield: number  // 中场 0-100
  speed: number     // 速度 0-100
  technique: number // 技术 0-100
  physical: number  // 体能 0-100
}
```

---

### 2. MatchHistoryChart - 历史交锋柱状图

展示两队历史交锋记录，包括比分和胜负统计。

**使用示例：**
```vue
<script setup>
import MatchHistoryChart from '@/components/charts/MatchHistoryChart.vue'

const history = [
  { date: '2022-12-18', team1Score: 3, team2Score: 3, venue: '卢赛尔体育场' },
  { date: '2021-07-11', team1Score: 1, team2Score: 0, venue: '马拉卡纳球场' },
  { date: '2019-07-03', team1Score: 0, team2Score: 2, venue: '米内罗球场' },
]
</script>

<template>
  <MatchHistoryChart
    team1-name="阿根廷"
    team2-name="巴西"
    :history="history"
  />
</template>
```

**Props：**
- `team1Name` (string, required) - 球队1名称
- `team2Name` (string, required) - 球队2名称
- `history` (MatchHistory[], required) - 历史交锋记录
- `height` (string, optional) - 图表高度，默认 '400px'

**MatchHistory 接口：**
```typescript
interface MatchHistory {
  date: string        // 比赛日期
  team1Score: number  // 球队1比分
  team2Score: number  // 球队2比分
  venue: string       // 比赛场地
}
```

---

### 3. StandingsTrendChart - 积分榜趋势图

展示小组内各队积分随轮次变化的趋势。

**使用示例：**
```vue
<script setup>
import StandingsTrendChart from '@/components/charts/StandingsTrendChart.vue'

const trends = [
  { teamName: '阿根廷', points: [3, 6, 9], color: '#3b82f6' },
  { teamName: '墨西哥', points: [3, 4, 6], color: '#10b981' },
  { teamName: '波兰', points: [0, 3, 4], color: '#f59e0b' },
  { teamName: '沙特', points: [3, 3, 3], color: '#ef4444' },
]

const rounds = ['第1轮', '第2轮', '第3轮']
</script>

<template>
  <StandingsTrendChart
    :trends="trends"
    :rounds="rounds"
  />
</template>
```

**Props：**
- `trends` (TeamTrend[], required) - 各队积分趋势
- `rounds` (string[], required) - 轮次标签
- `height` (string, optional) - 图表高度，默认 '400px'

**TeamTrend 接口：**
```typescript
interface TeamTrend {
  teamName: string  // 球队名称
  points: number[]  // 每轮积分
  color?: string    // 线条颜色（可选）
}
```

---

## 安装依赖

```bash
cd frontend
npm install echarts vue-echarts
```

## 全局注册（可选）

如果需要全局使用，可以在 `main.ts` 中注册：

```typescript
import { createApp } from 'vue'
import ECharts from 'vue-echarts'
import App from './App.vue'

const app = createApp(App)
app.component('VChart', ECharts)
app.mount('#app')
```

## 响应式设计

所有图表组件都支持响应式调整大小，使用 `autoresize` 属性自动适应容器尺寸。

## 性能优化

- 使用按需引入，只加载需要的 ECharts 模块
- 图表数据变化时自动更新，无需手动刷新
- 支持大数据量渲染（建议单个图表数据点 < 1000）

## 样式定制

可以通过修改 ECharts option 来定制图表样式：
- 颜色主题
- 字体大小
- 图例位置
- 坐标轴样式

---

**版本：** v1.0  
**更新时间：** 2026-03-13
