import api from '.'

export const getPointRecords = (params?: { skip?: number; limit?: number }) =>
  api.get('/points/records', { params })
