import api from '.'

export const getScorers = (limit: number = 20) =>
  api.get('/rankings/scorers', { params: { limit } })

export const getAssists = (limit: number = 20) =>
  api.get('/rankings/assists', { params: { limit } })
