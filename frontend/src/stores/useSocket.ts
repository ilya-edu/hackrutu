import { StoreDefinition } from 'pinia'
import { useUserStore } from './UserStore'

export function connect (useStore: StoreDefinition) {
  const messageStore = useStore()
  const userStore = useUserStore()
  const ws = new WebSocket(`wss://${process.env.API}/cable?username=${userStore.user.username}`)
  ws.onopen = function () {
    ws.send(JSON.stringify({
      command: 'subscribe',
      identifier: '{"channel":"UserChannel"}'
    }))
    ws.send(JSON.stringify({
      command: 'message',
      data: '{"action": "fetch_room"}',
      identifier: '{"channel":"UserChannel"}'
    }))
  }

  ws.onmessage = function (e) {
    const resp = JSON.parse(e.data)
    if (resp.message && resp.message.kind) {
      if (resp.message.kind === 'new_message') {
        if (resp.message.object.room_id === messageStore.currentRoomId) {
          messageStore.addMessage(resp.message.object)
        }
      }
      if (resp.message.kind === 'room_id') {
        messageStore.currentRoomId = resp.message.room_id
      }
    }
  }

  ws.onclose = function () {
    setTimeout(function () {
      connect(useStore)
    }, 1000)
  }

  ws.onerror = function (err) {
    console.error('Socket encountered error: ', err, 'Closing socket')
    ws.close()
  }
  return ws
}
