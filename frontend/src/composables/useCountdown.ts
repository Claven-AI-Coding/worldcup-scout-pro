import { ref, onUnmounted } from 'vue'

export function useCountdown(targetTime: string) {
  const days = ref(0)
  const hours = ref(0)
  const minutes = ref(0)
  const seconds = ref(0)
  const expired = ref(false)

  let timer: ReturnType<typeof setInterval> | null = null

  function update() {
    const now = Date.now()
    const target = new Date(targetTime).getTime()
    const diff = target - now

    if (diff <= 0) {
      expired.value = true
      if (timer) clearInterval(timer)
      return
    }

    days.value = Math.floor(diff / (1000 * 60 * 60 * 24))
    hours.value = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
    minutes.value = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
    seconds.value = Math.floor((diff % (1000 * 60)) / 1000)
  }

  function start() {
    update()
    timer = setInterval(update, 1000)
  }

  onUnmounted(() => {
    if (timer) clearInterval(timer)
  })

  return { days, hours, minutes, seconds, expired, start }
}
