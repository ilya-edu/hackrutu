import { defineStore } from 'pinia'
import { AuthService } from 'services/AuthService'

function parseToken (token: string) {
  const base64Url = token.split('.')[1]
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
  const jsonPayload = decodeURIComponent(
    window
      .atob(base64)
      .split('')
      .map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)
      })
      .join('')
  )

  return JSON.parse(jsonPayload)
}

export interface User {
  accessToken?: string,
  refreshToken?: string,
  username?: string,
  roles?: []
}

export const useUserStore = defineStore('user', {
  state: () => ({
    user: {} as User
  }),
  getters: {
    isSignedIn (state) {
      return (
        !!state.user.accessToken?.length && !!state.user.refreshToken?.length
      )
    },
    isAdmin (state) {
      return state.user.username === 'admin'
    }
  },
  actions: {
    async login (login:string, password:string) {
      const resp = await AuthService.logIn(login, password)
      if (resp.name !== 'AxiosError') {
        const parsedToken = parseToken(resp.data.access_token)
        if (parsedToken.sub === 'manager') {
          this.user.username = 'admin'
        } else {
          this.user.username = parsedToken.sub
        }

        this.user.roles = parsedToken.roles
        this.user.accessToken = resp.data.access_token
        this.user.refreshToken = resp.data.refresh_token
      }
    },
    logout () {
      this.user = {}
    }
  },
  persist: true
})
