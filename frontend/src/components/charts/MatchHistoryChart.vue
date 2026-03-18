<script setup lang="ts">
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from 'echarts/components'

use([CanvasRenderer, BarChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

interface MatchHistory {
  date: string
  team1Score: number
  team2Score: number
  venue: string
}

interface Props {
  team1Name: string
  team2Name: string
  history: MatchHistory[]
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  height: '400px',
})

const option = computed(() => {
  const dates = props.history.map(h => h.date.slice(0, 10))
  const team1Scores = props.history.map(h => h.team1Score)
  const team2Scores = props.history.map(h => h.team2Score)

  return {
    title: {
      text: '历史交锋记录',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
      },
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
      formatter: (params: { dataIndex: number }[]) => {
        const index = params[0].dataIndex
        const match = props.history[index]
        return `
          <div style="padding: 8px;">
            <div style="font-weight: bold; margin-bottom: 4px;">${match.date.slice(0, 10)}</div>
            <div>${props.team1Name}: ${match.team1Score}</div>
            <div>${props.team2Name}: ${match.team2Score}</div>
            <div style="color: #666; font-size: 12px; margin-top: 4px;">${match.venue}</div>
          </div>
        `
      },
    },
    legend: {
      bottom: 10,
      data: [props.team1Name, props.team2Name],
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLabel: {
        rotate: 45,
        fontSize: 11,
      },
    },
    yAxis: {
      type: 'value',
      name: '进球数',
      minInterval: 1,
    },
    series: [
      {
        name: props.team1Name,
        type: 'bar',
        data: team1Scores,
        itemStyle: {
          color: '#3b82f6',
        },
      },
      {
        name: props.team2Name,
        type: 'bar',
        data: team2Scores,
        itemStyle: {
          color: '#ef4444',
        },
      },
    ],
  }
})

const stats = computed(() => {
  let team1Wins = 0
  let team2Wins = 0
  let draws = 0

  props.history.forEach(match => {
    if (match.team1Score > match.team2Score) team1Wins++
    else if (match.team2Score > match.team1Score) team2Wins++
    else draws++
  })

  return { team1Wins, team2Wins, draws }
})
</script>

<template>
  <div class="history-chart-container">
    <div class="mb-4 flex justify-center gap-6 text-sm">
      <div class="text-center">
        <div class="font-bold text-blue-600">
          {{ stats.team1Wins }}
        </div>
        <div class="text-gray-600">{{ team1Name }}胜</div>
      </div>
      <div class="text-center">
        <div class="font-bold text-gray-600">
          {{ stats.draws }}
        </div>
        <div class="text-gray-600">平局</div>
      </div>
      <div class="text-center">
        <div class="font-bold text-red-600">
          {{ stats.team2Wins }}
        </div>
        <div class="text-gray-600">{{ team2Name }}胜</div>
      </div>
    </div>
    <VChart :option="option" :style="{ height: props.height }" autoresize />
  </div>
</template>

<style scoped>
.history-chart-container {
  width: 100%;
}
</style>
