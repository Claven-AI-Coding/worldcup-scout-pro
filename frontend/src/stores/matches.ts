import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getMatches, getMatch } from '@/api/matches'

interface Team {
  id: number
  name: string
  code: string
  flag_url: string | null
}

interface Match {
  id: number
  stage: string
  group_name: string | null
  home_team: Team
  away_team: Team
  home_score: number | null
  away_score: number | null
  status: string
  start_time: string
  venue: string | null
}

export const useMatchStore = defineStore('matches', () => {
  const matches = ref<Match[]>([])
  const currentMatch = ref<Match | null>(null)
  const loading = ref(false)

  async function fetchMatches(params?: { stage?: string; group?: string; team_id?: number; date?: string; status?: string; limit?: number }) {
    loading.value = true
    try {
      const res = await getMatches(params)
      matches.value = res.data.items || res.data
    } finally {
      loading.value = false
    }
  }

  async function fetchMatch(id: number) {
    loading.value = true
    try {
      const res = await getMatch(id)
      currentMatch.value = res.data
    } finally {
      loading.value = false
    }
  }

  return { matches, currentMatch, loading, fetchMatches, fetchMatch }
})
