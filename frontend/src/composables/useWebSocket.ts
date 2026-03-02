import { ref, onUnmounted } from 'vue'

export function useWebSocket(matchId: number) {
  const data = ref<Record<string, unknown> | null>(null)
  const connected = ref(false)
  let ws: WebSocket | null = null

  function connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    ws = new WebSocket(`${protocol}//${window.location.host}/api/v1/ws/live/${matchId}`)

    ws.onopen = () => {
      connected.value = true
    }

    ws.onmessage = (event) => {
      data.value = JSON.parse(event.data)
    }

    ws.onclose = () => {
      connected.value = false
    }
  }

  function disconnect() {
    ws?.close()
    ws = null
    connected.value = false
  }

  onUnmounted(() => disconnect())

  return { data, connected, connect, disconnect }
}
