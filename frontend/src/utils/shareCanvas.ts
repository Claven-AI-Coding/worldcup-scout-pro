/**
 * Canvas 分享海报生成工具
 */

interface ShareCardOptions {
  title: string
  subtitle?: string
  teamCode?: string
  qrCodeUrl?: string
  width?: number
  height?: number
}

/**
 * 生成分享海报（Canvas）
 */
export async function generateShareCard(options: ShareCardOptions): Promise<string> {
  const { title, subtitle = '世界杯球探 Pro', teamCode = '', width = 750, height = 1334 } = options

  const canvas = document.createElement('canvas')
  canvas.width = width
  canvas.height = height
  const ctx = canvas.getContext('2d')!

  // 背景渐变
  const gradient = ctx.createLinearGradient(0, 0, 0, height)
  gradient.addColorStop(0, '#16a34a')
  gradient.addColorStop(1, '#15803d')
  ctx.fillStyle = gradient
  ctx.fillRect(0, 0, width, height)

  // 装饰元素
  ctx.fillStyle = 'rgba(255, 255, 255, 0.05)'
  ctx.beginPath()
  ctx.arc(width * 0.8, height * 0.2, 200, 0, Math.PI * 2)
  ctx.fill()

  // 标题
  ctx.fillStyle = '#ffffff'
  ctx.font = 'bold 48px sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText(title, width / 2, height * 0.35)

  // 球队代码
  if (teamCode) {
    ctx.font = 'bold 120px sans-serif'
    ctx.fillStyle = 'rgba(255, 255, 255, 0.2)'
    ctx.fillText(teamCode, width / 2, height * 0.55)
  }

  // 副标题
  ctx.font = '28px sans-serif'
  ctx.fillStyle = 'rgba(255, 255, 255, 0.7)'
  ctx.fillText(subtitle, width / 2, height * 0.75)

  // 底部 slogan
  ctx.font = '24px sans-serif'
  ctx.fillStyle = 'rgba(255, 255, 255, 0.5)'
  ctx.fillText('2026 FIFA World Cup', width / 2, height * 0.9)

  return canvas.toDataURL('image/png')
}

/**
 * 下载图片
 */
export function downloadImage(dataUrl: string, filename: string = 'share.png') {
  const link = document.createElement('a')
  link.href = dataUrl
  link.download = filename
  link.click()
}
