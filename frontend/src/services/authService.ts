import { api, unwrap } from './api'
import type { ApiEnvelope, AuthData } from '../types/api'

export const authService = {
  async login(email: string, password: string) {
    return unwrap((await api.post<ApiEnvelope<AuthData>>('/auth/login', { email, password })).data)
  },
  async register(name: string, email: string, password: string) {
    return unwrap((await api.post<ApiEnvelope<AuthData>>('/auth/register', { username: name, email, password })).data)
  },
  async forgotPassword(email: string) {
    return unwrap((await api.post<ApiEnvelope<unknown>>('/auth/forgot-password', { email })).data)
  },
  async logout() {
    return unwrap((await api.post<ApiEnvelope<unknown>>('/auth/logout')).data)
  },
}
