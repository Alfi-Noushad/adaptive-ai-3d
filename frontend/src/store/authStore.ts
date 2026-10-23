import { create } from 'zustand'

export interface User {
  id: string
  name: string
  email: string
  role: string
}

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  login: (user: User, token: string) => void
  logout: () => Promise<void>
}

function getStoredUser(): User | null {
  try {
    const raw = localStorage.getItem('current_user')
    return raw ? JSON.parse(raw) as User : null
  } catch { return null }
}

export const useAuthStore = create<AuthState>((set) => ({
  user: getStoredUser(),
  isAuthenticated: Boolean(localStorage.getItem('access_token')),
  login: (user, token) => {
    localStorage.setItem('access_token', token)
    localStorage.setItem('current_user', JSON.stringify(user))
    set({ user, isAuthenticated: true })
  },
  logout: async () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('current_user')
    set({ user: null, isAuthenticated: false })
  },
}))
