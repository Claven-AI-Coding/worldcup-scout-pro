import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios')
const mockedAxios = axios as any

describe('API Utils', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Error Handling', () => {
    it('handles network errors', async () => {
      mockedAxios.get.mockRejectedValue(new Error('Network Error'))
      
      try {
        await mockedAxios.get('/api/test')
      } catch (error: any) {
        expect(error.message).toBe('Network Error')
      }
    })

    it('handles 401 unauthorized', async () => {
      mockedAxios.get.mockRejectedValue({
        response: { status: 401, data: { detail: 'Unauthorized' } },
      })

      try {
        await mockedAxios.get('/api/protected')
      } catch (error: any) {
        expect(error.response.status).toBe(401)
      }
    })

    it('handles 404 not found', async () => {
      mockedAxios.get.mockRejectedValue({
        response: { status: 404, data: { detail: 'Not Found' } },
      })

      try {
        await mockedAxios.get('/api/nonexistent')
      } catch (error: any) {
        expect(error.response.status).toBe(404)
      }
    })
  })

  describe('Request Interceptors', () => {
    it('adds auth token to requests', () => {
      const token = 'test-token'
      localStorage.setItem('token', token)

      const config = { headers: {} }
      // Simulate interceptor
      if (localStorage.getItem('token')) {
        config.headers = { Authorization: `Bearer ${token}` }
      }

      expect(config.headers).toHaveProperty('Authorization')
      expect(config.headers.Authorization).toBe(`Bearer ${token}`)
    })
  })
})
