import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as any | null,
    isAuthenticated: false,
  }),
  actions: {
    async login(userId: number, password: string) {
      try {
        const response = await api.post('/login', { user_id: userId, password })
        this.user = response.data.user
        this.isAuthenticated = true
        return true
      } catch (error) {
        console.error('Login failed:', error)
        return false
      }
    },
    async logout() {
      try {
        await api.post('/logout')
        this.user = null
        this.isAuthenticated = false
      } catch (error) {
        console.error('Logout failed:', error)
      }
    },
    async checkAuth() {
      try {
        // Try to get account info to check if session is valid
        const response = await api.get('/account')
        this.user = response.data.user
        this.isAuthenticated = true
      } catch (error) {
        this.user = null
        this.isAuthenticated = false
      }
    },
  },
})
