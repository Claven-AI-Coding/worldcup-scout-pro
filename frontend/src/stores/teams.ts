import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getTeams, getTeam, getTeamPlayers } from '@/api/teams'

interface Team {
  id: number
  name: string
  name_en: string | null
  code: string
  group_name: string | null
  flag_url: string | null
  coach: string | null
  description: string | null
  stats: Record<string, unknown> | null
}

interface Player {
  id: number
  team_id: number
  name: string
  number: number | null
  position: string | null
  age: number | null
  club: string | null
}

export const useTeamStore = defineStore('teams', () => {
  const teams = ref<Team[]>([])
  const currentTeam = ref<Team | null>(null)
  const teamPlayers = ref<Player[]>([])
  const loading = ref(false)

  async function fetchTeams(group?: string) {
    loading.value = true
    try {
      const res = await getTeams(group ? { group } : undefined)
      teams.value = res.data.items || res.data
    } finally {
      loading.value = false
    }
  }

  async function fetchTeam(id: number) {
    loading.value = true
    try {
      const res = await getTeam(id)
      currentTeam.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function fetchTeamPlayers(id: number) {
    const res = await getTeamPlayers(id)
    teamPlayers.value = res.data.items || res.data
  }

  return { teams, currentTeam, teamPlayers, loading, fetchTeams, fetchTeam, fetchTeamPlayers }
})
