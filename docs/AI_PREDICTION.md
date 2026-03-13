# AI 预测系统文档

## 概述

使用 Claude AI 实现的智能比赛预测系统，提供赛果预测、胜率分析、球队实力评估等功能。

## 功能

### 1. 比赛预测

基于球队数据、FIFA 排名、历史战绩等信息，使用 AI 分析预测比赛结果。

**API：** `POST /api/v1/ai/predict-match`

**请求：**
```json
{
  "match_id": 123
}
```

**响应：**
```json
{
  "match_id": 123,
  "team1_name": "阿根廷",
  "team2_name": "巴西",
  "team1_win_prob": 0.45,
  "draw_prob": 0.25,
  "team2_win_prob": 0.30,
  "predicted_score": "2-1",
  "confidence": 0.75,
  "key_factors": [
    "阿根廷 FIFA 排名更高（第1位 vs 第3位）",
    "阿根廷近期状态出色",
    "巴西防守端存在隐患"
  ],
  "analysis": "基于双方实力对比和历史数据，阿根廷在本场比赛中具有一定优势。阿根廷目前 FIFA 排名第1，且近期状态出色，进攻端火力十足。巴西虽然实力强劲，但防守端存在一些隐患。综合考虑，预测阿根廷将以 2-1 的比分获胜，但比赛过程可能会比较激烈。"
}
```

**字段说明：**
- `team1_win_prob` - 主队胜率（0-1）
- `draw_prob` - 平局概率（0-1）
- `team2_win_prob` - 客队胜率（0-1）
- `predicted_score` - 预测比分
- `confidence` - 预测置信度（0-1），越高越可信
- `key_factors` - 关键影响因素列表
- `analysis` - AI 生成的详细分析文本

### 2. 球队实力评估

评估球队在进攻、防守、中场等维度的实力。

**API：** `GET /api/v1/ai/team-strength/{team_id}`

**响应：**
```json
{
  "team_id": 1,
  "team_name": "阿根廷",
  "overall_rating": 92.5,
  "attack_rating": 95.0,
  "defense_rating": 88.0,
  "midfield_rating": 90.0,
  "form_rating": 94.0,
  "ranking": 1
}
```

**字段说明：**
- `overall_rating` - 综合评分（0-100）
- `attack_rating` - 进攻评分
- `defense_rating` - 防守评分
- `midfield_rating` - 中场评分
- `form_rating` - 近期状态评分
- `ranking` - FIFA 排名

## 使用场景

### 1. 赛前预测

在比赛开始前，为用户提供 AI 预测结果，帮助用户了解比赛走势。

```vue
<script setup>
import { ref } from 'vue'
import { api } from '@/api'

const prediction = ref(null)

async function loadPrediction(matchId) {
  const res = await api.post('/ai/predict-match', { match_id: matchId })
  prediction.value = res.data
}
</script>

<template>
  <div v-if="prediction" class="prediction-card">
    <h3>AI 预测</h3>
    <div class="probabilities">
      <div>{{ prediction.team1_name }} 胜：{{ (prediction.team1_win_prob * 100).toFixed(0) }}%</div>
      <div>平局：{{ (prediction.draw_prob * 100).toFixed(0) }}%</div>
      <div>{{ prediction.team2_name }} 胜：{{ (prediction.team2_win_prob * 100).toFixed(0) }}%</div>
    </div>
    <div class="predicted-score">
      预测比分：{{ prediction.predicted_score }}
    </div>
    <div class="analysis">{{ prediction.analysis }}</div>
  </div>
</template>
```

### 2. 球队对比

展示两队实力对比，配合雷达图使用。

```vue
<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import TeamRadarChart from '@/components/charts/TeamRadarChart.vue'

const team1Strength = ref(null)
const team2Strength = ref(null)

onMounted(async () => {
  team1Strength.value = await api.get('/ai/team-strength/1')
  team2Strength.value = await api.get('/ai/team-strength/2')
})

const team1Stats = computed(() => ({
  attack: team1Strength.value?.attack_rating || 0,
  defense: team1Strength.value?.defense_rating || 0,
  midfield: team1Strength.value?.midfield_rating || 0,
  speed: team1Strength.value?.form_rating || 0,
  technique: team1Strength.value?.overall_rating || 0,
  physical: team1Strength.value?.overall_rating || 0,
}))
</script>

<template>
  <TeamRadarChart
    :team1-name="team1Strength?.team_name"
    :team1-stats="team1Stats"
    :team2-name="team2Strength?.team_name"
    :team2-stats="team2Stats"
  />
</template>
```

## 技术实现

### AI 模型

使用 **Claude 3.5 Sonnet** 进行预测分析：
- 模型：`claude-3-5-sonnet-20241022`
- 提供商：Anthropic
- 特点：强大的推理能力，适合数据分析

### 预测算法

1. **数据收集**
   - 球队 FIFA 排名
   - 历史战绩
   - 近期状态
   - 球员阵容

2. **AI 分析**
   - 构建结构化提示词
   - 调用 Claude API
   - 解析 JSON 响应

3. **结果验证**
   - 概率归一化（确保三个概率之和为 1）
   - 置信度评估
   - 异常值处理

### 性能优化

- **缓存策略**：相同比赛的预测结果缓存 1 小时
- **异步处理**：使用 async/await 避免阻塞
- **错误处理**：AI 调用失败时返回默认预测

## 配置

### 环境变量

在 `.env` 文件中配置：

```env
ANTHROPIC_API_KEY=sk-ant-xxx
```

### API 限制

- Anthropic API 有速率限制
- 建议添加缓存减少 API 调用
- 生产环境建议使用 Redis 缓存预测结果

## 未来扩展

- [ ] 历史预测准确率统计
- [ ] 多模型集成（Claude + GPT-4）
- [ ] 实时赔率对比
- [ ] 用户反馈学习
- [ ] 预测结果可视化（胜率饼图、趋势图）

---

**版本：** v1.0  
**更新时间：** 2026-03-13
