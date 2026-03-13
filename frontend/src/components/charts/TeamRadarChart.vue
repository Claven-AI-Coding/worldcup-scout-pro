<script setup lang="ts">
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { RadarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'

use([CanvasRenderer, RadarChart, TitleComponent, TooltipComponent, LegendComponent])

interface TeamStats {
  attack: number // 进攻 0-100
  defense: number // 防守 0-100
  midfield: number // 中场 0-100
  speed: number // 速度 0-100
  technique: number // 技术 0-100
  physical: number // 体能 0-100
}

interface Props {
  team1Name: string
  team1Stats: TeamStats
  team2Name?: string
  team2Stats?: TeamStats
  height?: string
}

const props = withDefaults(defineProps<Props>(), {
  height: '400px',
})

const option = computed(() => {
  const series: any[] = [
    {
      name: props.team1Name,
      type: 'radar',
      data: [
        {
          value: [
            props.team1Stats.attack,
            props.team1Stats.defense,
            props.team1Stats.midfield,
            props.team1Stats.speed,
            props.team1Stats.technique,
            props.team1Stats.physical,
          ],
          name: props.team1Name,
        },
      ],
      areaStyle: {
        opacity: 0.3,
      },
    },
  ]

  if (props.team2Name && props.team2Stats) {
    series.push({
      name: props.team2Name,
      type: 'radar',
      data: [
        {
          value: [
            props.team2Stats.attack,
            props.team2Stats.defense,
            props.team2Stats.midfield,
            props.team2Stats.speed,
            props.team2Stats.technique,
            props.team2Stats.physical,
          ],
          name: props.team2Name,
        },
      ],
      areaStyle: {
        opacity: 0.3,
      },
    })
  }

  return {
    title: {
      text: '球队战力对比',
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
      },
    },
    tooltip: {
      trigger: 'item',
    },
    legend: {
      bottom: 10,
      data: [props.team1Name, props.team2Name].filter(Boolean),
    },
    radar: {
      indicator: [
        { name: '进攻', max: 100 },
        { name: '防守', max: 100 },
        { name: '中场', max: 100 },
        { name: '速度', max: 100 },
        { name: '技术', max: 100 },
        { name: '体能', max: 100 },
      ],
      radius: '60%',
      splitNumber: 4,
      axisName: {
        color: '#666',
        fontSize: 12,
      },
      splitLine: {
        lineStyle: {
          color: '#e5e7eb',
        },
      },
      splitArea: {
        areaStyle: {
          color: ['#f9fafb', '#ffffff'],
        },
      },
    },
    series,
  }
})
</script>

<template>
  <div class="radar-chart-container">
    <VChart :option="option" :style="{ height: props.height }" autoresize />
  </div>
</template>

<style scoped>
.radar-chart-container {
  width: 100%;
}
</style>
