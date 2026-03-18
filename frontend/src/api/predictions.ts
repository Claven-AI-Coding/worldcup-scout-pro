import api from '.'

export const getMatchPrediction = (matchId: number) => api.get(`/predictions/matches/${matchId}`)

export const submitPrediction = (data: {
  match_id: number
  predicted_result: string
  predicted_home_score?: number
  predicted_away_score?: number
  points_wagered?: number
}) => api.post('/predictions', data)

export const getLeaderboard = (type: 'daily' | 'all' = 'all') =>
  api.get('/predictions/leaderboard', { params: { type } })

export const getMyPredictions = () => api.get('/predictions/my')
