// stores/user.ts
import { defineStore } from 'pinia'
import { jwtDecode } from 'jwt-decode'

interface JwtPayload {
  username?: string
  sub?: string
  exp?: number
}

export const useUserStore = defineStore('user', {
  state: () => ({
    username: '',
    isAuthenticated: false
  }),
  actions: {
    loadFromToken() {
      const token = localStorage.getItem('access_token')
      if (!token) {
        this.isAuthenticated = false
        return
      }

      try {
        const decoded = jwtDecode<JwtPayload>(token)
        const now = Math.floor(Date.now() / 1000)

        if (decoded.exp && decoded.exp < now) {
          // токен истёк
          this.logout()
          return
        }

        this.username = decoded.username || `User${decoded.sub}` || 'Guest'
        
        console.log('Decoded token:', decoded)
        this.isAuthenticated = true
      } catch {
        this.logout()
      }
    },
    logout() {
      localStorage.removeItem('access_token')
      this.username = ''
      this.isAuthenticated = false
    }
  }
})
