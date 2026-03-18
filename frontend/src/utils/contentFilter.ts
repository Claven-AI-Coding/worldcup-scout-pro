/**
 * 前端内容预过滤
 * 客户端侧简单检测，完整过滤由后端保障
 */

// 前端基础违禁词列表（精简版）
const BASIC_BANNED_WORDS = [
  '赌博',
  '赌球',
  '下注',
  '庄家',
  '盘口',
  '外围',
  '买球',
  '加微信',
  '加QQ',
  '免费领',
  '扫码领取',
  '日赚',
  '月入',
]

/**
 * 客户端预检测内容是否包含违禁词
 */
export function preCheckContent(text: string): { isClean: boolean; warning: string } {
  const cleanText = text.replace(/\s+/g, '').toLowerCase()

  for (const word of BASIC_BANNED_WORDS) {
    if (cleanText.includes(word)) {
      return {
        isClean: false,
        warning: '内容可能包含违规词汇，发布后将由系统审核',
      }
    }
  }

  return { isClean: true, warning: '' }
}

/**
 * 检查文本长度
 */
export function checkLength(text: string, max: number = 500): boolean {
  return text.length <= max
}
