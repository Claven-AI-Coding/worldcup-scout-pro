import api from '.'

export const generateWallpaper = (data: {
  team_id?: number
  player_id?: number
  style: string
}) => api.post('/wallpapers/generate', data)

export const getMyWallpapers = () => api.get('/wallpapers/my')

export const getGallery = (params?: { skip?: number; limit?: number }) =>
  api.get('/wallpapers/gallery', { params })
