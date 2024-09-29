import { defineStore } from 'pinia'
import { MessageService, Room } from 'src/api/services/MessageService'
import { useMessageStore } from './MessageStore'
import { useModelMessageStore } from './ModelMessageStore'

export const useRoomsStore = defineStore('rooms', {
  state: () => ({
    rooms: [] as Room[]
  }),
  actions: {
    async setFirstRoom () {
      const room = this.rooms.find(({ human_need: humanNeed }) => humanNeed)
      if (room) {
        this.changeRoom(room.id, room.main_room_id)
        this.rooms = await MessageService.getRooms()
      }
    },
    changeRoom (id:number, modelId: number | null) {
      const messageStore = useMessageStore()
      const ModelMessageStore = useModelMessageStore()
      messageStore.changeRoom(id)
      if (modelId) {
        ModelMessageStore.changeRoom(modelId)
      }
    }
  }
})
