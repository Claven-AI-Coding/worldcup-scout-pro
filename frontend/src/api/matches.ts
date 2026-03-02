import api from '.'

export const getMatches = (params?: { stage?: string; date?: string; status?: string }) =>
  api.get('/matches', { params })

export const getMatch = (id: number) => api.get(`/matches/${id}`)

export const getMatchEvents = (id: number) => api.get(`/matches/${id}/events`)

export const setReminder = (matchId: number, minutes: number = 30) =>
  api.post(`/matches/${matchId}/remind`, { match_id: matchId, remind_before_minutes: minutes })

export const getStandings = () => api.get('/matches/standings')
