import api from '.'

export const getPosts = (teamId: number, params?: { skip?: number; limit?: number }) =>
  api.get(`/community/${teamId}/posts`, { params })

export const createPost = (data: { team_id: number; content: string; images?: string[] }) =>
  api.post('/community/posts', data)

export const likePost = (postId: number) => api.post(`/community/posts/${postId}/like`)

export const commentOnPost = (postId: number, content: string) =>
  api.post(`/community/posts/${postId}/comment`, { content })

export const getComments = (postId: number) => api.get(`/community/posts/${postId}/comments`)

export const getHotPosts = (params?: { skip?: number; limit?: number }) =>
  api.get('/community/hot', { params })
