import api from '.'

export const getTeams = (params?: { group?: string }) => api.get('/teams', { params })

export const getTeam = (id: number) => api.get(`/teams/${id}`)

export const getTeamPlayers = (id: number) => api.get(`/teams/${id}/players`)
