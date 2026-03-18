<script setup lang="ts">
interface StandingEntry {
  position: number
  team_id: number
  team_name: string
  team_code: string
  played: number
  won: number
  drawn: number
  lost: number
  goals_for: number
  goals_against: number
  goal_difference: number
  points: number
}

interface Props {
  standings: StandingEntry[]
  groupName: string
}

const props = defineProps<Props>()

function positionClass(pos: number): string {
  if (pos <= 2) return 'text-green-600 font-bold'
  return 'text-gray-500'
}
</script>

<template>
  <div class="overflow-hidden rounded-xl border border-gray-100 bg-white shadow-sm">
    <!-- Group header -->
    <div class="border-b border-gray-100 bg-gray-50 px-4 py-3">
      <h3 class="text-sm font-bold text-gray-700">
        {{ props.groupName }}
      </h3>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-gray-100 text-xs uppercase text-gray-400">
            <th class="w-8 px-3 py-2 text-left">#</th>
            <th class="px-3 py-2 text-left">球队</th>
            <th class="w-8 px-2 py-2 text-center">场</th>
            <th class="w-8 px-2 py-2 text-center">胜</th>
            <th class="w-8 px-2 py-2 text-center">平</th>
            <th class="w-8 px-2 py-2 text-center">负</th>
            <th class="w-8 px-2 py-2 text-center">进</th>
            <th class="w-8 px-2 py-2 text-center">失</th>
            <th class="w-10 px-2 py-2 text-center">净胜</th>
            <th class="w-10 px-3 py-2 text-center font-bold">积分</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="entry in props.standings"
            :key="entry.team_id"
            class="border-b border-gray-50 transition-colors last:border-b-0 hover:bg-gray-50"
          >
            <td class="px-3 py-2.5" :class="positionClass(entry.position)">
              {{ entry.position }}
            </td>
            <td class="px-3 py-2.5">
              <div class="flex items-center gap-2">
                <span class="w-6 font-mono text-xs text-gray-400">{{ entry.team_code }}</span>
                <span class="text-sm font-medium text-gray-700">{{ entry.team_name }}</span>
              </div>
            </td>
            <td class="px-2 py-2.5 text-center text-gray-600">
              {{ entry.played }}
            </td>
            <td class="px-2 py-2.5 text-center text-gray-600">
              {{ entry.won }}
            </td>
            <td class="px-2 py-2.5 text-center text-gray-600">
              {{ entry.drawn }}
            </td>
            <td class="px-2 py-2.5 text-center text-gray-600">
              {{ entry.lost }}
            </td>
            <td class="px-2 py-2.5 text-center text-gray-600">
              {{ entry.goals_for }}
            </td>
            <td class="px-2 py-2.5 text-center text-gray-600">
              {{ entry.goals_against }}
            </td>
            <td
              class="px-2 py-2.5 text-center font-medium"
              :class="
                entry.goal_difference > 0
                  ? 'text-green-600'
                  : entry.goal_difference < 0
                    ? 'text-red-500'
                    : 'text-gray-500'
              "
            >
              {{ entry.goal_difference > 0 ? '+' : '' }}{{ entry.goal_difference }}
            </td>
            <td class="px-3 py-2.5 text-center font-bold text-gray-800">
              {{ entry.points }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
