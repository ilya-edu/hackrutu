import { defineStore } from 'pinia'
import { Message } from './MessageStore'
import { MessageService } from 'src/api/services/MessageService'

export const useSearchStore = defineStore('search', {
  state: () => ({
    searchedMessages: [] as Message[]
  }),
  actions: {
    async setSearch (v: string) {
      if (!v) {
        this.searchedMessages = []
        return
      }
      const resp = await MessageService.searchMessages(v)
      if (resp) {
        this.searchedMessages = resp
      } else {
        this.searchedMessages = []
      }
    }
  }
})
