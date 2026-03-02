const BASE_URL = 'https://your-api-domain.com/api/v1'

function getToken(): string {
  return uni.getStorageSync('token') || ''
}

export function request<T = unknown>(options: {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: Record<string, unknown>
}): Promise<T> {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${options.url}`,
      method: options.method || 'GET',
      data: options.data,
      header: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${getToken()}`,
      },
      success: (res) => {
        if (res.statusCode === 200 || res.statusCode === 201) {
          resolve(res.data as T)
        } else if (res.statusCode === 401) {
          uni.removeStorageSync('token')
          uni.reLaunch({ url: '/pages/profile/profile' })
          reject(new Error('未授权'))
        } else {
          reject(new Error(`请求失败: ${res.statusCode}`))
        }
      },
      fail: (err) => {
        reject(new Error(err.errMsg))
      },
    })
  })
}

export async function wxLogin(): Promise<string> {
  return new Promise((resolve, reject) => {
    uni.login({
      provider: 'weixin',
      success: async (loginRes) => {
        try {
          const data = await request<{ access_token: string }>({
            url: '/auth/wx-login',
            method: 'POST',
            data: { code: loginRes.code },
          })
          uni.setStorageSync('token', data.access_token)
          resolve(data.access_token)
        } catch (e) {
          reject(e)
        }
      },
      fail: reject,
    })
  })
}
