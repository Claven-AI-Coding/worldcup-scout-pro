<script setup lang="ts">
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from 'echarts/components'

use([CanvasRenderer, LineChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

interface TeamTrend {
  teamName: string
  points: number[] // 每轮积分
  color?: string
}

interface Props {
  trends: TeamTrend[]
  rounds: string[] // 轮次标签 ['第1轮', '第2轮', ...]
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  height: '400px',
})

const option = computed(() => {
  const series = props.trends.map(trend => ({
    name: trend.teamName,
    type: 'line',
    data: trend.points,
    smooth: true,
    itemStyle: {
      color: trend.color,
    },
    lineStyle: {
      width: 2,
    },
    symbol: 'circle',
    symbolSize: 6,
  }))

  return {
    title: {
      text: '小组积分趋势',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
      },
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
      },
    },
    legend: {
      bottom: 10,
      data: props.trends.map(t => t.teamName),
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: props.rounds,
      boundaryGap: false,
    },
    yAxis: {
      type: 'value',
      name: '积分',
      minInterval: 1,
    },
    series,
  }
})
</script>

<template>
  <div class="trend-chart-container">
    <VChart :option="option" :style="{ height: props.height }" autoresize />
  </div>
</template>

<style scoped>
.trend-chart-container {
  width: 100%;
}
</style>
