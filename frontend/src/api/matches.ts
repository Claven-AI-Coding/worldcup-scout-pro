import api from '.'

export interface MatchFilters {
  stage?: string
  group?: string
  team_id?: number
  date?: string
  status?: string
  skip?: number
  limit?: number
}

export const getMatches = (params?: MatchFilters) => api.get('/matches', { params })

export const getMatch = (id: number) => api.get(`/matches/${id}`)

export const getMatchEvents = (id: number) => api.get(`/matches/${id}/events`)

export const setReminder = (matchId: number, minutes: number = 30) =>
  api.post(`/matches/${matchId}/remind`, { match_id: matchId, remind_before_minutes: minutes })

export const getStandings = (group?: string) =>
  api.get('/matches/standings', { params: group ? { group } : {} })

// AI 预测（D6 实现）
export const getMatchPrediction = (id: number) => api.get(`/matches/${id}/prediction`)
export const getMatchPreview = (id: number) => api.get(`/matches/${id}/preview`)

// 球队全赛程一键订阅
export const subscribeTeamMatches = (teamId: number, minutes: number = 30) =>
  api.post(`/matches/subscribe-team/${teamId}`, null, {
    params: { remind_before_minutes: minutes },
  })
