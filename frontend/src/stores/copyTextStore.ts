import { defineStore } from 'pinia'

export const useTextStore = defineStore('text', {
  state: () => ({
    copyText: ''
  }),
  getters: {
    getText (state) {
      if (state.copyText) {
        setTimeout(() => {
          state.copyText = ''
        })
        return state.copyText
      }
    }
  }
})
