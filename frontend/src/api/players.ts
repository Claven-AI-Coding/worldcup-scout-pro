import api from '.'

export const getPlayer = (id: number) => api.get(`/players/${id}`)

export const searchPlayers = (params?: { name?: string; position?: string; team_id?: number }) =>
  api.get('/players', { params })
