import { useUserStore } from 'src/stores/UserStore'
import { messageHttpClient } from '../MessagesHttpClient'
import { Message, useMessageStore } from 'src/stores/MessageStore'
import { StoreDefinition } from 'pinia'

export interface Room {
  id: number;
  name: string;
  human_need: null | true;
  main_room_id: null | number;
  assistant_room_id: null | number,
  kind: string
}
export interface Categories {
  answer: string;
  answer_class: number;
  category: string;
  id: number;
  question: string;
  score: number;
}

class MessageService {
  static async searchMessages (search: string) {
    if (!search) return
    const messageStore = useMessageStore()
    const response = await messageHttpClient().get(
      `messages?room_id=${messageStore.currentRoomId}&search=${search}`
      , { headers: { Accept: '*/*' } })
    return response.data as Message[]
  }

  static async deleteRoom (id: number) {
    const response = await messageHttpClient().delete(
      `rooms/${id}`
      , { headers: { Accept: '*/*' } })
    return response.data as Message[]
  }

  static async getRooms () {
    const store = useUserStore()
    const response = await messageHttpClient().get(
      `rooms.json?username=${store.user.username}`
    )
    return response.data as Room[]
  }

  static async sendMessage (text: string, useStore: StoreDefinition, LllmEnabled?:true) {
    const store = useUserStore()
    const messageStore = useStore()
    const response = await messageHttpClient().post(
      `messages.json?username=${store.user.username}`,
      {
        text,
        room_id: messageStore.currentRoomId,
        llm: LllmEnabled ? undefined : 'disabled'
      }
    )
    return response
  }

  static async getMessages (offset: number, useStore: StoreDefinition, limit = 20) {
    const store = useUserStore()
    const messageStore = useStore()
    const response = await messageHttpClient().get(
      `messages.json?username=${store.user.username}&room_id=${messageStore.getRoomId}&offset=${offset}&limit=${limit}`
    )
    return response.data as Message[]
  }
}

export { MessageService }
