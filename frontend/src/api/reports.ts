import api from '.'

export const createReport = (data: { target_type: string; target_id: number; reason?: string }) =>
  api.post('/reports', data)

export const getMyReports = (params?: { skip?: number; limit?: number }) =>
  api.get('/reports/my', { params })
