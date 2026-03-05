import api from '.'

export const getDailyTasks = () => api.get('/tasks/daily')

export const completeTask = (taskType: string) =>
  api.post(`/tasks/${taskType}/complete`)

export const signIn = () => api.post('/tasks/sign-in')
